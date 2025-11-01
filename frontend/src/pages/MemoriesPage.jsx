import React, { useState, useEffect } from 'react'
import './MemoriesPage.css'

function MemoriesPage() {
  const [memories, setMemories] = useState([
    {
      id: 1,
      type: 'family_member',
      name: '外婆',
      attributes: {
        relationship: '外婆',
        hobby: '织毛衣',
        memory: '小时候外婆教我织毛衣'
      },
      date: '2023-04-15'
    },
    {
      id: 2,
      type: 'event',
      name: '大学毕业',
      attributes: {
        year: 2010,
        achievement: '计算机科学学士',
        feeling: '兴奋和不舍'
      },
      date: '2023-04-10'
    }
  ])

  return (
    <div className="memories-page">
      <h2>我的记忆库</h2>
      <div className="memories-container">
        {memories.map(memory => (
          <div key={memory.id} className="memory-card">
            <h3>{memory.name}</h3>
            <p><strong>类型:</strong> {memory.type}</p>
            <div className="memory-attributes">
              {Object.entries(memory.attributes).map(([key, value]) => (
                <p key={key}><strong>{key}:</strong> {value}</p>
              ))}
            </div>
            <p className="memory-date">{memory.date}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default MemoriesPage