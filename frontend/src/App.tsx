import './App.css'

import { useEffect, useState } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'

import Navbar from './components/navbar/Navbar'
import Home from './pages/Home'
import Login from './pages/Login'
import Contribute from './pages/Login'

function App() {
  const [isInfoModalOpen, setIsInfoModalOpen] = useState(false)

  return (
    <div>
      <Navbar setIsInfoModalOpen={setIsInfoModalOpen} />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/contribute" element={<Contribute />} />
        </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App
