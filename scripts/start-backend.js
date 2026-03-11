/**
 * Cross-platform backend runner: start uvicorn (using backend/.venv if present).
 * Used by npm run dev:backend.
 */
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

const backendDir = path.join(__dirname, '..', 'backend');
const venvDir = path.join(backendDir, '.venv');
const isWin = process.platform === 'win32';
const venvPython = isWin
  ? path.join(venvDir, 'Scripts', 'python.exe')
  : path.join(venvDir, 'bin', 'python');

const args = ['-m', 'uvicorn', 'main:app', '--reload'];
const hasVenv = fs.existsSync(venvPython);

const cmd = hasVenv ? venvPython : isWin ? 'python' : 'python3';
const child = spawn(cmd, args, {
  cwd: backendDir,
  stdio: 'inherit',
  shell: isWin,
});

child.on('error', (err) => {
  console.error(err);
  process.exit(1);
});
child.on('exit', (code) => {
  process.exit(code ?? 0);
});
