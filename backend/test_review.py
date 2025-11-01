"""
回顾功能的单元测试
"""

import unittest
from datetime import datetime
from review_aggregator import DataAggregator, TimeRangeCalculator
from review_analyzer import (
    EmotionAnalyzer, 
    TopicExtractor, 
    EventExtractor,
    HighlightSelector,
    GrowthInsightGenerator
)


class TestTimeRangeCalculator(unittest.TestCase):
    """测试时间范围计算器"""
    
    def test_monthly_range(self):
        """测试月度时间范围计算"""
        start, end = TimeRangeCalculator.get_monthly_range(2024, 1)
        
        self.assertEqual(start.year, 2024)
        self.assertEqual(start.month, 1)
        self.assertEqual(start.day, 1)
        self.assertEqual(start.hour, 0)
        
        self.assertEqual(end.year, 2024)
        self.assertEqual(end.month, 1)
        self.assertEqual(end.day, 31)
        self.assertEqual(end.hour, 23)
        self.assertEqual(end.minute, 59)
    
    def test_monthly_range_december(self):
        """测试12月的时间范围计算"""
        start, end = TimeRangeCalculator.get_monthly_range(2024, 12)
        
        self.assertEqual(start.year, 2024)
        self.assertEqual(start.month, 12)
        self.assertEqual(start.day, 1)
        
        self.assertEqual(end.year, 2024)
        self.assertEqual(end.month, 12)
        self.assertEqual(end.day, 31)
    
    def test_annual_range(self):
        """测试年度时间范围计算"""
        start, end = TimeRangeCalculator.get_annual_range(2024)
        
        self.assertEqual(start.year, 2024)
        self.assertEqual(start.month, 1)
        self.assertEqual(start.day, 1)
        
        self.assertEqual(end.year, 2024)
        self.assertEqual(end.month, 12)
        self.assertEqual(end.day, 31)
    
    def test_format_period_label(self):
        """测试时间段标签格式化"""
        monthly_label = TimeRangeCalculator.format_period_label('monthly', 2024, 3)
        self.assertEqual(monthly_label, '2024年3月')
        
        annual_label = TimeRangeCalculator.format_period_label('annual', 2024)
        self.assertEqual(annual_label, '2024年')


class TestEmotionAnalyzer(unittest.TestCase):
    """测试情感分析器"""
    
    def setUp(self):
        self.analyzer = EmotionAnalyzer()
    
    def test_analyze_emotion_empty(self):
        """测试空消息列表的情感分析"""
        result = self.analyzer.analyze_emotion([])
        
        self.assertIn('overall_sentiment', result)
        self.assertIn('emotion_timeline', result)
        self.assertIn('emotion_trends', result)
    
    def test_analyze_emotion_positive(self):
        """测试正面情感分析"""
        messages = [
            {
                'role': 'user',
                'content': '今天很开心,很幸福',
                'timestamp': '2024-01-01T10:00:00'
            }
        ]
        
        result = self.analyzer.analyze_emotion(messages)
        
        self.assertEqual(len(result['emotion_timeline']), 1)
        self.assertGreater(result['emotion_timeline'][0]['sentiment_score'], 0)
    
    def test_analyze_emotion_negative(self):
        """测试负面情感分析"""
        messages = [
            {
                'role': 'user',
                'content': '今天很难过,很痛苦',
                'timestamp': '2024-01-01T10:00:00'
            }
        ]
        
        result = self.analyzer.analyze_emotion(messages)
        
        self.assertEqual(len(result['emotion_timeline']), 1)
        self.assertLess(result['emotion_timeline'][0]['sentiment_score'], 0)
    
    def test_calculate_sentiment_score(self):
        """测试情感分数计算"""
        messages = [
            {
                'role': 'user',
                'content': '今天很开心',
                'timestamp': '2024-01-01T10:00:00'
            }
        ]
        
        score = self.analyzer._calculate_sentiment_score(messages)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, -1)
        self.assertLessEqual(score, 1)


class TestTopicExtractor(unittest.TestCase):
    """测试主题提取器"""
    
    def setUp(self):
        self.extractor = TopicExtractor()
    
    def test_extract_topics_empty(self):
        """测试空消息的主题提取"""
        result = self.extractor.extract_topics([])
        self.assertEqual(len(result), 0)
    
    def test_extract_topics_family(self):
        """测试家庭主题提取"""
        messages = [
            {
                'role': 'user',
                'content': '今天和家人一起吃饭,爸爸妈妈都在',
                'timestamp': '2024-01-01T10:00:00'
            }
        ]
        
        result = self.extractor.extract_topics(messages)
        
        # 应该提取到家庭关系主题
        topic_names = [t['topic_name'] for t in result]
        self.assertIn('家庭关系', topic_names)
    
    def test_extract_topics_work(self):
        """测试职业主题提取"""
        messages = [
            {
                'role': 'user',
                'content': '今天在公司开会,讨论了新项目',
                'timestamp': '2024-01-01T10:00:00'
            }
        ]
        
        result = self.extractor.extract_topics(messages)
        
        topic_names = [t['topic_name'] for t in result]
        self.assertIn('职业发展', topic_names)
    
    def test_topic_weight_calculation(self):
        """测试主题权重计算"""
        messages = [
            {
                'role': 'user',
                'content': '今天和家人一起吃饭',
                'timestamp': '2024-01-01T10:00:00'
            },
            {
                'role': 'user',
                'content': '今天在公司工作',
                'timestamp': '2024-01-02T10:00:00'
            }
        ]
        
        result = self.extractor.extract_topics(messages)
        
        # 检查权重总和
        total_weight = sum(t['weight'] for t in result)
        self.assertAlmostEqual(total_weight, 1.0, places=2)


class TestEventExtractor(unittest.TestCase):
    """测试事件提取器"""
    
    def setUp(self):
        self.extractor = EventExtractor()
    
    def test_calculate_importance_score(self):
        """测试重要性评分计算"""
        message = {
            'id': 1,
            'role': 'user',
            'content': '今天是我第一次参加重要的面试,非常难忘',
            'timestamp': '2024-01-01T10:00:00'
        }
        
        emotion_timeline = [
            {
                'date': '2024-01-01',
                'sentiment_score': 0.8,
                'dominant_emotion': 'positive'
            }
        ]
        
        score = self.extractor._calculate_importance_score(message, emotion_timeline)
        
        self.assertGreater(score, 0)
        self.assertIsInstance(score, float)
    
    def test_extract_key_events(self):
        """测试关键事件提取"""
        messages = [
            {
                'id': 1,
                'role': 'user',
                'content': '今天是一个重要的日子,我完成了一个重要的项目',
                'timestamp': '2024-01-01T10:00:00'
            }
        ]
        
        emotion_timeline = [
            {
                'date': '2024-01-01',
                'sentiment_score': 0.8,
                'dominant_emotion': 'positive'
            }
        ]
        
        result = self.extractor.extract_key_events(
            messages, [], emotion_timeline, max_events=5
        )
        
        self.assertIsInstance(result, list)
        if len(result) > 0:
            self.assertIn('event_id', result[0])
            self.assertIn('title', result[0])
            self.assertIn('importance_score', result[0])


class TestHighlightSelector(unittest.TestCase):
    """测试亮点片段选择器"""
    
    def setUp(self):
        self.selector = HighlightSelector()
    
    def test_select_highlights(self):
        """测试亮点片段选择"""
        messages = []
        key_events = [
            {
                'event_id': 'msg_1',
                'title': '重要事件',
                'description': '这是一个重要的事件描述',
                'date': '2024-01-01',
                'emotion': 'positive'
            }
        ]
        
        result = self.selector.select_highlights(messages, key_events, max_highlights=3)
        
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 3)


class TestGrowthInsightGenerator(unittest.TestCase):
    """测试成长洞察生成器"""
    
    def setUp(self):
        self.generator = GrowthInsightGenerator()
    
    def test_generate_insights(self):
        """测试成长洞察生成"""
        messages = []
        emotion_analysis = {
            'overall_sentiment': {
                'positive': 0.7,
                'neutral': 0.2,
                'negative': 0.1
            },
            'emotion_trends': '整体积极'
        }
        topics = [
            {'topic_name': '家庭关系', 'weight': 0.5},
            {'topic_name': '职业发展', 'weight': 0.3},
            {'topic_name': '健康生活', 'weight': 0.2}
        ]
        statistics = {
            'active_days': 25,
            'total_conversations': 30
        }
        
        result = self.generator.generate_insights(
            messages, emotion_analysis, topics, statistics
        )
        
        self.assertIsInstance(result, list)
        if len(result) > 0:
            self.assertIn('dimension', result[0])
            self.assertIn('insight', result[0])


if __name__ == '__main__':
    unittest.main()
