import React, { useState } from 'react';
import axios from 'axios';

function ClinicalSummarizer() {
  const [noteText, setNoteText] = useState('');
  const [summary, setSummary] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    setSummary('');
    setError('');

    try {
      const response = await axios.post('http://127.0.0.1:8000/summarize_note', {
        medical_text: noteText,
      });

      if (response.data && response.data.summary) {
        setSummary(response.data.summary);
      }
    } catch (err) {
      setError('Failed to get summary. Please make sure the backend server is running and try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="card-body">
        <h5 className="card-title">Clinical Note Summarizer</h5>
        <p className="card-text">
          Paste a clinical note below to receive a concise summary for a healthcare professional.
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
          <button type="submit" className="btn btn-success" disabled={isLoading}>
            {isLoading ? 'Summarizing...' : 'Summarize Note'}
          </button>
        </form>

        {summary && (
          <div className="mt-4 p-3 bg-light rounded">
            <h6>AI-Generated Summary:</h6>
            <p>{summary}</p>
          </div>
        )}

        {error && (
          <div className="alert alert-danger mt-4" role="alert">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}

export default ClinicalSummarizer;