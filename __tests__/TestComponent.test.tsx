import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import TestComponent from '../src/components/TestComponent'

describe('TestComponent', () => {
  it('renders correctly', () => {
    render(<TestComponent />)
    expect(screen.getByText('Interactive Test Component')).toBeInTheDocument()
  })

  it('increments counter when button clicked', () => {
    render(<TestComponent />)
    const incrementButton = screen.getByText('Increment')
    
    expect(screen.getByText('Counter: 0')).toBeInTheDocument()
    
    fireEvent.click(incrementButton)
    expect(screen.getByText('Counter: 1')).toBeInTheDocument()
    
    fireEvent.click(incrementButton)
    expect(screen.getByText('Counter: 2')).toBeInTheDocument()
  })

  it('resets counter when reset button clicked', () => {
    render(<TestComponent />)
    const incrementButton = screen.getByText('Increment')
    const resetButton = screen.getByText('Reset')
    
    fireEvent.click(incrementButton)
    fireEvent.click(incrementButton)
    expect(screen.getByText('Counter: 2')).toBeInTheDocument()
    
    fireEvent.click(resetButton)
    expect(screen.getByText('Counter: 0')).toBeInTheDocument()
  })
})