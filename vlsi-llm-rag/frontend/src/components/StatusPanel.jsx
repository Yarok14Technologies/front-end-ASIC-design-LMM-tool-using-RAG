import React from 'react'
import { AlertCircle, CheckCircle, Clock, Info } from 'lucide-react'

const StatusPanel = ({ status, message, type = 'info' }) => {
  const getIcon = () => {
    switch (type) {
      case 'success':
        return <CheckCircle size={20} color="#10b981" />
      case 'error':
        return <AlertCircle size={20} color="#ef4444" />
      case 'warning':
        return <AlertCircle size={20} color="#f59e0b" />
      case 'loading':
        return <Clock size={20} color="#3b82f6" />
      default:
        return <Info size={20} color="#3b82f6" />
    }
  }

  return (
    <div className={`status-panel status-${type}`}>
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
        {getIcon()}
        <div>
          <strong style={{ display: 'block', marginBottom: '0.25rem' }}>
            {status}
          </strong>
          <div style={{ color: '#cbd5e1', fontSize: '0.9rem' }}>
            {message}
          </div>
        </div>
      </div>
    </div>
  )
}

export default StatusPanel
