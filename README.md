# 记忆回响 (Echoes of Memory)

## 项目简介

"记忆回响"是一个旨在通过日常对话，帮助用户记录、整理并最终生成一本个性化人生回忆录的AI伴侣。它不仅是一个聊天机器人，更是一位充满同理心、善于引导的倾听者和传记作家。

## 核心功能

1. **日常对话与记忆捕捉** - 通过温暖的对话引导用户分享人生故事
2. **长期记忆系统** - 安全存储和智能检索用户的个人记忆
3. **回忆录生成与编辑** - 自动生成个性化的回忆录初稿并支持编辑
4. **导出与分享** - 支持多种格式导出和个性化排版

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
│   ├── requirements.txt # Python依赖
│   └── .env           # 后端环境变量
├── frontend/          # 前端界面
│   ├── src/           # 源代码
│   ├── package.json   # Node.js依赖
│   └── vite.config.js # Vite配置
├── docs/              # 文档
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