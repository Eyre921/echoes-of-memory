# 记忆回响 (Echoes of Memory)

## 项目简介

"记忆回响"是一个旨在通过日常对话，帮助用户记录、整理并最终生成一本个性化人生回忆录的AI伴侣。它不仅是一个聊天机器人，更是一位充满同理心、善于引导的倾听者和传记作家。

## 核心功能

1. **日常对话与记忆捕捉** - 通过温暖的对话引导用户分享人生故事
2. **长期记忆系统** - 安全存储和智能检索用户的个人记忆
3. **时光回顾** - 自动生成月度和年度回顾报告,智能分析情感变化和生活主题
4. **回忆录生成与编辑** - 自动生成个性化的回忆录初稿并支持编辑
5. **导出与分享** - 支持多种格式导出和个性化排版

## 技术架构

- 前端：React + TypeScript + Vite
- 后端：Python + FastAPI
- 数据库：PostgreSQL + ChromaDB
- AI模型：OpenAI GPT + Sentence-BERT

## 项目结构

```
echoes-of-memory/
├── backend/           # 后端服务
│   ├── main.py        # 主应用文件
│   ├── database.py    # 数据库模型和配置
│   ├── ai_core.py     # AI核心逻辑
│   ├── api.py         # API路由
│   ├── review_aggregator.py  # 回顾数据聚合
│   ├── review_analyzer.py    # 回顾AI分析引擎
│   ├── review_service.py     # 回顾生成服务
│   ├── review_api.py         # 回顾API接口
│   ├── test_review.py        # 回顾功能测试
│   ├── requirements.txt # Python依赖
│   └── .env           # 后端环境变量
├── frontend/          # 前端界面
│   ├── src/           # 源代码
│   │   ├── pages/     # 页面组件
│   │   │   ├── ReviewPage.jsx    # 回顾页面
│   │   │   └── ...
│   │   └── components/  # 通用组件
│   │       ├── ReviewSelector.jsx   # 时间选择器
│   │       ├── ReviewContent.jsx    # 回顾内容展示
│   │       ├── EmotionChart.jsx     # 情感曲线图
│   │       ├── TopicCloud.jsx       # 主题云图
│   │       └── ...
│   ├── package.json   # Node.js依赖
│   └── vite.config.js # Vite配置
├── docs/              # 文档
├── REVIEW_FEATURE_GUIDE.md  # 回顾功能使用指南
├── ai_models/         # AI模型文件
├── README.md          # 项目说明
├── .env.example       # 环境变量示例
└── start.sh           # 启动脚本
```

## 开发环境搭建

### 后端环境

1. 安装Python 3.8+
2. 安装依赖：
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. 配置环境变量：
   ```bash
   cp .env.example .env
   # 编辑.env文件，填入实际的API密钥和数据库连接信息
   ```

### 前端环境

1. 安装Node.js 16+
2. 安装依赖：
   ```bash
   cd frontend
   npm install
   ```

3. 配置环境变量：
   ```bash
   cp .env.example .env
   # 编辑.env文件，配置API地址
   ```

## 运行项目

### 手动启动

1. 启动后端服务：
   ```bash
   cd backend
   python main.py
   ```

2. 启动前端开发服务器：
   ```bash
   cd frontend
   npm run dev
   ```

### 使用启动脚本

```bash
./start.sh
```

## API文档

后端API文档可通过以下地址访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 特色功能详解

### 时光回顾功能

「记忆回响」提供了智能的时光回顾功能,帮助用户以时间维度重新审视人生轨迹:

- **月度回顾**: 每月自动生成回顾报告,分析当月的情感变化和生活主题
- **年度回顾**: 年末自动生成年度总结,识别重要时刻和成长轨迹
- **智能分析**:
  - 情感曲线分析:可视化展示情绪起伏
  - 主题分布统计:识别生活关注重点
  - 关键事件提取:智能筛选重要时刻
  - 成长洞察生成:AI发现行为模式变化
- **可视化展示**:
  - 情感曲线图(SVG折线图)
  - 主题云图(词云展示)
  - 统计数据面板
  - 事件时间线
- **导出分享**: 支持Markdown格式导出

详细使用指南请参考: [REVIEW_FEATURE_GUIDE.md](REVIEW_FEATURE_GUIDE.md)

## 数据库设置

1. 安装PostgreSQL
2. 创建数据库：
   ```sql
   CREATE DATABASE echoes_of_memory;
   ```

## 开发指南

### 代码规范

- Python代码遵循PEP 8规范
- JavaScript代码使用ESLint检查
- 提交代码前运行测试

### Git工作流

1. Fork仓库
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 部署

### 生产环境部署

1. 构建前端：
   ```bash
   cd frontend
   npm run build
   ```

2. 使用Docker部署（推荐）：
   ```bash
   docker-compose up -d
   ```

## 贡献

欢迎提交Issue和Pull Request来改进项目。

## 许可证

[MIT License](LICENSE)