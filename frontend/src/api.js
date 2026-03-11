// In dev, use relative /api so Vite proxy can forward to the backend
const API_BASE = import.meta.env.VITE_API_URL ?? (import.meta.env.DEV ? '' : 'http://localhost:8000');

/**
 * Submit a task to the agent. Returns the structured result (final_output, execution_steps, tools_used, timestamp).
 * @param {string} task - The user's input task
 * @returns {Promise<object>}
 */
export async function submitTask(task) {
  const res = await fetch(`${API_BASE}/api/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP ${res.status}`);
  }
  return res.json();
}

/**
 * Fetch the history of all executed tasks.
 * @returns {Promise<Array<object>>}
 */
export async function getTaskHistory() {
  const res = await fetch(`${API_BASE}/api/tasks`);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP ${res.status}`);
  }
  return res.json();
}
