import React, { useState, useEffect } from 'react'
import ReviewSelector from '../components/ReviewSelector'
import ReviewContent from '../components/ReviewContent'
import './ReviewPage.css'

function ReviewPage() {
  const [selectedType, setSelectedType] = useState('monthly')
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear())
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth())
  const [reviewData, setReviewData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleGenerateReview = async () => {
    setLoading(true)
    setError(null)

    try {
      const requestBody = {
        review_type: selectedType,
        year: selectedYear,
        month: selectedType === 'monthly' ? selectedMonth + 1 : null,
        regenerate: false
      }

      const response = await fetch('/api/reviews/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      })

      const result = await response.json()

      if (result.success) {
        // 生成成功后加载回顾数据
        await loadReviewData(result.review_id)
      } else {
        setError(result.message || '生成回顾失败')
      }
    } catch (err) {
      setError('网络错误: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const loadReviewData = async (reviewId) => {
    try {
      const response = await fetch(`/api/reviews/${reviewId}`)
      const result = await response.json()

      if (result.success) {
        setReviewData(result.data)
      } else {
        setError(result.message || '加载回顾数据失败')
      }
    } catch (err) {
      setError('加载数据失败: ' + err.message)
    }
  }

  const handleExport = async (format) => {
    if (!reviewData) return

    try {
      const response = await fetch(
        `/api/reviews/${reviewData.review_id}/export?format=${format}`
      )
      const result = await response.json()

      if (result.success && format === 'markdown') {
        // 下载Markdown文件
        const blob = new Blob([result.content], { type: 'text/markdown' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = result.filename
        a.click()
        URL.revokeObjectURL(url)
      } else {
        alert(result.message || '导出失败')
      }
    } catch (err) {
      alert('导出失败: ' + err.message)
    }
  }

  return (
    <div className="review-page">
      <div className="review-header">
        <h1>时光回顾</h1>
        <p>回顾您的记忆轨迹,发现生活的美好瞬间</p>
      </div>

      <ReviewSelector
        selectedType={selectedType}
        selectedYear={selectedYear}
        selectedMonth={selectedMonth}
        onTypeChange={setSelectedType}
        onYearChange={setSelectedYear}
        onMonthChange={setSelectedMonth}
        onGenerate={handleGenerateReview}
        loading={loading}
      />

      {error && (
        <div className="review-error">
          <p>⚠️ {error}</p>
        </div>
      )}

      {loading && (
        <div className="review-loading">
          <div className="spinner"></div>
          <p>正在生成回顾报告,请稍候...</p>
        </div>
      )}

      {reviewData && !loading && (
        <ReviewContent 
          reviewData={reviewData} 
          onExport={handleExport}
        />
      )}
    </div>
  )
}

export default ReviewPage
