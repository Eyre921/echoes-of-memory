import React, { useState, useRef, useEffect } from 'react'
import ChatMessage from '../components/ChatMessage'
import './ChatPage.css'

function ChatPage() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      content: "你好！我是你的记忆回响AI助手。今天过得怎么样？有什么想聊的吗？",
      role: "assistant",
      timestamp: new Date()
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = () => {
    if (inputValue.trim() === '') return

    // 添加用户消息
    const userMessage = {
      id: messages.length + 1,
      content: inputValue,
      role: "user",
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')

    // 模拟AI回复
    setTimeout(() => {
      const aiMessage = {
        id: messages.length + 2,
        content: `感谢你分享关于"${inputValue.substring(0, 20)}..."的内容。这听起来很有趣！能告诉我更多细节吗？`,
        role: "assistant",
        timestamp: new Date()
      }
      setMessages(prev => [...prev, aiMessage])
    }, 1000)
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="chat-page">
      <div className="chat-container">
        <div className="chat-messages">
          {messages.map(message => (
            <ChatMessage key={message.id} message={message} />
          ))}
          <div ref={messagesEndRef} />
        </div>
        
        <div className="chat-input-container">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="输入消息..."
            rows="3"
          />
          <button onClick={handleSend} disabled={inputValue.trim() === ''}>
            发送
          </button>
        </div>
      </div>
    </div>
  )
}

export default ChatPage