import React from 'react';

function PatientDetails({ patient, onExplainNote }) {
  if (!patient) {
    return (
      <div className="alert alert-info">
        Select a patient from the list above to see their details.
      </div>
    );
  }

  return (
    <div className="card">
      <div className="card-header">
        <h5>Details for: {patient.name}</h5>
      </div>
      <div className="card-body">
        <p><strong>Gender:</strong> {patient.gender}</p>
        <p><strong>Date of Birth:</strong> {patient.birthDate}</p>

        <h6 className="mt-4">Clinical Report Notes:</h6>
        {patient.reports_text.length > 0 ? (
          patient.reports_text.map((report, index) => (
            <div key={index} className="p-2 mb-2 bg-light border rounded">
              <div dangerouslySetInnerHTML={{ __html: report }} />
              <button 
                className="btn btn-secondary btn-sm mt-2"
                onClick={() => onExplainNote(report)}
              >
                Explain this note
              </button>
            </div>
          ))
        ) : (
          <p>No clinical report notes found for this patient.</p>
        )}
      </div>
    </div>
  );
}

export default PatientDetails;