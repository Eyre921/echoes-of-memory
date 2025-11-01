# 年度回顾和月度回顾功能 - 使用说明

## 功能概述

年度回顾和月度回顾功能是"记忆回响"系统的时间线回顾模块,通过智能分析用户在特定时间段内的对话记录和记忆数据,自动生成个性化的回顾报告。

## 目录结构

### 后端文件

```
backend/
├── database.py              # 数据库模型(新增Review模型)
├── review_aggregator.py     # 数据聚合层
├── review_analyzer.py       # AI分析引擎
├── review_service.py        # 回顾生成服务
├── review_api.py           # REST API接口
└── test_review.py          # 单元测试
```

### 前端文件

```
frontend/src/
├── pages/
│   ├── ReviewPage.jsx      # 回顾页面主组件
│   └── ReviewPage.css      # 回顾页面样式
└── components/
    ├── ReviewSelector.jsx   # 时间选择器组件
    ├── ReviewSelector.css   # 时间选择器样式
    ├── ReviewContent.jsx    # 回顾内容展示组件
    ├── ReviewContent.css    # 回顾内容样式
    ├── EmotionChart.jsx     # 情感曲线图组件
    ├── EmotionChart.css     # 情感曲线图样式
    ├── TopicCloud.jsx       # 主题云图组件
    └── TopicCloud.css       # 主题云图样式
```

## 后端使用指南

### 1. 数据库迁移

首先需要创建新的数据库表:

```python
from database import create_tables

# 创建所有表(包括新的Review表)
create_tables()
```

### 2. 使用回顾服务

```python
from database import get_db
from review_service import ReviewService

# 获取数据库会话
db = next(get_db())

# 创建服务实例
review_service = ReviewService(db)

# 生成月度回顾
monthly_review = review_service.generate_review(
    user_id=1,
    review_type='monthly',
    year=2024,
    month=10,
    regenerate=False
)

# 生成年度回顾
annual_review = review_service.generate_review(
    user_id=1,
    review_type='annual',
    year=2023,
    regenerate=False
)

# 查询回顾报告
review = review_service.get_review(review_id=1, user_id=1)

# 获取回顾列表
reviews = review_service.list_reviews(
    user_id=1,
    review_type='monthly',
    page=1,
    page_size=10
)

# 删除回顾
success = review_service.delete_review(review_id=1, user_id=1)
```

### 3. API接口集成

如果使用Flask:

```python
from flask import Flask, request, jsonify
from review_api import review_api, get_current_user_id

app = Flask(__name__)

# 生成回顾
@app.route('/api/reviews/generate', methods=['POST'])
def api_generate_review():
    user_id = get_current_user_id(request)
    request_data = request.get_json()
    result, status_code = review_api.generate_review(request_data, user_id)
    return jsonify(result), status_code

# 查询回顾
@app.route('/api/reviews/<int:review_id>', methods=['GET'])
def api_get_review(review_id):
    user_id = get_current_user_id(request)
    result, status_code = review_api.get_review(review_id, user_id)
    return jsonify(result), status_code

# 回顾列表
@app.route('/api/reviews', methods=['GET'])
def api_list_reviews():
    user_id = get_current_user_id(request)
    query_params = request.args.to_dict()
    result, status_code = review_api.list_reviews(query_params, user_id)
    return jsonify(result), status_code

# 删除回顾
@app.route('/api/reviews/<int:review_id>', methods=['DELETE'])
def api_delete_review(review_id):
    user_id = get_current_user_id(request)
    result, status_code = review_api.delete_review(review_id, user_id)
    return jsonify(result), status_code

# 导出回顾
@app.route('/api/reviews/<int:review_id>/export', methods=['GET'])
def api_export_review(review_id):
    user_id = get_current_user_id(request)
    query_params = request.args.to_dict()
    result, status_code = review_api.export_review(review_id, query_params, user_id)
    return jsonify(result), status_code
```

### 4. 运行单元测试

```bash
cd backend
python -m pytest test_review.py -v
```

或使用unittest:

```bash
python test_review.py
```

## 前端使用指南

### 1. 在应用中集成回顾页面

回顾页面已经集成到主应用中,通过导航按钮"时光回顾"访问。

### 2. 组件使用示例

#### ReviewSelector (时间选择器)

```jsx
import ReviewSelector from '../components/ReviewSelector'

<ReviewSelector
  selectedType="monthly"
  selectedYear={2024}
  selectedMonth={10}
  onTypeChange={setSelectedType}
  onYearChange={setSelectedYear}
  onMonthChange={setSelectedMonth}
  onGenerate={handleGenerateReview}
  loading={false}
/>
```

#### ReviewContent (回顾内容展示)

```jsx
import ReviewContent from '../components/ReviewContent'

<ReviewContent 
  reviewData={reviewData} 
  onExport={handleExport}
/>
```

#### EmotionChart (情感曲线图)

```jsx
import EmotionChart from '../components/EmotionChart'

<EmotionChart 
  emotionTimeline={reviewData.emotion_analysis.emotion_timeline} 
/>
```

#### TopicCloud (主题云图)

```jsx
import TopicCloud from '../components/TopicCloud'

<TopicCloud 
  topics={reviewData.topics} 
/>
```

### 3. API调用示例

```javascript
// 生成回顾
const generateReview = async (type, year, month) => {
  const response = await fetch('/api/reviews/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      review_type: type,
      year: year,
      month: month,
      regenerate: false
    })
  })
  
  const result = await response.json()
  return result
}

// 获取回顾详情
const getReview = async (reviewId) => {
  const response = await fetch(`/api/reviews/${reviewId}`)
  const result = await response.json()
  return result.data
}

// 导出回顾
const exportReview = async (reviewId, format) => {
  const response = await fetch(
    `/api/reviews/${reviewId}/export?format=${format}`
  )
  const result = await response.json()
  return result
}
```

## 核心功能说明

### 1. 数据聚合

- 自动收集指定时间范围内的对话记录
- 提取结构化记忆数据
- 统计基础数据指标

### 2. AI分析引擎

#### 情感分析
- 分析每日情感趋势
- 计算整体情感分布
- 生成情感变化描述

#### 主题提取
- 识别6大生活主题
- 计算主题权重和频次
- 提供主题分布可视化

#### 事件提取
- 基于重要性评分算法识别关键事件
- 评分维度:
  - 情感强度 (30%)
  - 关键词匹配 (40%)
  - 消息长度 (30%)

#### 亮点选择
- 从关键事件中筛选亮点片段
- 保留情感共鸣度高的对话

#### 成长洞察
- 行为习惯分析
- 情感状态评估
- 生活关注点识别

### 3. 可视化展示

- **情感曲线图**: SVG绘制的折线图,展示情感变化趋势
- **主题云图**: 词云风格展示,字体大小反映主题权重
- **统计面板**: 卡片式展示核心数据指标
- **事件时间线**: 按时间顺序展示关键事件

## 业务规则

### 生成限制

1. **时间限制**: 只能为已结束的时间段生成回顾
   - 月度回顾: 不能为当前月份生成
   - 年度回顾: 不能为当前年份生成

2. **数据量要求**:
   - 月度回顾: 建议至少5次对话,3条记忆
   - 年度回顾: 建议至少20次对话,10条记忆
   - 数据不足时仍可生成,但会有提示

3. **重新生成**: 同一时间段的回顾每24小时只允许重新生成一次

### 数据权限

- 回顾报告仅对所有者可见
- 删除回顾不影响原始对话和记忆数据
- 导出功能支持Markdown格式

## 扩展建议

### 短期优化
1. 增加周回顾功能
2. 优化情感分析准确性
3. 增加回顾对比功能

### 中期扩展
1. 支持自定义回顾周期
2. 引入多媒体元素(照片、音频)
3. 开发移动端原生应用

### 长期愿景
1. AI主动发现生活模式并提供建议
2. 支持多人共享回顾
3. AR/VR沉浸式回顾体验

## 故障排查

### 常见问题

1. **回顾生成失败**
   - 检查数据库连接
   - 确认时间范围是否有效
   - 验证用户是否有足够的数据

2. **情感分析结果异常**
   - 检查消息内容是否为空
   - 验证时间戳格式是否正确

3. **前端无法加载回顾**
   - 检查API端点是否正确
   - 验证用户认证token
   - 查看浏览器控制台错误

## 性能优化建议

1. **数据库索引**
   - 为Review表的user_id和period_start添加索引
   - 为Message表的timestamp添加索引

2. **缓存策略**
   - 使用Redis缓存已生成的回顾报告
   - 缓存过期时间设为24小时

3. **异步处理**
   - 对于大数据量用户,使用Celery等任务队列异步生成
   - 通过WebSocket推送生成进度

## 联系与支持

如有问题或建议,请通过以下方式联系:
- 提交GitHub Issue
- 发送邮件至项目维护者

## 许可证

本功能模块遵循主项目的开源许可证。
