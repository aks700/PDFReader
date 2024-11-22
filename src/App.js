import React, { useState } from 'react';
import PDFUploader from './components/PDFUploader';
import QuestionAnswerer from './components/QuestionAnswerer';
import './index.css';

function App() {
  const [pdfUploaded, setPdfUploaded] = useState(false);

  return (
    <div className="app-container">
      <div className="main-card">
        <h1>PDF Question Answering App</h1>
        <PDFUploader onUploadSuccess={() => setPdfUploaded(true)} />
        {pdfUploaded && <QuestionAnswerer />}
      </div>
    </div>
  );
}

export default App;