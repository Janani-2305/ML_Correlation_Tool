import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [targetColumn, setTargetColumn] = useState('');
  const [method, setMethod] = useState('pearson');
  const [correlations, setCorrelations] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    formData.append('target_column', targetColumn);
    formData.append('method', method);

    try {
      const response = await axios.post('http://127.0.0.1:5000/upload', formData);
      setCorrelations(response.data);
      
    } catch (error) {
      console.error('There was an error uploading the file!', error);
    }
  };

  return (
    <div className="App">
      <h1> Correlations Analyze </h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Choose CSV or Excel file:</label>
          <input type="file" accept=".csv, .xlsx" onChange={handleFileChange} required />
        </div>
        <div>
          <label>Target Column:</label>
          <input type="text" value={targetColumn} onChange={(e) => setTargetColumn(e.target.value)} required />
        </div>
        <div>
          <label>Correlation Method:</label>
          <select value={method} onChange={(e) => setMethod(e.target.value)}>
            <option value="pearson">Pearson</option>
            <option value="spearman">Spearman</option>
            <option value="kendall">Kendall</option>
          </select>
        </div>
        <button type="submit">Analyze</button>
      </form>
      {correlations && (
        <div>
          <h2>Correlation Results:</h2>
          <ul>
            {Object.keys(correlations).map((key) => (
              <li key={key} className={correlations[key].color}>
                {key}: {correlations[key].correlation !== undefined ? correlations[key].correlation.toFixed(2) : 'N/A'}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
