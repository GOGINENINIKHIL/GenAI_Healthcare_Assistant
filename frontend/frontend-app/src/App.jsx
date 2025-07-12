import React, { useState } from 'react';
import PatientExplanation from './components/PatientExplanation';
import PatientList from './components/PatientList';
import PatientDetails from './components/PatientDetails';
import ClinicalSummarizer from './components/ClinicalSummarizer'; // 1. Import the new component

function App() {
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [noteToExplain, setNoteToExplain] = useState('');

  const handlePatientSelect = (patient) => {
    setSelectedPatient(patient);
  };

  const handleExplainNote = (noteText) => {
    setNoteToExplain({ text: noteText, timestamp: Date.now() });
  };

  return (
    <div className="container mt-5">
      <header className="text-center mb-4">
        <h1>GenAI-Powered Healthcare Assistant</h1>
        <p className="lead">A secure AI tool for interacting with patient records.</p>
      </header>
      
      <main>
        {/* Patient-Facing Tools Section */}
        <div className="row">
          <div className="col-md-6">
            <PatientList onPatientSelect={handlePatientSelect} />
          </div>
          <div className="col-md-6">
            <PatientDetails patient={selectedPatient} onExplainNote={handleExplainNote} />
          </div>
        </div>
        
        <div className="mt-4">
          <PatientExplanation noteToExplain={noteToExplain.text} />
        </div>

        <hr className="my-5" />

        {/* Provider-Facing Tools Section */}
        <h2 className="text-center mb-4">Provider Tools</h2>
        <div className="row justify-content-center">
          <div className="col-md-8">
            <ClinicalSummarizer /> {/* 2. Add the new component here */}
          </div>
        </div>
      </main>

      <footer className="text-center text-muted mt-5">
        <p>&copy; 2025 GenAI Healthcare Project</p>
      </footer>
    </div>
  );
}

export default App;