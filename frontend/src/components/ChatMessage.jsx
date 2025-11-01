import React from 'react'
import './ChatMessage.css'

function ChatMessage({ message }) {
  const isUser = message.role === 'user'
  
  return (
    <div className={`chat-message ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-content">
        <p>{message.content}</p>
        <span className="timestamp">
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>
    </div>
  )
}

export default ChatMessage