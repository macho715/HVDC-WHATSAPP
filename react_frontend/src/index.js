import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

/**
 * MACHO-GPT v3.4-mini Entry Point
 * HVDC Project - Samsung C&T Logistics Integration
 */
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// MACHO-GPT Performance Monitoring
if (process.env.NODE_ENV === 'production') {
  // Add performance monitoring here
  console.log('MACHO-GPT v3.4-mini 프로덕션 모드 활성화');
} 