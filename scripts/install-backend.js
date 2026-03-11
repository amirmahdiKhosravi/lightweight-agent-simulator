/**
 * Cross-platform backend install: create .venv if needed, then pip install -r requirements.txt.
 * Used by npm run install:backend (and root npm install).
 * Requires Node.js and Python on PATH.
 */
const path = require('path');
const fs = require('fs');
const { spawnSync } = require('child_process');

const backendDir = path.join(__dirname, '..', 'backend');
const venvDir = path.join(backendDir, '.venv');
const isWin = process.platform === 'win32';
const venvPython = isWin
  ? path.join(venvDir, 'Scripts', 'python.exe')
  : path.join(venvDir, 'bin', 'python');
const venvPip = isWin
  ? path.join(venvDir, 'Scripts', 'pip.exe')
  : path.join(venvDir, 'bin', 'pip');

function run(cmd, args, opts = {}) {
  const result = spawnSync(cmd, args, {
    cwd: backendDir,
    stdio: 'inherit',
    shell: isWin,
    ...opts,
  });
  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
  return result;
}

// 1. Create venv if it doesn't exist
if (!fs.existsSync(venvDir)) {
  const systemPython = isWin ? 'python' : 'python3';
  console.log('[install-backend] Creating virtualenv at backend/.venv ...');
  run(systemPython, ['-m', 'venv', '.venv']);
}

// 2. pip install -r requirements.txt
console.log('[install-backend] Installing Python dependencies...');
run(venvPip, ['install', '-r', 'requirements.txt']);

console.log('[install-backend] Done.');
