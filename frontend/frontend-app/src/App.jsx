import React from 'react';
import PatientExplanation from './components/PatientExplanation'; // Import the new component

function App() {
  return (
    <div className="container mt-5">
      <header className="text-center mb-4">
        <h1>GenAI-Powered Healthcare Assistant</h1>
        <p className="lead">A secure AI tool for interacting with patient records.</p>
      </header>

      <main>
        <PatientExplanation />
      </main>

      <footer className="text-center text-muted mt-5">
        <p>&copy; 2025 GenAI Healthcare Project</p>
      </footer>
    </div>
  );
}

export default App;