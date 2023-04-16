import './App.css'

import { useEffect, useState } from 'react'
import Div100vh from 'react-div-100vh'
import { BrowserRouter, Route, Routes } from 'react-router-dom'

import { AlertContainer } from './components/alerts/AlertContainer'
import { Navbar } from './components/navbar/Navbar'

function App() {
  return (
    <Div100vh>
      <div className="flex h-full flex-col">
        <Navbar brand="iBookStore" />
        <Routes> </Routes>
      </div>
    </Div100vh>
  )
}

export default App
