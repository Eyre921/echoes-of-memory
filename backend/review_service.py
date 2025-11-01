"""
回顾生成服务 - 协调数据聚合和AI分析,生成完整的回顾报告
"""

from typing import Optional, Dict
from datetime import datetime
from sqlalchemy.orm import Session
from database import Review, get_db
from review_aggregator import DataAggregator, TimeRangeCalculator
from review_analyzer import ReviewAnalyzer
import json


class ReviewService:
    """回顾生成服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.aggregator = DataAggregator(db)
        self.analyzer = ReviewAnalyzer()
        self.time_calculator = TimeRangeCalculator()
    
    def generate_review(
        self,
        user_id: int,
        review_type: str,
        year: int,
        month: Optional[int] = None,
        regenerate: bool = False
    ) -> Dict:
        """
        生成回顾报告
        
        Args:
            user_id: 用户ID
            review_type: 回顾类型 ('monthly' 或 'annual')
            year: 年份
            month: 月份 (月度回顾必填)
            regenerate: 是否强制重新生成
            
        Returns:
            回顾报告数据
        """
        # 验证参数
        if review_type == 'monthly' and month is None:
            raise ValueError("月度回顾必须指定月份")
        
        if review_type not in ['monthly', 'annual']:
            raise ValueError("回顾类型必须是 'monthly' 或 'annual'")
        
        # 计算时间范围
        if review_type == 'monthly':
            period_start, period_end = self.time_calculator.get_monthly_range(year, month)
        else:
            period_start, period_end = self.time_calculator.get_annual_range(year)
        
        # 检查是否已存在相同时间段的回顾报告
        existing_review = self._get_existing_review(
            user_id, review_type, period_start, period_end
        )
        
        if existing_review and not regenerate:
            # 返回已有报告
            return self._format_review_response(existing_review)
        
        # 聚合数据
        aggregated_data = self.aggregator.aggregate_review_data(
            user_id, period_start, period_end
        )
        
        # 检查数据量是否足够
        if not self._check_data_sufficiency(aggregated_data, review_type):
            # 数据量不足但仍允许生成,只是添加警告
            pass
        
        # AI分析
        analysis_result = self.analyzer.analyze(aggregated_data, review_type)
        
        # 保存或更新回顾报告
        if existing_review:
            review = self._update_review(existing_review, aggregated_data, analysis_result)
        else:
            review = self._create_review(
                user_id, review_type, period_start, period_end,
                aggregated_data, analysis_result
            )
        
        return self._format_review_response(review)
    
    def get_review(self, review_id: int, user_id: int) -> Optional[Dict]:
        """
        获取回顾报告
        
        Args:
            review_id: 回顾报告ID
            user_id: 用户ID (用于权限验证)
            
        Returns:
            回顾报告数据,如果不存在或无权访问则返回None
        """
        review = self.db.query(Review).filter(
            Review.id == review_id,
            Review.user_id == user_id
        ).first()
        
        if not review:
            return None
        
        return self._format_review_response(review)
    
    def list_reviews(
        self,
        user_id: int,
        review_type: Optional[str] = None,
        year: Optional[int] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Dict:
        """
        获取回顾报告列表
        
        Args:
            user_id: 用户ID
            review_type: 回顾类型筛选 ('monthly', 'annual' 或 None)
            year: 年份筛选
            page: 页码
            page_size: 每页数量
            
        Returns:
            分页的回顾报告列表
        """
        # 构建查询
        query = self.db.query(Review).filter(Review.user_id == user_id)
        
        if review_type and review_type != 'all':
            query = query.filter(Review.review_type == review_type)
        
        if year:
            # 筛选指定年份的回顾
            year_start = datetime(year, 1, 1)
            year_end = datetime(year, 12, 31, 23, 59, 59)
            query = query.filter(
                Review.period_start >= year_start,
                Review.period_end <= year_end
            )
        
        # 计算总数
        total = query.count()
        
        # 分页查询
        reviews = query.order_by(Review.period_start.desc()).offset(
            (page - 1) * page_size
        ).limit(page_size).all()
        
        # 格式化列表数据
        review_list = []
        for review in reviews:
            review_list.append({
                'review_id': review.id,
                'review_type': review.review_type,
                'period_start': review.period_start.isoformat(),
                'period_end': review.period_end.isoformat(),
                'summary': review.summary[:200] + '...' if len(review.summary) > 200 else review.summary,
                'generated_at': review.generated_at.isoformat(),
                'status': review.status
            })
        
        return {
            'total': total,
            'page': page,
            'page_size': page_size,
            'reviews': review_list
        }
    
    def delete_review(self, review_id: int, user_id: int) -> bool:
        """
        删除回顾报告
        
        Args:
            review_id: 回顾报告ID
            user_id: 用户ID (用于权限验证)
            
        Returns:
            是否删除成功
        """
        review = self.db.query(Review).filter(
            Review.id == review_id,
            Review.user_id == user_id
        ).first()
        
        if not review:
            return False
        
        self.db.delete(review)
        self.db.commit()
        
        return True
    
    def _get_existing_review(
        self,
        user_id: int,
        review_type: str,
        period_start: datetime,
        period_end: datetime
    ) -> Optional[Review]:
        """查询已存在的回顾报告"""
        return self.db.query(Review).filter(
            Review.user_id == user_id,
            Review.review_type == review_type,
            Review.period_start == period_start,
            Review.period_end == period_end
        ).first()
    
    def _check_data_sufficiency(self, aggregated_data: Dict, review_type: str) -> bool:
        """
        检查数据量是否足够
        
        根据设计文档:
        - 月度回顾: 最小5次对话,3条记忆
        - 年度回顾: 最小20次对话,10条记忆
        """
        statistics = aggregated_data['statistics']
        
        if review_type == 'monthly':
            min_conversations = 5
            min_memories = 3
        else:  # annual
            min_conversations = 20
            min_memories = 10
        
        return (
            statistics['total_conversations'] >= min_conversations and
            statistics['total_structured_memories'] >= min_memories
        )
    
    def _create_review(
        self,
        user_id: int,
        review_type: str,
        period_start: datetime,
        period_end: datetime,
        aggregated_data: Dict,
        analysis_result: Dict
    ) -> Review:
        """创建新的回顾报告"""
        review = Review(
            user_id=user_id,
            review_type=review_type,
            period_start=period_start,
            period_end=period_end,
            summary=analysis_result['summary'],
            key_events=analysis_result['key_events'],
            emotion_analysis=analysis_result['emotion_analysis'],
            topics=analysis_result['topics'],
            statistics=aggregated_data['statistics'],
            highlights=analysis_result['highlights'],
            growth_insights=analysis_result['growth_insights'],
            visualization_data=analysis_result['visualization_data'],
            status='completed'
        )
        
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        
        return review
    
    def _update_review(
        self,
        existing_review: Review,
        aggregated_data: Dict,
        analysis_result: Dict
    ) -> Review:
        """更新已存在的回顾报告"""
        existing_review.summary = analysis_result['summary']
        existing_review.key_events = analysis_result['key_events']
        existing_review.emotion_analysis = analysis_result['emotion_analysis']
        existing_review.topics = analysis_result['topics']
        existing_review.statistics = aggregated_data['statistics']
        existing_review.highlights = analysis_result['highlights']
        existing_review.growth_insights = analysis_result['growth_insights']
        existing_review.visualization_data = analysis_result['visualization_data']
        existing_review.generated_at = datetime.utcnow()
        existing_review.status = 'completed'
        
        self.db.commit()
        self.db.refresh(existing_review)
        
        return existing_review
    
    def _format_review_response(self, review: Review) -> Dict:
        """格式化回顾报告响应数据"""
        return {
            'review_id': review.id,
            'user_id': review.user_id,
            'review_type': review.review_type,
            'period_start': review.period_start.isoformat(),
            'period_end': review.period_end.isoformat(),
            'summary': review.summary,
            'key_events': review.key_events,
            'emotion_analysis': review.emotion_analysis,
            'topics': review.topics,
            'statistics': review.statistics,
            'highlights': review.highlights,
            'growth_insights': review.growth_insights,
            'visualization_data': review.visualization_data,
            'generated_at': review.generated_at.isoformat(),
            'status': review.status
        }


class ReviewExporter:
    """回顾报告导出器"""
    
    def export_to_markdown(self, review_data: Dict) -> str:
        """
        导出为Markdown格式
        
        Args:
            review_data: 回顾报告数据
            
        Returns:
            Markdown格式文本
        """
        md_parts = []
        
        # 标题
        period_label = self._format_period_label(
            review_data['review_type'],
            review_data['period_start'],
            review_data['period_end']
        )
        md_parts.append(f"# {period_label}回顾\n\n")
        
        # 总结
        md_parts.append(f"## 总结\n\n{review_data['summary']}\n\n")
        
        # 统计数据
        md_parts.append("## 数据统计\n\n")
        stats = review_data['statistics']
        md_parts.append(f"- 对话次数: {stats.get('total_conversations', 0)}\n")
        md_parts.append(f"- 消息数量: {stats.get('total_messages', 0)}\n")
        md_parts.append(f"- 活跃天数: {stats.get('active_days', 0)}\n")
        md_parts.append(f"- 记忆片段: {stats.get('total_structured_memories', 0)}\n\n")
        
        # 关键事件
        md_parts.append("## 关键事件\n\n")
        for event in review_data.get('key_events', []):
            md_parts.append(f"### {event['title']}\n\n")
            md_parts.append(f"**日期**: {event['date']}\n\n")
            md_parts.append(f"{event['description']}\n\n")
        
        # 主题分布
        md_parts.append("## 主题分布\n\n")
        for topic in review_data.get('topics', []):
            md_parts.append(f"- **{topic['topic_name']}**: {topic['frequency']}次\n")
        md_parts.append("\n")
        
        # 成长洞察
        md_parts.append("## 成长洞察\n\n")
        for insight in review_data.get('growth_insights', []):
            md_parts.append(f"### {insight['dimension']}\n\n")
            md_parts.append(f"{insight['insight']}\n\n")
        
        return ''.join(md_parts)
    
    def _format_period_label(
        self, 
        review_type: str, 
        period_start: str, 
        period_end: str
    ) -> str:
        """格式化时间段标签"""
        start_date = datetime.fromisoformat(period_start)
        
        if review_type == 'monthly':
            return f"{start_date.year}年{start_date.month}月"
        else:
            return f"{start_date.year}年"
