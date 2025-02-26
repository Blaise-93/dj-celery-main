import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import './css/footer.css'
/* import * as serviceWorker from './serviceWorker' */
// Routes === Switch (deprecated)
import {Route, BrowserRouter as Router, Routes } from 'react-router-dom'
import Header from './components/Header.jsx'
import Footer from './components/Footer.jsx'
import SignUpUSer from './components/register/register.jsx'
//import { Register } from './components/Users.jsx'
//import { SignUp } from './components/register/register.jsx'


const routing = (
    <Router>
      <React.StrictMode>
        <Header />
        <Routes>
          <Route path='/' element={<App/>} />
          <Route path='/register/' element={<SignUpUSer/>} />

         {/*  <Route path='/register' element={<Register/>} /> */}
        </Routes>
        <Footer/>
      </React.StrictMode>   
    </Router>
);


ReactDOM.createRoot(document.getElementById("root")).render(routing)

