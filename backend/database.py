from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/echoes_of_memory")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 用户模型
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联对话记录
    conversations = relationship("Conversation", back_populates="user")

# 对话记录模型
class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联用户
    user = relationship("User", back_populates="conversations")
    
    # 关联消息
    messages = relationship("Message", back_populates="conversation")

# 消息模型
class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    content = Column(Text)
    role = Column(String)  # 'user' 或 'assistant'
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # 关联对话
    conversation = relationship("Conversation", back_populates="messages")

# 结构化记忆模型
class StructuredMemory(Base):
    __tablename__ = "structured_memories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    entity_type = Column(String)  # 实体类型 (人物、地点、事件等)
    entity_name = Column(String)  # 实体名称
    attributes = Column(Text)     # 实体属性 (JSON格式)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联用户
    user = relationship("User")

# 创建数据库表
def create_tables():
    Base.metadata.create_all(bind=engine)

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()