import React from 'react'
import './EmotionChart.css'

function EmotionChart({ emotionTimeline }) {
  if (!emotionTimeline || emotionTimeline.length === 0) {
    return (
      <div className="emotion-chart empty">
        <p>暂无情感数据</p>
      </div>
    )
  }

  // 找出最大和最小值用于归一化
  const maxScore = 1
  const minScore = -1
  const range = maxScore - minScore

  // 计算图表高度和宽度
  const chartHeight = 200
  const chartWidth = 100 // 百分比

  // 生成SVG路径
  const generatePath = () => {
    const points = emotionTimeline.map((item, index) => {
      const x = (index / (emotionTimeline.length - 1)) * 100
      const normalizedScore = ((item.sentiment_score - minScore) / range) * 100
      const y = 100 - normalizedScore // 反转Y轴
      return `${x},${y}`
    })

    return `M ${points.join(' L ')}`
  }

  // 生成区域路径
  const generateAreaPath = () => {
    const points = emotionTimeline.map((item, index) => {
      const x = (index / (emotionTimeline.length - 1)) * 100
      const normalizedScore = ((item.sentiment_score - minScore) / range) * 100
      const y = 100 - normalizedScore
      return `${x},${y}`
    })

    return `M 0,100 L ${points.join(' L ')} L 100,100 Z`
  }

  // 获取情感颜色
  const getEmotionColor = (emotion) => {
    switch (emotion) {
      case 'positive':
        return '#4caf50'
      case 'negative':
        return '#ff9800'
      default:
        return '#9e9e9e'
    }
  }

  return (
    <div className="emotion-chart">
      <div className="chart-header">
        <h3>情感曲线</h3>
        <div className="chart-legend">
          <span className="legend-item positive">
            <span className="legend-dot"></span>
            正面
          </span>
          <span className="legend-item neutral">
            <span className="legend-dot"></span>
            中性
          </span>
          <span className="legend-item negative">
            <span className="legend-dot"></span>
            负面
          </span>
        </div>
      </div>

      <div className="chart-container">
        <svg
          viewBox="0 0 100 100"
          preserveAspectRatio="none"
          className="chart-svg"
        >
          {/* 背景网格线 */}
          <line x1="0" y1="50" x2="100" y2="50" className="grid-line" />
          <line x1="0" y1="25" x2="100" y2="25" className="grid-line-light" />
          <line x1="0" y1="75" x2="100" y2="75" className="grid-line-light" />

          {/* 区域填充 */}
          <path
            d={generateAreaPath()}
            className="chart-area"
          />

          {/* 曲线 */}
          <path
            d={generatePath()}
            className="chart-line"
          />

          {/* 数据点 */}
          {emotionTimeline.map((item, index) => {
            const x = (index / (emotionTimeline.length - 1)) * 100
            const normalizedScore = ((item.sentiment_score - minScore) / range) * 100
            const y = 100 - normalizedScore
            const color = getEmotionColor(item.dominant_emotion)

            return (
              <circle
                key={index}
                cx={x}
                cy={y}
                r="1.5"
                fill={color}
                className="chart-point"
              />
            )
          })}
        </svg>
      </div>

      <div className="chart-footer">
        <div className="date-labels">
          <span>{emotionTimeline[0]?.date}</span>
          <span>{emotionTimeline[emotionTimeline.length - 1]?.date}</span>
        </div>
      </div>
    </div>
  )
}

export default EmotionChart
