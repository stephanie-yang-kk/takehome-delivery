import { useEffect } from 'react'
import Layout from './components/Layout'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import ServiceDetailPage from './pages/ServiceDetailPage'
import { isLoggedIn } from './auth/session'
import { parseRoute } from './routes'
import './App.css'

function App() {
  const route = parseRoute(window.location.pathname)

  useEffect(() => {
    if (route.page === 'unknown') {
      window.location.replace('/login')
      return
    }

    if (!isLoggedIn() && route.page !== 'login') {
      window.location.replace('/login')
      return
    }

    if (isLoggedIn() && route.page === 'login') {
      window.location.replace('/dashboard')
    }
  }, [route.page])

  if (route.page === 'dashboard') {
    return <Layout><DashboardPage /></Layout>
  }

  if (route.page === 'service') {
    return <Layout><ServiceDetailPage id={route.id} /></Layout>
  }

  return <LoginPage />
}

export default App
