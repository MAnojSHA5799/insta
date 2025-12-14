import React from 'react';
import './App.css';

function App() {
  return (
    <div className="app">
      <div className="card">
        <h2>Connect Your Instagram</h2>
        <p>Securely link your Instagram account to continue</p>
        <a 
          href="http://localhost:9000/instagram/connect" 
          className="connect-btn"
        >
          🔗 Connect Instagram Account
        </a>
      </div>
    </div>
  );
}

export default App;
