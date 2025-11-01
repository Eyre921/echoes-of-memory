import React, { useState } from 'react'
import ChatPage from './pages/ChatPage'
import MemoriesPage from './pages/MemoriesPage'
import MemoirPage from './pages/MemoirPage'
import ReviewPage from './pages/ReviewPage'
import './styles/App.css'

function App() {
  const [currentPage, setCurrentPage] = useState('chat')

  return (
    <div className="app">
      <header className="app-header">
        <h1>记忆回响</h1>
        <nav>
          <button 
            className={currentPage === 'chat' ? 'active' : ''}
            onClick={() => setCurrentPage('chat')}
          >
            对话
          </button>
          <button 
            className={currentPage === 'memories' ? 'active' : ''}
            onClick={() => setCurrentPage('memories')}
          >
            我的记忆
          </button>
          <button 
            className={currentPage === 'review' ? 'active' : ''}
            onClick={() => setCurrentPage('review')}
          >
            时光回顾
          </button>
          <button 
            className={currentPage === 'memoir' ? 'active' : ''}
            onClick={() => setCurrentPage('memoir')}
          >
            回忆录
          </button>
        </nav>
      </header>
      
      <main className="app-main">
        {currentPage === 'chat' && <ChatPage />}
        {currentPage === 'memories' && <MemoriesPage />}
        {currentPage === 'review' && <ReviewPage />}
        {currentPage === 'memoir' && <MemoirPage />}
      </main>
      
      <footer className="app-footer">
        <p>记忆回响 - 人生回忆录AI助手</p>
      </footer>
    </div>
  )
}

export default App