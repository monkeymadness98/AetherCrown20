import { useEffect, useState } from 'react'
import Head from 'next/head'
import styles from '../styles/Home.module.css'

interface ApiStatus {
  message?: string
  status?: string
  api_version?: string
  environment?: string
}

export default function Home() {
  const [apiStatus, setApiStatus] = useState<ApiStatus | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchApiStatus = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        const response = await fetch(`${apiUrl}/`)
        const data = await response.json()
        setApiStatus(data)
      } catch (error) {
        console.error('Error fetching API status:', error)
        setApiStatus({ status: 'error', message: 'Failed to connect to API' })
      } finally {
        setLoading(false)
      }
    }

    fetchApiStatus()
  }, [])

  return (
    <div className={styles.container}>
      <Head>
        <title>AetherCrown20</title>
        <meta name="description" content="AetherCrown20 Application" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to <span className={styles.highlight}>AetherCrown20</span>
        </h1>

        <p className={styles.description}>
          Enterprise automation and management platform
        </p>

        <div className={styles.statusCard}>
          <h2>API Status</h2>
          {loading ? (
            <p>Loading...</p>
          ) : apiStatus ? (
            <div>
              <p><strong>Status:</strong> {apiStatus.status || 'Unknown'}</p>
              {apiStatus.message && <p><strong>Message:</strong> {apiStatus.message}</p>}
              {apiStatus.api_version && <p><strong>Version:</strong> {apiStatus.api_version}</p>}
              {apiStatus.environment && <p><strong>Environment:</strong> {apiStatus.environment}</p>}
            </div>
          ) : (
            <p>Unable to fetch API status</p>
          )}
        </div>

        <div className={styles.grid}>
          <div className={styles.card}>
            <h2>Documentation &rarr;</h2>
            <p>Find in-depth information about AetherCrown20 features and API.</p>
          </div>

          <div className={styles.card}>
            <h2>Automation &rarr;</h2>
            <p>Explore automated empire management tools and workflows.</p>
          </div>

          <div className={styles.card}>
            <h2>Analytics &rarr;</h2>
            <p>View real-time analytics and performance metrics.</p>
          </div>

          <div className={styles.card}>
            <h2>Deploy &rarr;</h2>
            <p>Deploy your AetherCrown20 instance on Render or Vercel.</p>
          </div>
        </div>
      </main>

      <footer className={styles.footer}>
        <p>AetherCrown20 - Powered by FastAPI and Next.js</p>
      </footer>
    </div>
  )
}
