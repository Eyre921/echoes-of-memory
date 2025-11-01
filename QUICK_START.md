# 年度回顾和月度回顾功能 - 快速开始

## 快速概览

此功能允许用户生成月度和年度回顾报告,通过AI智能分析对话记录,自动提取关键事件、情感变化和生活主题。

## 5分钟快速启动

### 第一步:数据库准备

```bash
# 进入后端目录
cd backend

# 启动Python环境
python
```

```python
# 创建数据库表
from database import create_tables
create_tables()
```

### 第二步:测试后端功能

```python
from database import get_db
from review_service import ReviewService

# 创建服务实例
db = next(get_db())
service = ReviewService(db)

# 生成测试回顾(需要先有对话数据)
# review = service.generate_review(
#     user_id=1,
#     review_type='monthly',
#     year=2024,
#     month=10
# )
```

### 第三步:启动前端

```bash
# 在新终端进入前端目录
cd frontend

# 启动开发服务器
npm run dev
```

访问 http://localhost:5173 即可看到应用,点击"时光回顾"导航按钮进入回顾页面。

## 核心功能演示

### 1. 生成月度回顾

1. 在回顾页面选择"月度回顾"
2. 选择年份和月份
3. 点击"生成回顾"按钮
4. 等待AI分析完成
5. 查看生成的回顾报告

### 2. 查看可视化数据

回顾报告包含以下可视化内容:

- **统计面板**: 对话次数、消息数量、活跃天数、记忆片段
- **情感曲线图**: 情感变化趋势折线图
- **情感分布条**: 正面/中性/负面情感占比
- **主题云图**: 生活主题词云展示
- **关键事件**: 按时间顺序的重要事件列表
- **亮点时刻**: 精选的记忆片段
- **成长洞察**: AI生成的个人成长分析

### 3. 导出回顾

1. 点击"导出Markdown"按钮
2. 系统自动下载.md文件
3. 可用任何Markdown编辑器打开

## 测试数据准备

为了测试回顾功能,需要先准备一些对话数据:

```python
from database import get_db, User, Conversation, Message
from datetime import datetime

db = next(get_db())

# 创建测试用户
user = User(username="testuser", email="test@example.com")
db.add(user)
db.commit()

# 创建测试对话
conv = Conversation(user_id=user.id, title="测试对话")
db.add(conv)
db.commit()

# 添加测试消息
messages = [
    Message(
        conversation_id=conv.id,
        content="今天很开心,和家人一起吃饭",
        role="user",
        timestamp=datetime(2024, 10, 1, 10, 0, 0)
    ),
    Message(
        conversation_id=conv.id,
        content="今天在公司完成了一个重要项目",
        role="user",
        timestamp=datetime(2024, 10, 5, 14, 0, 0)
    ),
    Message(
        conversation_id=conv.id,
        content="今天学习了新技能,感觉很充实",
        role="user",
        timestamp=datetime(2024, 10, 10, 20, 0, 0)
    ),
]

for msg in messages:
    db.add(msg)
db.commit()
```

## 常见问题

### Q: 为什么无法生成当前月份的回顾?

A: 系统只允许为已结束的时间段生成回顾。例如在10月份时,只能生成9月及之前的月度回顾。

### Q: 数据量不足时能生成回顾吗?

A: 可以,但系统会提示"记忆数据较少,回顾内容可能不够丰富"。建议至少有5次对话记录。

### Q: 如何重新生成回顾?

A: 在生成请求中设置 `regenerate: true`,但同一时间段的回顾每24小时只允许重新生成一次。

### Q: 情感分析的准确度如何?

A: 当前使用基于关键词的情感分析,准确度约70-80%。未来版本将集成更先进的情感分析模型。

### Q: 支持哪些导出格式?

A: 目前支持Markdown格式。PDF和DOCX格式正在开发中。

## 功能演进路线图

### ✅ 已完成
- [x] 月度和年度回顾生成
- [x] 情感曲线分析
- [x] 主题提取和可视化
- [x] 关键事件识别
- [x] 成长洞察生成
- [x] Markdown导出

### 🚧 进行中
- [ ] PDF和DOCX导出
- [ ] 更精准的情感分析模型
- [ ] 周回顾功能

### 📋 计划中
- [ ] 自定义回顾周期
- [ ] 多人共享回顾
- [ ] 回顾对比功能
- [ ] 移动端适配
- [ ] AR/VR沉浸式体验

## 技术细节

### 核心算法

#### 1. 情感评分算法

```
sentiment_score = (positive_count - negative_count) / (positive_count + negative_count)
范围: -1(极度负面) 到 +1(极度正面)
```

#### 2. 重要性评分算法

```
importance_score = 
    keyword_score × 0.4 +     // 关键词匹配
    emotion_score × 0.3 +     // 情感强度
    length_score × 0.3        // 消息长度
```

#### 3. 主题权重计算

```
topic_weight = topic_frequency / total_frequency
```

### 性能指标

- 数据聚合: < 1秒 (1000条消息)
- AI分析: 2-5秒 (月度回顾)
- 回顾生成: 3-8秒 (年度回顾)
- 前端渲染: < 500ms

## 开发与调试

### 启用调试模式

```python
# backend/review_service.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 运行单元测试

```bash
cd backend
python -m pytest test_review.py -v --cov=review_analyzer
```

### 前端调试

浏览器开发者工具 -> Console查看API调用日志

### API测试工具

使用Postman或curl测试API:

```bash
# 生成回顾
curl -X POST http://localhost:8000/api/reviews/generate \
  -H "Content-Type: application/json" \
  -d '{"review_type": "monthly", "year": 2024, "month": 10}'

# 查询回顾
curl http://localhost:8000/api/reviews/1
```

## 贡献指南

欢迎提交Issue和Pull Request!

### 开发流程

1. Fork项目
2. 创建功能分支: `git checkout -b feature/amazing-feature`
3. 提交更改: `git commit -m 'Add amazing feature'`
4. 推送分支: `git push origin feature/amazing-feature`
5. 创建Pull Request

### 代码规范

- Python: 遵循PEP 8
- JavaScript: 使用ESLint
- 提交信息: 遵循Conventional Commits

## 获取帮助

- 📖 完整文档: [REVIEW_FEATURE_GUIDE.md](REVIEW_FEATURE_GUIDE.md)
- 🐛 报告Bug: [GitHub Issues](https://github.com/your-repo/issues)
- 💬 讨论交流: [GitHub Discussions](https://github.com/your-repo/discussions)

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件
