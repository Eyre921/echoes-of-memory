"""
AI分析引擎 - 执行内容分析、主题提取、情感分析、亮点识别
"""

from typing import List, Dict, Optional
from datetime import datetime
from collections import Counter
import re
import json


class EmotionAnalyzer:
    """情感分析器"""
    
    # 情感关键词库
    POSITIVE_KEYWORDS = [
        '开心', '快乐', '高兴', '幸福', '喜欢', '爱', '感动', '温暖', 
        '美好', '满意', '舒服', '兴奋', '激动', '感谢', '欣慰', '骄傲'
    ]
    
    NEGATIVE_KEYWORDS = [
        '难过', '伤心', '痛苦', '悲伤', '焦虑', '担心', '害怕', '恐惧',
        '愤怒', '生气', '失望', '沮丧', '孤独', '疲惫', '压力', '烦躁'
    ]
    
    def analyze_emotion(self, messages: List[Dict]) -> Dict:
        """
        分析情感曲线
        
        Args:
            messages: 消息列表
            
        Returns:
            情感分析结果
        """
        # 按日期组织消息
        messages_by_date = self._group_messages_by_date(messages)
        
        # 生成情感时间线
        emotion_timeline = []
        for date, msgs in sorted(messages_by_date.items()):
            sentiment_score = self._calculate_sentiment_score(msgs)
            dominant_emotion = self._get_dominant_emotion(msgs)
            
            emotion_timeline.append({
                'date': date,
                'sentiment_score': sentiment_score,
                'dominant_emotion': dominant_emotion
            })
        
        # 计算整体情感分布
        overall_sentiment = self._calculate_overall_sentiment(emotion_timeline)
        
        # 生成情感趋势描述
        emotion_trends = self._generate_emotion_trends(emotion_timeline)
        
        return {
            'overall_sentiment': overall_sentiment,
            'emotion_timeline': emotion_timeline,
            'emotion_trends': emotion_trends
        }
    
    def _group_messages_by_date(self, messages: List[Dict]) -> Dict[str, List[Dict]]:
        """按日期组织消息"""
        messages_by_date = {}
        
        for msg in messages:
            if msg['role'] == 'user':  # 只分析用户消息
                date = datetime.fromisoformat(msg['timestamp']).date().isoformat()
                if date not in messages_by_date:
                    messages_by_date[date] = []
                messages_by_date[date].append(msg)
        
        return messages_by_date
    
    def _calculate_sentiment_score(self, messages: List[Dict]) -> float:
        """
        计算情感分数
        
        Returns:
            -1到1之间的分数,-1表示非常负面,1表示非常正面
        """
        total_score = 0
        
        for msg in messages:
            content = msg['content']
            
            # 统计正面和负面关键词
            positive_count = sum(1 for keyword in self.POSITIVE_KEYWORDS if keyword in content)
            negative_count = sum(1 for keyword in self.NEGATIVE_KEYWORDS if keyword in content)
            
            # 计算该消息的情感分数
            if positive_count + negative_count > 0:
                score = (positive_count - negative_count) / (positive_count + negative_count)
                total_score += score
        
        # 返回平均分数
        if len(messages) > 0:
            return round(total_score / len(messages), 2)
        return 0.0
    
    def _get_dominant_emotion(self, messages: List[Dict]) -> str:
        """识别主导情感"""
        emotion_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
        
        for msg in messages:
            content = msg['content']
            
            positive_count = sum(1 for keyword in self.POSITIVE_KEYWORDS if keyword in content)
            negative_count = sum(1 for keyword in self.NEGATIVE_KEYWORDS if keyword in content)
            
            if positive_count > negative_count:
                emotion_counts['positive'] += 1
            elif negative_count > positive_count:
                emotion_counts['negative'] += 1
            else:
                emotion_counts['neutral'] += 1
        
        # 返回占比最高的情感
        return max(emotion_counts, key=emotion_counts.get)
    
    def _calculate_overall_sentiment(self, emotion_timeline: List[Dict]) -> Dict:
        """计算整体情感分布"""
        positive_count = 0
        neutral_count = 0
        negative_count = 0
        
        for item in emotion_timeline:
            if item['dominant_emotion'] == 'positive':
                positive_count += 1
            elif item['dominant_emotion'] == 'negative':
                negative_count += 1
            else:
                neutral_count += 1
        
        total = len(emotion_timeline)
        if total == 0:
            return {'positive': 0, 'neutral': 0, 'negative': 0}
        
        return {
            'positive': round(positive_count / total, 2),
            'neutral': round(neutral_count / total, 2),
            'negative': round(negative_count / total, 2)
        }
    
    def _generate_emotion_trends(self, emotion_timeline: List[Dict]) -> str:
        """生成情感变化趋势描述"""
        if len(emotion_timeline) < 2:
            return "数据不足以分析情感趋势"
        
        # 计算前半段和后半段的平均情感分数
        mid = len(emotion_timeline) // 2
        first_half_avg = sum(item['sentiment_score'] for item in emotion_timeline[:mid]) / mid
        second_half_avg = sum(item['sentiment_score'] for item in emotion_timeline[mid:]) / (len(emotion_timeline) - mid)
        
        # 生成趋势描述
        if second_half_avg > first_half_avg + 0.2:
            return "情感整体呈现上升趋势,后期情绪更加积极"
        elif second_half_avg < first_half_avg - 0.2:
            return "情感整体呈现下降趋势,需要关注情绪变化"
        else:
            return "情感相对稳定,没有明显的波动"


class TopicExtractor:
    """主题提取器"""
    
    # 预定义主题库
    TOPIC_LIBRARY = {
        '家庭关系': ['家人', '父母', '孩子', '爸爸', '妈妈', '家庭', '亲子', '夫妻', '长辈'],
        '职业发展': ['工作', '职业', '公司', '同事', '老板', '项目', '业绩', '升职', '技能'],
        '健康生活': ['健康', '运动', '锻炼', '饮食', '睡眠', '医生', '身体', '养生'],
        '兴趣爱好': ['旅行', '阅读', '音乐', '电影', '美食', '摄影', '画画', '运动'],
        '社交关系': ['朋友', '聚会', '社交', '关系', '人际', '交流'],
        '个人成长': ['学习', '成长', '反思', '目标', '习惯', '改变', '进步']
    }
    
    def extract_topics(self, messages: List[Dict]) -> List[Dict]:
        """
        提取主题标签
        
        Args:
            messages: 消息列表
            
        Returns:
            主题列表,包含主题名称、权重、频次等信息
        """
        # 统计主题出现次数
        topic_counts = {topic: 0 for topic in self.TOPIC_LIBRARY.keys()}
        topic_dates = {topic: set() for topic in self.TOPIC_LIBRARY.keys()}
        
        for msg in messages:
            if msg['role'] == 'user':
                content = msg['content']
                date = datetime.fromisoformat(msg['timestamp']).date().isoformat()
                
                for topic, keywords in self.TOPIC_LIBRARY.items():
                    for keyword in keywords:
                        if keyword in content:
                            topic_counts[topic] += 1
                            topic_dates[topic].add(date)
                            break
        
        # 计算总出现次数
        total_count = sum(topic_counts.values())
        
        # 生成主题列表
        topics = []
        for topic, count in topic_counts.items():
            if count > 0:
                weight = count / total_count if total_count > 0 else 0
                topics.append({
                    'topic_name': topic,
                    'weight': round(weight, 3),
                    'frequency': count,
                    'related_dates': sorted(list(topic_dates[topic])),
                    'description': f"在这段时间里,您{count}次提到了与{topic}相关的内容"
                })
        
        # 按权重降序排序
        topics.sort(key=lambda x: x['weight'], reverse=True)
        
        return topics
    
    def extract_keywords(self, messages: List[Dict], top_k: int = 10) -> List[Dict]:
        """
        提取高频关键词
        
        Args:
            messages: 消息列表
            top_k: 返回前k个关键词
            
        Returns:
            关键词列表
        """
        # 提取所有用户消息的内容
        all_text = ' '.join([msg['content'] for msg in messages if msg['role'] == 'user'])
        
        # 简单的分词(实际应用中应使用jieba等专业分词工具)
        words = re.findall(r'[\u4e00-\u9fa5]+', all_text)
        
        # 过滤停用词和短词
        words = [word for word in words if len(word) >= 2]
        
        # 统计词频
        word_counts = Counter(words)
        
        # 返回前k个关键词
        top_keywords = word_counts.most_common(top_k)
        
        return [
            {'keyword': word, 'frequency': count}
            for word, count in top_keywords
        ]


class EventExtractor:
    """事件提取器"""
    
    # 重要性关键词
    IMPORTANCE_KEYWORDS = [
        '第一次', '重要', '难忘', '转折', '关键', '特别', '印象深刻',
        '决定', '改变', '突破', '成就', '里程碑', '纪念'
    ]
    
    def extract_key_events(
        self, 
        messages: List[Dict], 
        structured_memories: List[Dict],
        emotion_timeline: List[Dict],
        max_events: int = 10
    ) -> List[Dict]:
        """
        提取关键事件
        
        Args:
            messages: 消息列表
            structured_memories: 结构化记忆列表
            emotion_timeline: 情感时间线
            max_events: 最大事件数量
            
        Returns:
            关键事件列表
        """
        candidate_events = []
        
        # 从消息中提取候选事件
        for msg in messages:
            if msg['role'] == 'user' and len(msg['content']) > 20:
                importance_score = self._calculate_importance_score(
                    msg, emotion_timeline
                )
                
                if importance_score > 0:
                    candidate_events.append({
                        'event_id': f"msg_{msg['id']}",
                        'title': self._generate_event_title(msg['content']),
                        'date': datetime.fromisoformat(msg['timestamp']).date().isoformat(),
                        'description': msg['content'][:200] + '...' if len(msg['content']) > 200 else msg['content'],
                        'importance_score': importance_score,
                        'emotion': self._get_message_emotion(msg),
                        'related_memories': [msg['id']]
                    })
        
        # 从结构化记忆中提取重要事件
        for memory in structured_memories:
            if memory['entity_type'] == '事件':
                candidate_events.append({
                    'event_id': f"mem_{memory['id']}",
                    'title': memory['entity_name'],
                    'date': datetime.fromisoformat(memory['created_at']).date().isoformat(),
                    'description': str(memory['attributes']),
                    'importance_score': 5.0,  # 结构化记忆默认重要性较高
                    'emotion': 'neutral',
                    'related_memories': [memory['id']]
                })
        
        # 按重要性评分排序
        candidate_events.sort(key=lambda x: x['importance_score'], reverse=True)
        
        # 返回前max_events个事件
        return candidate_events[:max_events]
    
    def _calculate_importance_score(
        self, 
        message: Dict, 
        emotion_timeline: List[Dict]
    ) -> float:
        """
        计算重要性评分
        
        评分算法:
        - 情感强度权重: 30%
        - 关键词匹配权重: 40%
        - 消息长度权重: 30%
        """
        content = message['content']
        
        # 关键词匹配得分
        keyword_score = sum(3 for keyword in self.IMPORTANCE_KEYWORDS if keyword in content)
        
        # 情感强度得分
        emotion_score = 0
        msg_date = datetime.fromisoformat(message['timestamp']).date().isoformat()
        for item in emotion_timeline:
            if item['date'] == msg_date:
                emotion_score = abs(item['sentiment_score']) * 5
                break
        
        # 消息长度得分 (归一化到0-5)
        length_score = min(len(content) / 100, 5)
        
        # 综合评分
        total_score = keyword_score * 0.4 + emotion_score * 0.3 + length_score * 0.3
        
        return round(total_score, 2)
    
    def _generate_event_title(self, content: str) -> str:
        """生成事件标题"""
        # 简单实现:取前30个字符作为标题
        title = content[:30]
        if len(content) > 30:
            title += '...'
        return title
    
    def _get_message_emotion(self, message: Dict) -> str:
        """获取消息的情感色彩"""
        content = message['content']
        
        positive_keywords = ['开心', '快乐', '高兴', '幸福', '喜欢']
        negative_keywords = ['难过', '伤心', '痛苦', '悲伤', '焦虑']
        
        positive_count = sum(1 for keyword in positive_keywords if keyword in content)
        negative_count = sum(1 for keyword in negative_keywords if keyword in content)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'


class HighlightSelector:
    """亮点片段选择器"""
    
    def select_highlights(
        self, 
        messages: List[Dict], 
        key_events: List[Dict],
        max_highlights: int = 5
    ) -> List[Dict]:
        """
        选择亮点片段
        
        Args:
            messages: 消息列表
            key_events: 关键事件列表
            max_highlights: 最大亮点数量
            
        Returns:
            亮点片段列表
        """
        highlights = []
        
        # 从关键事件中选择部分作为亮点
        for event in key_events[:max_highlights]:
            if event['event_id'].startswith('msg_'):
                highlights.append({
                    'id': event['event_id'],
                    'title': event['title'],
                    'content': event['description'],
                    'date': event['date'],
                    'emotion': event['emotion']
                })
        
        return highlights


class GrowthInsightGenerator:
    """成长洞察生成器"""
    
    def generate_insights(
        self,
        messages: List[Dict],
        emotion_analysis: Dict,
        topics: List[Dict],
        statistics: Dict
    ) -> List[Dict]:
        """
        生成成长洞察
        
        Args:
            messages: 消息列表
            emotion_analysis: 情感分析结果
            topics: 主题列表
            statistics: 统计数据
            
        Returns:
            成长洞察列表
        """
        insights = []
        
        # 活跃度洞察
        if statistics.get('active_days', 0) > 20:
            insights.append({
                'dimension': '行为习惯',
                'insight': f"在这段时间里,您有{statistics['active_days']}天与我进行了对话,展现出良好的记录习惯。",
                'evidence': f"总共进行了{statistics['total_conversations']}次对话"
            })
        
        # 情感洞察
        overall_sentiment = emotion_analysis.get('overall_sentiment', {})
        if overall_sentiment.get('positive', 0) > 0.6:
            insights.append({
                'dimension': '情感状态',
                'insight': f"您的整体情绪状态较为积极,正面情感占比达到{int(overall_sentiment['positive'] * 100)}%。",
                'evidence': emotion_analysis.get('emotion_trends', '')
            })
        
        # 主题多样性洞察
        if len(topics) >= 3:
            top_topics = [t['topic_name'] for t in topics[:3]]
            insights.append({
                'dimension': '生活关注点',
                'insight': f"您最关注的生活领域是:{', '.join(top_topics)},展现出平衡的生活态度。",
                'evidence': f"共涉及{len(topics)}个不同的生活主题"
            })
        
        return insights


class ReviewAnalyzer:
    """回顾分析器 - 整合所有分析功能"""
    
    def __init__(self):
        self.emotion_analyzer = EmotionAnalyzer()
        self.topic_extractor = TopicExtractor()
        self.event_extractor = EventExtractor()
        self.highlight_selector = HighlightSelector()
        self.insight_generator = GrowthInsightGenerator()
    
    def analyze(self, aggregated_data: Dict, review_type: str) -> Dict:
        """
        执行完整的回顾分析
        
        Args:
            aggregated_data: 聚合的数据
            review_type: 回顾类型 ('monthly' 或 'annual')
            
        Returns:
            分析结果
        """
        messages = aggregated_data['messages']
        structured_memories = aggregated_data['structured_memories']
        statistics = aggregated_data['statistics']
        
        # 情感分析
        emotion_analysis = self.emotion_analyzer.analyze_emotion(messages)
        
        # 主题提取
        topics = self.topic_extractor.extract_topics(messages)
        
        # 关键事件提取
        max_events = 10 if review_type == 'annual' else 5
        key_events = self.event_extractor.extract_key_events(
            messages, 
            structured_memories, 
            emotion_analysis['emotion_timeline'],
            max_events
        )
        
        # 亮点片段选择
        max_highlights = 12 if review_type == 'annual' else 5
        highlights = self.highlight_selector.select_highlights(
            messages, 
            key_events, 
            max_highlights
        )
        
        # 成长洞察生成
        growth_insights = self.insight_generator.generate_insights(
            messages, 
            emotion_analysis, 
            topics, 
            statistics
        )
        
        # 生成总结
        summary = self._generate_summary(
            review_type, 
            statistics, 
            emotion_analysis, 
            topics
        )
        
        # 准备可视化数据
        visualization_data = self._prepare_visualization_data(
            emotion_analysis, 
            topics, 
            key_events
        )
        
        return {
            'summary': summary,
            'key_events': key_events,
            'emotion_analysis': emotion_analysis,
            'topics': topics,
            'highlights': highlights,
            'growth_insights': growth_insights,
            'visualization_data': visualization_data
        }
    
    def _generate_summary(
        self, 
        review_type: str, 
        statistics: Dict, 
        emotion_analysis: Dict, 
        topics: List[Dict]
    ) -> str:
        """生成总结性描述"""
        period_name = "这个月" if review_type == 'monthly' else "这一年"
        
        # 构建总结文本
        summary_parts = []
        
        # 活跃度描述
        summary_parts.append(
            f"{period_name},您与我进行了{statistics['total_conversations']}次对话,"
            f"分享了{statistics['total_messages']}条消息。"
        )
        
        # 情感描述
        overall_sentiment = emotion_analysis.get('overall_sentiment', {})
        if overall_sentiment.get('positive', 0) > 0.5:
            summary_parts.append("您的整体心情较为积极乐观。")
        elif overall_sentiment.get('negative', 0) > 0.5:
            summary_parts.append("您经历了一些挑战,希望未来会更好。")
        else:
            summary_parts.append("您的情绪相对平稳。")
        
        # 主题描述
        if topics:
            top_topic = topics[0]['topic_name']
            summary_parts.append(f"您最关注的是{top_topic}相关的内容。")
        
        return ' '.join(summary_parts)
    
    def _prepare_visualization_data(
        self, 
        emotion_analysis: Dict, 
        topics: List[Dict], 
        key_events: List[Dict]
    ) -> Dict:
        """准备可视化数据"""
        return {
            'emotion_chart': {
                'type': 'line',
                'data': emotion_analysis['emotion_timeline']
            },
            'topic_cloud': {
                'type': 'wordcloud',
                'data': [
                    {'name': t['topic_name'], 'value': t['weight']}
                    for t in topics
                ]
            },
            'event_timeline': {
                'type': 'timeline',
                'data': [
                    {'date': e['date'], 'title': e['title'], 'score': e['importance_score']}
                    for e in key_events
                ]
            }
        }
