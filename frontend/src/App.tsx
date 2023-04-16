import './App.css'

import { useEffect, useState } from 'react'
import Div100vh from 'react-div-100vh'

import { AlertContainer } from './components/alerts/AlertContainer'

function App() {
  return (
    <Div100vh>
      <div className="flex h-full flex-col">
        <AlertContainer />
      </div>
    </Div100vh>
  )
}

export default App
