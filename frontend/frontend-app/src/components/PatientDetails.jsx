import React from 'react';

function PatientDetails({ patient }) {
  // This component receives the selected patient as a "prop"
  // If no patient is selected, it displays nothing.
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

        <h6 className="mt-4">Conditions:</h6>
        <ul>
          {patient.conditions.map((condition, index) => (
            <li key={index}>{condition}</li>
          ))}
        </ul>

        <h6 className="mt-4">Medications:</h6>
        <ul>
          {patient.medications.map((medication, index) => (
            <li key={index}>{medication}</li>
          ))}
        </ul>

        <h6 className="mt-4">Clinical Report Notes:</h6>
        {patient.reports_text.length > 0 ? (
          patient.reports_text.map((report, index) => (
            <div key={index} className="p-2 mb-2 bg-light border rounded">
              {/* We are using dangerouslySetInnerHTML because Synthea notes contain HTML tags like <div>.
                  This is generally safe here because we trust the source of the data (our own generator),
                  but you should be very careful using this with unknown data to prevent XSS attacks. */}
              <div dangerouslySetInnerHTML={{ __html: report }} />
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