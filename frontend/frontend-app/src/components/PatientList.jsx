import React, { useState, useEffect } from 'react';
import axios from 'axios';

// The component now accepts a function `onPatientSelect` as a prop
function PatientList({ onPatientSelect }) {
  const [patients, setPatients] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/patients');
        setPatients(response.data);
      } catch (err) {
        setError('Failed to fetch patients. Please ensure the backend is running.');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPatients();
  }, []);

  if (isLoading) {
    return <p>Loading patients...</p>;
  }

  if (error) {
    return <p className="text-danger">{error}</p>;
  }

  return (
    <div className="card">
      <div className="card-body">
        <h5 className="card-title">Patient List</h5>
        <div className="list-group">
          {/* Changed from <ul> to <div>, and <li> to <button> */}
          {patients.map((patient) => (
            <button
              key={patient._id}
              type="button"
              className="list-group-item list-group-item-action"
              onClick={() => onPatientSelect(patient)} // Call the passed function on click
            >
              {patient.name} ({patient.gender}, born {patient.birthDate})
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default PatientList;