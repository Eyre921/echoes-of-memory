"""
数据聚合层 - 负责收集指定时间范围内的记忆数据
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import Message, StructuredMemory, Conversation, get_db
import json


class DataAggregator:
    """数据聚合器 - 从多个数据源收集指定时间范围内的记忆数据"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def aggregate_review_data(
        self, 
        user_id: int, 
        period_start: datetime, 
        period_end: datetime
    ) -> Dict:
        """
        聚合回顾数据
        
        Args:
            user_id: 用户ID
            period_start: 起始时间
            period_end: 结束时间
            
        Returns:
            包含所有相关数据的字典
        """
        # 获取对话记录
        conversations = self._get_conversations(user_id, period_start, period_end)
        
        # 获取消息记录
        messages = self._get_messages(user_id, period_start, period_end)
        
        # 获取结构化记忆
        structured_memories = self._get_structured_memories(user_id, period_start, period_end)
        
        # 获取向量记忆 (暂时模拟,实际需要从ChromaDB查询)
        vector_memories = self._get_vector_memories(user_id, period_start, period_end)
        
        return {
            'user_id': user_id,
            'period_start': period_start,
            'period_end': period_end,
            'conversations': conversations,
            'messages': messages,
            'structured_memories': structured_memories,
            'vector_memories': vector_memories,
            'statistics': self._calculate_basic_statistics(
                conversations, messages, structured_memories
            )
        }
    
    def _get_conversations(
        self, 
        user_id: int, 
        period_start: datetime, 
        period_end: datetime
    ) -> List[Dict]:
        """查询对话记录"""
        conversations = self.db.query(Conversation).filter(
            Conversation.user_id == user_id,
            Conversation.created_at >= period_start,
            Conversation.created_at <= period_end
        ).order_by(Conversation.created_at.asc()).all()
        
        return [
            {
                'id': conv.id,
                'title': conv.title,
                'created_at': conv.created_at.isoformat(),
                'updated_at': conv.updated_at.isoformat()
            }
            for conv in conversations
        ]
    
    def _get_messages(
        self, 
        user_id: int, 
        period_start: datetime, 
        period_end: datetime
    ) -> List[Dict]:
        """查询消息记录"""
        # 首先获取该时间段内的所有对话ID
        conversation_ids = self.db.query(Conversation.id).filter(
            Conversation.user_id == user_id
        ).all()
        conversation_ids = [conv_id[0] for conv_id in conversation_ids]
        
        # 查询这些对话中在时间范围内的所有消息
        messages = self.db.query(Message).filter(
            Message.conversation_id.in_(conversation_ids),
            Message.timestamp >= period_start,
            Message.timestamp <= period_end
        ).order_by(Message.timestamp.asc()).all()
        
        return [
            {
                'id': msg.id,
                'conversation_id': msg.conversation_id,
                'content': msg.content,
                'role': msg.role,
                'timestamp': msg.timestamp.isoformat()
            }
            for msg in messages
        ]
    
    def _get_structured_memories(
        self, 
        user_id: int, 
        period_start: datetime, 
        period_end: datetime
    ) -> List[Dict]:
        """查询结构化记忆"""
        memories = self.db.query(StructuredMemory).filter(
            StructuredMemory.user_id == user_id,
            StructuredMemory.created_at >= period_start,
            StructuredMemory.created_at <= period_end
        ).all()
        
        return [
            {
                'id': mem.id,
                'entity_type': mem.entity_type,
                'entity_name': mem.entity_name,
                'attributes': json.loads(mem.attributes) if mem.attributes else {},
                'created_at': mem.created_at.isoformat()
            }
            for mem in memories
        ]
    
    def _get_vector_memories(
        self, 
        user_id: int, 
        period_start: datetime, 
        period_end: datetime
    ) -> List[Dict]:
        """
        查询向量记忆
        实际实现需要从ChromaDB中根据元数据筛选
        这里提供模拟实现
        """
        # TODO: 实际集成ChromaDB查询
        # 根据元数据中的user_id和timestamp筛选
        return []
    
    def _calculate_basic_statistics(
        self,
        conversations: List[Dict],
        messages: List[Dict],
        structured_memories: List[Dict]
    ) -> Dict:
        """计算基础统计数据"""
        # 计算活跃天数
        message_dates = set()
        for msg in messages:
            date = datetime.fromisoformat(msg['timestamp']).date()
            message_dates.add(date)
        
        # 计算用户消息和AI消息数量
        user_messages = [msg for msg in messages if msg['role'] == 'user']
        assistant_messages = [msg for msg in messages if msg['role'] == 'assistant']
        
        # 计算平均对话长度
        avg_conversation_length = 0
        if len(conversations) > 0:
            avg_conversation_length = len(messages) / len(conversations)
        
        return {
            'total_conversations': len(conversations),
            'total_messages': len(messages),
            'user_messages': len(user_messages),
            'assistant_messages': len(assistant_messages),
            'active_days': len(message_dates),
            'avg_conversation_length': round(avg_conversation_length, 2),
            'total_structured_memories': len(structured_memories)
        }


class TimeRangeCalculator:
    """时间范围计算器"""
    
    @staticmethod
    def get_monthly_range(year: int, month: int) -> tuple:
        """
        获取月度回顾的时间范围
        
        Args:
            year: 年份
            month: 月份 (1-12)
            
        Returns:
            (period_start, period_end) 时间范围元组
        """
        # 月份第一天 00:00:00
        period_start = datetime(year, month, 1, 0, 0, 0)
        
        # 计算月份最后一天
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        
        # 最后一天 23:59:59
        period_end = next_month - timedelta(seconds=1)
        
        return period_start, period_end
    
    @staticmethod
    def get_annual_range(year: int) -> tuple:
        """
        获取年度回顾的时间范围
        
        Args:
            year: 年份
            
        Returns:
            (period_start, period_end) 时间范围元组
        """
        # 1月1日 00:00:00
        period_start = datetime(year, 1, 1, 0, 0, 0)
        
        # 12月31日 23:59:59
        period_end = datetime(year, 12, 31, 23, 59, 59)
        
        return period_start, period_end
    
    @staticmethod
    def format_period_label(review_type: str, year: int, month: Optional[int] = None) -> str:
        """
        格式化时间段标签
        
        Args:
            review_type: 回顾类型 ('monthly' 或 'annual')
            year: 年份
            month: 月份 (月度回顾时必填)
            
        Returns:
            格式化的时间段标签
        """
        if review_type == 'monthly':
            return f"{year}年{month}月"
        elif review_type == 'annual':
            return f"{year}年"
        else:
            return f"{year}年"
