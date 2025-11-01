#!/bin/bash

# 启动脚本 for 记忆回响项目

echo "正在启动记忆回响项目..."

# 启动后端服务
echo "启动后端服务..."
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# 启动前端开发服务器
echo "启动前端开发服务器..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "项目已启动!"
echo "后端服务运行在: http://localhost:8000"
echo "前端界面运行在: http://localhost:3000"

# 等待所有后台进程
wait $BACKEND_PID
wait $FRONTEND_PID