import React from 'react'
import './TopicCloud.css'

function TopicCloud({ topics }) {
  if (!topics || topics.length === 0) {
    return (
      <div className="topic-cloud empty">
        <p>暂无主题数据</p>
      </div>
    )
  }

  // 计算字体大小 (基于权重)
  const getFontSize = (weight) => {
    const minSize = 0.9
    const maxSize = 2.5
    return minSize + weight * (maxSize - minSize)
  }

  // 获取主题颜色
  const getTopicColor = (index) => {
    const colors = [
      '#667eea',
      '#764ba2',
      '#f093fb',
      '#4facfe',
      '#43e97b',
      '#fa709a',
      '#fee140',
      '#30cfd0'
    ]
    return colors[index % colors.length]
  }

  // 获取主题图标
  const getTopicIcon = (topicName) => {
    const iconMap = {
      '家庭关系': '👨‍👩‍👧‍👦',
      '职业发展': '💼',
      '健康生活': '🏃',
      '兴趣爱好': '🎨',
      '社交关系': '👥',
      '个人成长': '🌱'
    }
    return iconMap[topicName] || '📌'
  }

  return (
    <div className="topic-cloud">
      <div className="cloud-header">
        <h3>主题分布</h3>
        <p className="cloud-subtitle">您在这段时间关注的生活主题</p>
      </div>

      <div className="cloud-container">
        {topics.map((topic, index) => (
          <div
            key={index}
            className="topic-item"
            style={{
              fontSize: `${getFontSize(topic.weight)}em`,
              color: getTopicColor(index)
            }}
          >
            <span className="topic-icon">{getTopicIcon(topic.topic_name)}</span>
            <span className="topic-name">{topic.topic_name}</span>
            <span className="topic-count">({topic.frequency})</span>
          </div>
        ))}
      </div>

      <div className="cloud-details">
        {topics.slice(0, 3).map((topic, index) => (
          <div key={index} className="detail-item">
            <div className="detail-header">
              <span className="detail-icon">{getTopicIcon(topic.topic_name)}</span>
              <span className="detail-name">{topic.topic_name}</span>
              <span className="detail-badge">{Math.round(topic.weight * 100)}%</span>
            </div>
            <p className="detail-description">{topic.description}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default TopicCloud
