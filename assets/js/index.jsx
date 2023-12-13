import React from 'react';
import ReactDOM from 'react-dom/client';
import './core.js';
import './Terminal.jsx';
import Dashboard from './Dashboard';
import '../css/style.css';
import TerminalManager from "./Terminal.jsx";


const dashboard_root = ReactDOM.createRoot(
  document.getElementById('dashboard')
);
const terminal_root = ReactDOM.createRoot(
  document.getElementById('terminal-wrapper')
);

terminal_root.render(<TerminalManager />)
dashboard_root.render(<Dashboard />);
