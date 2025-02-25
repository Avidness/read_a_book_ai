// components/FileUpload.jsx
import React, { useState } from 'react';
import { Upload, Check, AlertCircle } from 'lucide-react';

const FileUpload = ({ onNewMessage, isUploading, setIsUploading }) => {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [status, setStatus] = useState('');

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      const validTypes = ['application/pdf', 'application/epub+zip', 'text/plain'];
      if (!validTypes.includes(selectedFile.type)) {
        setError('Please upload a PDF, EPUB, or text file');
        setSuccess('');
        return;
      }
      setFile(selectedFile);
      setError('');
      setSuccess('');
      onNewMessage(`File selected: ${selectedFile.name}`);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    setError('');
    setSuccess('');
    setProgress(0);
    setStatus('Starting upload...');
    onNewMessage('Starting upload...');
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/read_a_book', {
        method: 'POST',
        body: formData,
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        // Decode the stream chunk and split by newlines
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n').filter(line => line.trim());

        // For each line in the chunk, add it as a message
        for (const line of lines) {
          try {
            // Attempt to parse as JSON for backward compatibility
            const jsonData = JSON.parse(line);
            
            // Handle message based on status if it's JSON
            if (jsonData.status) {
              switch (jsonData.status) {
                case 'starting':
                  setStatus('Starting upload...');
                  setProgress(10);
                  onNewMessage(jsonData.message || 'Starting upload...');
                  break;
                
                case 'processing':
                  setStatus('Processing...');
                  setProgress(50);
                  onNewMessage(jsonData.message || 'Processing...');
                  break;
                
                case 'complete':
                  setStatus('Complete');
                  setSuccess('File processed successfully!');
                  setProgress(100);
                  onNewMessage(jsonData.message || 'Processing complete');
                  setFile(null);
                  break;
                
                case 'error':
                  setError(jsonData.message || 'An error occurred');
                  setStatus('Error');
                  onNewMessage(`Error: ${jsonData.message || 'An error occurred'}`);
                  break;
                
                default:
                  onNewMessage(jsonData.message || JSON.stringify(jsonData));
              }
            } else {
              // If it's just a regular JSON object without status
              onNewMessage(JSON.stringify(jsonData));
            }
          } catch (e) {
            // If it's not JSON, treat it as a plain string message
            onNewMessage(line);
          }
        }
      }
      
      if (!error) {
        setProgress(100);
        setSuccess('File processed successfully!');
        setStatus('Complete');
      }
    } catch (err) {
      setError(err.message);
      setStatus('Error');
      onNewMessage(`Error: ${err.message}`);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="p-4 border-t border-stone-700 bg-stone-800">
      <div className="space-y-4">
        <div className="flex items-center justify-center w-full">
          <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-stone-700 border-dashed rounded-lg cursor-pointer hover:bg-stone-700/50 transition-colors">
            <div className="flex flex-col items-center justify-center pt-5 pb-6">
              <Upload className="w-8 h-8 mb-2 text-amber-400" />
              <p className="mb-2 text-sm text-amber-50">
                <span className="font-semibold">Click to upload</span> or drag and drop
              </p>
              <p className="text-xs text-amber-200/30">
                PDF, EPUB, or TEXT (up to 50MB)
              </p>
            </div>
            <input 
              type="file" 
              className="hidden" 
              accept=".pdf,.epub,.txt"
              onChange={handleFileChange}
              disabled={isUploading}
            />
          </label>
        </div>

        {(file || isUploading) && (
          <div className="mt-4">
            {file && <p className="text-sm text-amber-50">Selected file: {file.name}</p>}
            {status && <p className="text-sm text-amber-50 mt-2">Status: {status}</p>}
            <div className="w-full bg-stone-700 rounded-full h-2.5 mt-2">
              <div 
                className="bg-amber-600 h-2.5 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            {!isUploading && file && (
              <button
                onClick={handleUpload}
                className="mt-4 w-full bg-amber-600 text-amber-50 rounded-lg py-2 px-4 hover:bg-amber-500 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-amber-400"
                disabled={!file || isUploading}
              >
                Upload File
              </button>
            )}
          </div>
        )}

        {error && (
          <div className="mt-4 flex items-center gap-2 text-red-400 text-sm">
            <AlertCircle className="w-4 h-4" />
            <span>{error}</span>
          </div>
        )}

        {success && (
          <div className="mt-4 flex items-center gap-2 text-green-400 text-sm">
            <Check className="w-4 h-4" />
            <span>{success}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;