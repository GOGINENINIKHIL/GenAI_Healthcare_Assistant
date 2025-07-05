import React, { useState } from 'react';
import PatientExplanation from './components/PatientExplanation';
import PatientList from './components/PatientList';
import PatientDetails from './components/PatientDetails';

function App() {
  const [selectedPatient, setSelectedPatient] = useState(null);
  // --- NEW: Add state for the note to be explained ---
  const [noteToExplain, setNoteToExplain] = useState('');

  const handlePatientSelect = (patient) => {
    setSelectedPatient(patient);
  };

  // --- NEW: Handler to receive the note text from PatientDetails ---
  const handleExplainNote = (noteText) => {
    // We use a timestamp to ensure React re-renders even if the same note is clicked twice
    setNoteToExplain({ text: noteText, timestamp: Date.now() });
  };

  return (
    <div className="container mt-5">
      <header className="text-center mb-4">
        <h1>GenAI-Powered Healthcare Assistant</h1>
        <p className="lead">A secure AI tool for interacting with patient records.</p>
      </header>

      <main>
        <PatientList onPatientSelect={handlePatientSelect} />

        <div className="mt-4">
          {/* Pass the new handler function to PatientDetails */}
          <PatientDetails patient={selectedPatient} onExplainNote={handleExplainNote} />
        </div>

        <div className="mt-4">
          {/* Pass the state down to PatientExplanation */}
          <PatientExplanation noteToExplain={noteToExplain.text} />
        </div>
      </main>

      <footer className="text-center text-muted mt-5">
        <p>&copy; 2025 GenAI Healthcare Project</p>
      </footer>
    </div>
  );
}

export default App;