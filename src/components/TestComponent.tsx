import React, { useState } from 'react'

export default function TestComponent() {
  const [count, setCount] = useState(0)
  const [apiResponse, setApiResponse] = useState<string | null>(null)

  const testAPI = async () => {
    try {
      const res = await fetch('/api/health')
      const data = await res.json()
      setApiResponse(JSON.stringify(data, null, 2))
    } catch (error) {
      setApiResponse('Error fetching API')
    }
  }

  return (
    <div style={{ 
      padding: '1rem', 
      border: '1px solid #ddd', 
      borderRadius: '8px',
      backgroundColor: '#f9f9f9'
    }}>
      <h3>Interactive Test Component</h3>
      
      <div style={{ marginTop: '1rem' }}>
        <p>Counter: {count}</p>
        <button 
          onClick={() => setCount(count + 1)}
          style={{
            padding: '0.5rem 1rem',
            marginRight: '0.5rem',
            cursor: 'pointer'
          }}
        >
          Increment
        </button>
        <button 
          onClick={() => setCount(0)}
          style={{
            padding: '0.5rem 1rem',
            cursor: 'pointer'
          }}
        >
          Reset
        </button>
      </div>

      <div style={{ marginTop: '1rem' }}>
        <button 
          onClick={testAPI}
          style={{
            padding: '0.5rem 1rem',
            cursor: 'pointer'
          }}
        >
          Test API Health
        </button>
        {apiResponse && (
          <pre style={{ 
            marginTop: '1rem', 
            padding: '1rem', 
            backgroundColor: '#fff',
            border: '1px solid #ddd',
            borderRadius: '4px',
            overflow: 'auto'
          }}>
            {apiResponse}
          </pre>
        )}
      </div>
    </div>
  )
}