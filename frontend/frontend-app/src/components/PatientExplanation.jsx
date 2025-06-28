import React, { useState } from 'react';
import axios from 'axios';

function PatientExplanation() {
  // --- State Variables ---
  // To store the text the user types into the textarea
  const [noteText, setNoteText] = useState('');
  // To store the simplified explanation we get back from the backend
  const [explanation, setExplanation] = useState('');
  // To show a loading message while we wait for the API
  const [isLoading, setIsLoading] = useState(false);
  // To store any error messages
  const [error, setError] = useState('');

  // --- Handle Form Submission ---
  const handleSubmit = async (event) => {
    // Prevent the default form submission behavior
    event.preventDefault();
    
    // Set loading state and clear previous results
    setIsLoading(true);
    setExplanation('');
    setError('');

    try {
      // Make a POST request to our FastAPI backend
      const response = await axios.post('http://127.0.0.1:8000/explain_note', {
        medical_text: noteText,
      });

      // Update the state with the explanation from the backend
      if (response.data && response.data.simplified_explanation) {
        setExplanation(response.data.simplified_explanation);
      }
    } catch (err) {
      // Handle errors (e.g., network error, backend error)
      setError('Failed to get explanation. Please make sure the backend server is running and try again.');
      console.error(err); // Log the full error to the console for debugging
    } finally {
      // Reset loading state
      setIsLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="card-body">
        <h5 className="card-title">Patient Note Explainer</h5>
        <p className="card-text">
          Paste a clinical note below, and the AI will explain it in simple terms.
        </p>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <textarea
              className="form-control"
              rows="8"
              value={noteText}
              onChange={(e) => setNoteText(e.target.value)}
              placeholder="Enter clinical note here..."
            ></textarea>
          </div>
          <button type="submit" className="btn btn-primary" disabled={isLoading}>
            {isLoading ? 'Loading...' : 'Explain Note'}
          </button>
        </form>

        {/* --- Display the Explanation --- */}
        {explanation && (
          <div className="mt-4 p-3 bg-light rounded">
            <h6>Simplified Explanation:</h6>
            <p>{explanation}</p>
          </div>
        )}

        {/* --- Display Errors --- */}
        {error && (
          <div className="alert alert-danger mt-4" role="alert">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}

export default PatientExplanation;