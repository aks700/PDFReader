import React, { useState } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';

const PDFUploader = ({ onUploadSuccess }) => {
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileUpload = async (acceptedFiles) => {
    const file = acceptedFiles[0];
    
    if (!file || file.type !== 'application/pdf') {
      setUploadStatus('Please upload a valid PDF file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploadStatus('Uploading...');
      await axios.post('http://localhost:8000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setUploadStatus('PDF uploaded successfully!');
      onUploadSuccess(true);
    } catch (error) {
      setUploadStatus('Upload failed. Please try again.');
      console.error('Upload error:', error);
    }
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop: handleFileUpload,
    accept: { 'application/pdf': ['.pdf'] }
  });

  return (
    <div className="pdf-uploader-container">
      <div {...getRootProps()} className="pdf-uploader">
        <input {...getInputProps()} />
        <p>Drag 'n' drop a PDF file, or click to select</p>
      </div>
      {uploadStatus && <p className="upload-status">{uploadStatus}</p>}
    </div>
  );
};

export default PDFUploader;