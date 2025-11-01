import React from 'react'
import EmotionChart from './EmotionChart'
import TopicCloud from './TopicCloud'
import './ReviewContent.css'

function ReviewContent({ reviewData, onExport }) {
  const formatDate = (dateStr) => {
    const date = new Date(dateStr)
    return date.toLocaleDateString('zh-CN', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    })
  }

  const getPeriodLabel = () => {
    const start = new Date(reviewData.period_start)
    if (reviewData.review_type === 'monthly') {
      return `${start.getFullYear()}年${start.getMonth() + 1}月`
    } else {
      return `${start.getFullYear()}年`
    }
  }

  const getEmotionIcon = (emotion) => {
    switch (emotion) {
      case 'positive':
        return '😊'
      case 'negative':
        return '😔'
      default:
        return '😐'
    }
  }

  return (
    <div className="review-content">
      {/* 标题区域 */}
      <div className="content-header">
        <h2>{getPeriodLabel()}回顾</h2>
        <div className="header-actions">
          <button 
            className="export-btn"
            onClick={() => onExport('markdown')}
          >
            📥 导出Markdown
          </button>
        </div>
      </div>

      {/* 总结部分 */}
      <div className="summary-section">
        <h3>📝 总结</h3>
        <p className="summary-text">{reviewData.summary}</p>
      </div>

      {/* 统计面板 */}
      <div className="statistics-panel">
        <div className="stat-card">
          <div className="stat-icon">💬</div>
          <div className="stat-content">
            <div className="stat-value">{reviewData.statistics?.total_conversations || 0}</div>
            <div className="stat-label">对话次数</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📨</div>
          <div className="stat-content">
            <div className="stat-value">{reviewData.statistics?.total_messages || 0}</div>
            <div className="stat-label">消息数量</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📅</div>
          <div className="stat-content">
            <div className="stat-value">{reviewData.statistics?.active_days || 0}</div>
            <div className="stat-label">活跃天数</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💭</div>
          <div className="stat-content">
            <div className="stat-value">{reviewData.statistics?.total_structured_memories || 0}</div>
            <div className="stat-label">记忆片段</div>
          </div>
        </div>
      </div>

      {/* 情感分析 */}
      {reviewData.emotion_analysis && (
        <>
          <EmotionChart 
            emotionTimeline={reviewData.emotion_analysis.emotion_timeline} 
          />

          <div className="emotion-summary">
            <h3>情感分布</h3>
            <div className="emotion-bars">
              <div className="emotion-bar">
                <div className="bar-label">
                  <span>😊 正面</span>
                  <span>{Math.round((reviewData.emotion_analysis.overall_sentiment?.positive || 0) * 100)}%</span>
                </div>
                <div className="bar-track">
                  <div 
                    className="bar-fill positive"
                    style={{ width: `${(reviewData.emotion_analysis.overall_sentiment?.positive || 0) * 100}%` }}
                  ></div>
                </div>
              </div>

              <div className="emotion-bar">
                <div className="bar-label">
                  <span>😐 中性</span>
                  <span>{Math.round((reviewData.emotion_analysis.overall_sentiment?.neutral || 0) * 100)}%</span>
                </div>
                <div className="bar-track">
                  <div 
                    className="bar-fill neutral"
                    style={{ width: `${(reviewData.emotion_analysis.overall_sentiment?.neutral || 0) * 100}%` }}
                  ></div>
                </div>
              </div>

              <div className="emotion-bar">
                <div className="bar-label">
                  <span>😔 负面</span>
                  <span>{Math.round((reviewData.emotion_analysis.overall_sentiment?.negative || 0) * 100)}%</span>
                </div>
                <div className="bar-track">
                  <div 
                    className="bar-fill negative"
                    style={{ width: `${(reviewData.emotion_analysis.overall_sentiment?.negative || 0) * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
            <p className="emotion-trends">{reviewData.emotion_analysis.emotion_trends}</p>
          </div>
        </>
      )}

      {/* 主题分布 */}
      {reviewData.topics && <TopicCloud topics={reviewData.topics} />}

      {/* 关键事件 */}
      {reviewData.key_events && reviewData.key_events.length > 0 && (
        <div className="key-events-section">
          <h3>⭐ 关键事件</h3>
          <div className="events-timeline">
            {reviewData.key_events.map((event, index) => (
              <div key={index} className="event-card">
                <div className="event-date">{formatDate(event.date)}</div>
                <div className="event-content">
                  <div className="event-header">
                    <span className="event-emotion">{getEmotionIcon(event.emotion)}</span>
                    <h4 className="event-title">{event.title}</h4>
                    <span className="event-score">重要性: {event.importance_score}/10</span>
                  </div>
                  <p className="event-description">{event.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 亮点片段 */}
      {reviewData.highlights && reviewData.highlights.length > 0 && (
        <div className="highlights-section">
          <h3>✨ 亮点时刻</h3>
          <div className="highlights-gallery">
            {reviewData.highlights.map((highlight, index) => (
              <div key={index} className="highlight-card">
                <div className="highlight-header">
                  <span className="highlight-icon">{getEmotionIcon(highlight.emotion)}</span>
                  <span className="highlight-date">{formatDate(highlight.date)}</span>
                </div>
                <h4 className="highlight-title">{highlight.title}</h4>
                <p className="highlight-content">{highlight.content}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 成长洞察 */}
      {reviewData.growth_insights && reviewData.growth_insights.length > 0 && (
        <div className="insights-section">
          <h3>🌱 成长洞察</h3>
          {reviewData.growth_insights.map((insight, index) => (
            <div key={index} className="insight-card">
              <div className="insight-dimension">{insight.dimension}</div>
              <p className="insight-text">{insight.insight}</p>
              {insight.evidence && (
                <p className="insight-evidence">💡 {insight.evidence}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default ReviewContent
