# 记忆系统使用指南

## 概述

记忆回响项目的记忆系统分为两个部分：
1. **结构化记忆** - 存储明确的实体信息（如人名、事件、地点等）
2. **非结构化记忆** - 存储对话内容和用户表达的完整语义

## 结构化记忆

### 存储结构化记忆

```javascript
// 示例：存储关于家庭成员的信息
const familyMember = {
  entity_type: "family_member",
  entity_name: "外婆",
  attributes: {
    relationship: "外婆",
    age: 75,
    hobby: "织毛衣",
    memory: "小时候外婆教我织毛衣"
  }
};

// 发送POST请求到 /api/users/{user_id}/memories/structured
fetch(`/api/users/1/memories/structured`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(familyMember)
});
```

### 实体类型

常见的实体类型包括：
- `family_member` - 家庭成员
- `friend` - 朋友
- `event` - 重要事件
- `place` - 地点
- `achievement` - 成就
- `challenge` - 挑战

## 非结构化记忆

### 存储非结构化记忆

```javascript
// 示例：存储一段对话内容
const conversationMemory = {
  content: "今天和外婆聊起了她年轻时的故事，她说那时候生活虽然艰苦，但邻里之间都很和睦。",
  metadata: {
    topic: "家庭回忆",
    emotion: "温暖",
    date: "2023-04-15"
  }
};

// 发送POST请求到 /api/users/{user_id}/memories/unstructured
fetch(`/api/users/1/memories/unstructured`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(conversationMemory)
});
```

## 记忆检索

### 检索相关记忆

```javascript
// 示例：检索与"外婆"相关的记忆
fetch(`/api/users/1/memories/relevant?query=外婆`)
  .then(response => response.json())
  .then(data => {
    console.log("相关记忆:", data.memories);
  });
```

系统会根据语义相似度返回最相关的记忆内容。

## 最佳实践

1. **及时存储** - 在对话过程中及时识别和存储重要信息
2. **丰富属性** - 为结构化记忆添加尽可能多的相关属性
3. **情感标记** - 为记忆添加情感标签，有助于后续的回忆录生成
4. **定期整理** - 定期回顾和整理记忆库，确保信息的准确性和完整性

## 隐私保护

所有记忆数据都经过加密处理，并严格遵循隐私保护原则：
- 数据存储在用户指定的位置
- 敏感信息进行脱敏处理
- 用户可随时删除个人记忆数据