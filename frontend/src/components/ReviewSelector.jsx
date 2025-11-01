import React from 'react'
import './ReviewSelector.css'

function ReviewSelector({
  selectedType,
  selectedYear,
  selectedMonth,
  onTypeChange,
  onYearChange,
  onMonthChange,
  onGenerate,
  loading
}) {
  const currentYear = new Date().getFullYear()
  const currentMonth = new Date().getMonth()

  // 生成年份选项 (从2020年到当前年份)
  const yearOptions = []
  for (let year = currentYear; year >= 2020; year--) {
    yearOptions.push(year)
  }

  // 月份选项
  const monthOptions = [
    '一月', '二月', '三月', '四月', '五月', '六月',
    '七月', '八月', '九月', '十月', '十一月', '十二月'
  ]

  // 检查是否可以生成回顾 (不能为当前月份或当前年份)
  const canGenerate = () => {
    if (selectedType === 'monthly') {
      return selectedYear < currentYear || 
             (selectedYear === currentYear && selectedMonth < currentMonth)
    } else {
      return selectedYear < currentYear
    }
  }

  const handleQuickSelect = (type) => {
    const now = new Date()
    
    if (type === 'last-month') {
      const lastMonth = new Date(now.getFullYear(), now.getMonth() - 1)
      onTypeChange('monthly')
      onYearChange(lastMonth.getFullYear())
      onMonthChange(lastMonth.getMonth())
    } else if (type === 'this-month') {
      onTypeChange('monthly')
      onYearChange(now.getFullYear())
      onMonthChange(now.getMonth())
    } else if (type === 'last-year') {
      onTypeChange('annual')
      onYearChange(now.getFullYear() - 1)
    }
  }

  return (
    <div className="review-selector">
      <div className="selector-header">
        <h2>选择回顾时间</h2>
      </div>

      <div className="type-selector">
        <button
          className={selectedType === 'monthly' ? 'type-btn active' : 'type-btn'}
          onClick={() => onTypeChange('monthly')}
        >
          📅 月度回顾
        </button>
        <button
          className={selectedType === 'annual' ? 'type-btn active' : 'type-btn'}
          onClick={() => onTypeChange('annual')}
        >
          📆 年度回顾
        </button>
      </div>

      <div className="time-picker">
        <div className="picker-group">
          <label>年份</label>
          <select
            value={selectedYear}
            onChange={(e) => onYearChange(parseInt(e.target.value))}
            className="time-select"
          >
            {yearOptions.map(year => (
              <option key={year} value={year}>{year}年</option>
            ))}
          </select>
        </div>

        {selectedType === 'monthly' && (
          <div className="picker-group">
            <label>月份</label>
            <select
              value={selectedMonth}
              onChange={(e) => onMonthChange(parseInt(e.target.value))}
              className="time-select"
            >
              {monthOptions.map((month, index) => (
                <option key={index} value={index}>{month}</option>
              ))}
            </select>
          </div>
        )}
      </div>

      <div className="quick-select">
        <span className="quick-label">快捷选择:</span>
        <button
          className="quick-btn"
          onClick={() => handleQuickSelect('last-month')}
        >
          上月
        </button>
        <button
          className="quick-btn"
          onClick={() => handleQuickSelect('last-year')}
        >
          去年
        </button>
      </div>

      <div className="generate-section">
        <button
          className="generate-btn"
          onClick={onGenerate}
          disabled={!canGenerate() || loading}
        >
          {loading ? '生成中...' : '生成回顾'}
        </button>
        
        {!canGenerate() && (
          <p className="warning-text">
            ⚠️ 只能为已结束的时间段生成回顾
          </p>
        )}
      </div>
    </div>
  )
}

export default ReviewSelector
