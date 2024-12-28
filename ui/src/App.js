import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './App.css';
import { useStreamFetcher } from "./hooks/useStreamFetcher";

const apiUrl = process.env.REACT_APP_API_URL;

function App() {
  const { streamData, isStreaming, fetchStream } = useStreamFetcher(apiUrl);
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e) => {
    fetchStream('send_input', { 'user_input': inputValue });
  };

  return (
    <div className="App">
      <h3>Input:</h3>
      <input
        className='textbox'
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
      />
      <button
        className='bigBtn'
        onClick={handleSubmit}
        disabled={isStreaming}
      >
        Submit
      </button>

      {streamData.map((chunk, index) => (
        <div key={index}>
          <ReactMarkdown>{chunk}</ReactMarkdown>
        </div>
      ))}
    </div>
  );
}

export default App;