import { useEffect } from 'react'
import Layout from './components/Layout'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import ServiceDetailPage from './pages/ServiceDetailPage'
import { parseRoute } from './routes'

function App() {
  const route = parseRoute(window.location.pathname)

  useEffect(() => {
    if (route.page === 'unknown') {
      window.history.replaceState(null, '', '/login')
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
