import React, { useState } from 'react';
import PatientExplanation from './components/PatientExplanation';
import PatientList from './components/PatientList';
import PatientDetails from './components/PatientDetails'; // Import PatientDetails

function App() {
  // Add state to keep track of the currently selected patient
  const [selectedPatient, setSelectedPatient] = useState(null);

  // This function will be called by PatientList when a patient is clicked
  const handlePatientSelect = (patient) => {
    setSelectedPatient(patient);
  };

  return (
    <div className="container mt-5">
      <header className="text-center mb-4">
        <h1>GenAI-Powered Healthcare Assistant</h1>
        <p className="lead">A secure AI tool for interacting with patient records.</p>
      </header>

      <main>
        {/* Pass the handlePatientSelect function to the PatientList */}
        <PatientList onPatientSelect={handlePatientSelect} />

        <div className="mt-4">
          {/* Pass the selected patient data to the PatientDetails component */}
          <PatientDetails patient={selectedPatient} />
        </div>

        <div className="mt-4">
          <PatientExplanation />
        </div>
      </main>

      <footer className="text-center text-muted mt-5">
        <p>&copy; 2025 GenAI Healthcare Project</p>
      </footer>
    </div>
  );
}

export default App;