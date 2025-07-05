import React, { useState, useEffect } from 'react';
import axios from 'axios';

// This component now receives a noteToExplain prop
function PatientExplanation({ noteToExplain }) {
  const [noteText, setNoteText] = useState('');
  const [explanation, setExplanation] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // --- NEW: useEffect hook to watch for changes in the noteToExplain prop ---
  useEffect(() => {
    // If a new note is passed from the parent component, update our state
    if (noteToExplain) {
      setNoteText(noteToExplain);
      // Optional: automatically submit when a new note is received
      // handleSubmit(null, noteToExplain);
    }
  }, [noteToExplain]); // This effect runs whenever noteToExplain changes

  const handleSubmit = async (event, textToSubmit) => {
    if (event) event.preventDefault(); // Prevent default form submission if it's from the form

    const note = textToSubmit || noteText; // Use passed text or state
    if (!note) return; // Don't submit if there's no text

    setIsLoading(true);
    setExplanation('');
    setError('');

    try {
      const response = await axios.post('http://127.0.0.1:8000/explain_note', {
        medical_text: note,
      });
      if (response.data && response.data.simplified_explanation) {
        setExplanation(response.data.simplified_explanation);
      }
    } catch (err) {
      setError('Failed to get explanation. Please make sure the backend server is running and try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="card-body">
        <h5 className="card-title">Patient Note Explainer</h5>
        <p className="card-text">
          Paste a note below, or select "Explain this note" from a patient's details.
        </p>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <textarea
              className="form-control"
              rows="8"
              value={noteText}
              onChange={(e) => setNoteText(e.target.value)}
              placeholder="Clinical note will appear here..."
            ></textarea>
          </div>
          <button type="submit" className="btn btn-primary" disabled={isLoading}>
            {isLoading ? 'Loading...' : 'Explain Note'}
          </button>
        </form>

        {explanation && (
          <div className="mt-4 p-3 bg-light rounded">
            <h6>Simplified Explanation:</h6>
            <p>{explanation}</p>
          </div>
        )}

        {error && <div className="alert alert-danger mt-4">{error}</div>}
      </div>
    </div>
  );
}

export default PatientExplanation;