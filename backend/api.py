# 简化版API路由文件

class SimpleRouter:
    def __init__(self, prefix=""):
        self.prefix = prefix
        self.routes = []
    
    def add_route(self, method, path, handler):
        self.routes.append((method, self.prefix + path, handler))

# 创建路由实例
api_router = SimpleRouter(prefix="/api")

# 健康检查端点
def health_check():
    return {"status": "ok"}

# 添加路由
api_router.add_route("GET", "/health", health_check)

# 模拟其他路由
def create_user():
    return {"message": "User created"}

def get_user(user_id):
    return {"user_id": user_id, "username": "testuser"}

api_router.add_route("POST", "/users", create_user)
api_router.add_route("GET", "/users/{user_id}", get_user)