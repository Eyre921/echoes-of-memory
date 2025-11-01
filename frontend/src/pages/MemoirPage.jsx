import React, { useState } from 'react'
import './MemoirPage.css'

function MemoirPage() {
  const [memoirContent, setMemoirContent] = useState(`
# 我的人生回忆录

## 第一章：童年时光

这是我童年的故事。那时候生活虽然简单，但充满了快乐和温暖。我记得小时候最喜欢和外婆一起度过下午时光，她会教我织毛衣，给我讲她年轻时的故事。

## 第二章：求学岁月

求学时期是我人生中重要的阶段。我努力学习，遇到了很多好老师和好朋友。大学四年，我不仅学到了知识，更重要的是学会了如何思考和成长。

## 第三章：初入社会

刚进入社会时，我面临着很多挑战。工作中的压力让我一度感到迷茫，但通过不断学习和努力，我逐渐找到了自己的方向。
  `)

  const [isGenerating, setIsGenerating] = useState(false)

  const generateMemoir = () => {
    setIsGenerating(true)
    // 模拟生成过程
    setTimeout(() => {
      setMemoirContent(`
# 我的人生回忆录（更新版）

## 第一章：童年时光

这是我童年的故事。那时候生活虽然简单，但充满了快乐和温暖。我记得小时候最喜欢和外婆一起度过下午时光，她会教我织毛衣，给我讲她年轻时的故事。

## 第二章：求学岁月

求学时期是我人生中重要的阶段。我努力学习，遇到了很多好老师和好朋友。大学四年，我不仅学到了知识，更重要的是学会了如何思考和成长。

## 第三章：初入社会

刚进入社会时，我面临着很多挑战。工作中的压力让我一度感到迷茫，但通过不断学习和努力，我逐渐找到了自己的方向。

## 第四章：家庭生活

成家立业后，我体会到了责任的重要性。与伴侣共同经营家庭，养育孩子，这些经历让我变得更加成熟和有担当。

## 第五章：人生感悟

回顾过往，我深深感受到人生的美好和不易。每一个阶段都有其独特的价值和意义，正是这些经历塑造了今天的我。
      `)
      setIsGenerating(false)
    }, 2000)
  }

  return (
    <div className="memoir-page">
      <div className="memoir-header">
        <h2>我的回忆录</h2>
        <button 
          onClick={generateMemoir} 
          disabled={isGenerating}
          className="generate-button"
        >
          {isGenerating ? '生成中...' : '重新生成'}
        </button>
      </div>
      
      <div className="memoir-content">
        <textarea
          value={memoirContent}
          onChange={(e) => setMemoirContent(e.target.value)}
          rows={25}
        />
      </div>
      
      <div className="memoir-actions">
        <button className="export-button">导出为PDF</button>
        <button className="export-button">导出为Word</button>
        <button className="export-button">导出为EPUB</button>
      </div>
    </div>
  )
}

export default MemoirPage