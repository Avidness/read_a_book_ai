import React, { useState } from 'react';
import { Upload, Check, AlertCircle } from 'lucide-react';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [status, setStatus] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [processingMessages, setProcessingMessages] = useState([]);

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
      setProcessingMessages([]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    setError('');
    setSuccess('');
    setProcessingMessages([]);
    
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

        // Process each line as a JSON message
        for (const line of lines) {
          try {
            const message = JSON.parse(line);
            console.log('Received message:', message);

            switch (message.status) {
              case 'starting':
                setStatus('Starting upload...');
                setProcessingMessages(prev => [...prev, message.message]);
                break;
              
              case 'processing':
                setStatus('Processing...');
                setProcessingMessages(prev => [...prev, message.message]);
                setProgress(50); // Set to intermediate progress
                break;
              
              case 'complete':
                setStatus('Complete');
                setSuccess('File processed successfully!');
                setProcessingMessages(prev => [...prev, 'Processing complete']);
                setProgress(100);
                setFile(null);
                break;
              
              case 'error':
                setError(message.message);
                setStatus('Error');
                break;
              
              default:
                setProcessingMessages(prev => [...prev, JSON.stringify(message)]);
            }
          } catch (e) {
            console.error('Error parsing message:', e);
          }
        }
      }
    } catch (err) {
      setError(err.message);
      setStatus('Error');
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

        {processingMessages.length > 0 && (
          <div className="mt-4 space-y-1">
            {processingMessages.map((message, index) => (
              <p key={index} className="text-xs text-amber-200/70">
                {message}
              </p>
            ))}
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