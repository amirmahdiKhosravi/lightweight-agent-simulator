import { useState, useEffect } from 'react'
import { submitTask, getTaskHistory } from './api'
import './App.css'

/**
 * Root application component.
 *
 * Layout: fixed history sidebar on the left, main panel (input + result +
 * execution trace) on the right.
 */
function App() {
  const [taskInput, setTaskInput] = useState('')
  const [currentResult, setCurrentResult] = useState(null)
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  /** Fetch the full task history from the backend and refresh the sidebar. */
  const loadHistory = async () => {
    try {
      const tasks = await getTaskHistory()
      setHistory(tasks)
    } catch (e) {
      console.error('Failed to load history:', e)
    }
  }

  useEffect(() => {
    loadHistory()
  }, [])

  /**
   * Submit the current input to the agent API.
   * On success the result panel and history sidebar are both refreshed.
   * Network errors are surfaced with a helpful hint about starting the backend.
   */
  const handleSubmit = async (e) => {
    e.preventDefault()
    const task = taskInput.trim()
    if (!task || loading) return
    setLoading(true)
    setError(null)
    try {
      const result = await submitTask(task)
      setCurrentResult(result)
      await loadHistory()
    } catch (e) {
      const msg = e.message || 'Request failed'
      const isNetworkError = msg === 'Failed to fetch' || e.name === 'TypeError'
      setError(isNetworkError
        ? 'Could not reach the API. Make sure the backend is running: cd backend && fastapi dev main.py'
        : msg)
    } finally {
      setLoading(false)
    }
  }

  /** Display a previously executed task from the history sidebar. */
  const showTask = (task) => {
    setCurrentResult({
      final_output: task.final_output,
      execution_steps: task.execution_steps,
      tools_used: task.tools_used,
      timestamp: task.timestamp,
    })
  }

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex">
      {/* History sidebar */}
      <aside className="w-72 border-r border-slate-700 flex flex-col bg-slate-800/50">
        <h2 className="p-4 font-semibold text-slate-200 border-b border-slate-700">History</h2>
        <ul className="flex-1 overflow-auto p-2">
          {history.length === 0 && (
            <li className="text-slate-500 text-sm p-2">No tasks yet</li>
          )}
          {history.map((t) => (
            <li key={t.id}>
              <button
                type="button"
                onClick={() => showTask(t)}
                className="w-full text-left p-3 rounded-lg hover:bg-slate-700/80 transition text-sm truncate"
                title={t.user_input}
              >
                <span className="block truncate">{t.user_input || '(empty)'}</span>
                {t.timestamp && (
                  <span className="text-xs text-slate-500 block mt-1">{t.timestamp}</span>
                )}
              </button>
            </li>
          ))}
        </ul>
      </aside>

      {/* Main: input + result + trace */}
      <main className="flex-1 flex flex-col max-w-3xl mx-auto p-6 w-full">
        <h1 className="text-xl font-semibold text-slate-200 mb-4">Lightweight Agent Simulator</h1>

        {/* Task input */}
        <form onSubmit={handleSubmit} className="flex gap-2 mb-6">
          <input
            type="text"
            value={taskInput}
            onChange={(e) => setTaskInput(e.target.value)}
            placeholder="e.g. What is 5 + 3? Weather in London. Uppercase hello world."
            className="flex-1 rounded-lg border border-slate-600 bg-slate-800 px-4 py-2 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-sky-500"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !taskInput.trim()}
            className="rounded-lg bg-sky-600 px-4 py-2 font-medium text-white hover:bg-sky-500 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            {loading ? 'Running…' : 'Run'}
          </button>
        </form>

        {error && (
          <div className="mb-4 p-3 rounded-lg bg-red-900/50 border border-red-700 text-red-200 text-sm">
            {error}
          </div>
        )}

        {/* Result display */}
        <section className="mb-6">
          <h2 className="text-sm font-medium text-slate-400 uppercase tracking-wider mb-2">Result</h2>
          <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-4 min-h-[4rem]">
            {currentResult ? (
              <p className="text-slate-100 whitespace-pre-wrap">{currentResult.final_output}</p>
            ) : (
              <p className="text-slate-500">Run a task to see the result.</p>
            )}
          </div>
        </section>

        {/* Trace inspector */}
        <section>
          <h2 className="text-sm font-medium text-slate-400 uppercase tracking-wider mb-2">Execution trace</h2>
          <div className="rounded-lg border border-slate-700 bg-slate-800/50 overflow-hidden">
            {currentResult?.execution_steps?.length ? (
              <ol className="divide-y divide-slate-700">
                {currentResult.execution_steps.map((step, i) => (
                  <li key={i} className="px-4 py-3 text-sm text-slate-300 font-mono">
                    {step}
                  </li>
                ))}
              </ol>
            ) : (
              <p className="p-4 text-slate-500 text-sm">No trace yet.</p>
            )}
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
