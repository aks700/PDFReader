import React, { useState } from 'react';
import axios from 'axios';

const QuestionAnswerer = () => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [error, setError] = useState('');

  const handleQuestionSubmit = async (e) => {
    e.preventDefault();
    
    if (!question) return;

    try {
      const response = await axios.post('http://localhost:8000/ask', 
        null, 
        { params: { question } }
      );
      
      setAnswer(response.data.answer);
      setError('');
    } catch (error) {
      setError(error.response?.data?.detail || 'An error occurred');
      setAnswer('');
    }
  };

  return (
    <div className="question-container">
      <form onSubmit={handleQuestionSubmit}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about the PDF"
          className="question-input"
        />
        <button 
          type="submit" 
          className="submit-button"
        >
          Ask Question
        </button>
      </form>
      {error && <p className="error-message">{error}</p>}
      {answer && (
        <div className="answer-container">
          <h3>Answer:</h3>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
};

export default QuestionAnswerer;