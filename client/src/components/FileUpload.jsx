import React, { useState } from 'react';
import { Upload, Check, AlertCircle } from 'lucide-react';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isUploading, setIsUploading] = useState(false);

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
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    setError('');
    setSuccess('');
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/upload2', {
        method: 'POST',
        body: formData,
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setProgress(percentCompleted);
        },
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.detail || 'Upload failed');
      }

      setSuccess(result.message || 'File uploaded successfully!');
      setFile(null);
      setProgress(0);
      
      console.log('Upload result:', result);
    } catch (err) {
      setError(err.message);
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

        {file && (
          <div className="mt-4">
            <p className="text-sm text-amber-50">Selected file: {file.name}</p>
            <div className="w-full bg-stone-700 rounded-full h-2.5 mt-2">
              <div 
                className="bg-amber-600 h-2.5 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <button
              onClick={handleUpload}
              className="mt-4 w-full bg-amber-600 text-amber-50 rounded-lg py-2 px-4 hover:bg-amber-500 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-amber-400"
              disabled={!file || isUploading}
            >
              {isUploading ? 'Uploading...' : 'Upload File'}
            </button>
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