import React, { useState } from "react";

export default function Landing({ setFile, onContinue }) {
  const [selected, setSelected] = useState(null);

  const handleFile = (e) => {
    const f = e.target.files[0];
    if (f) {
      setSelected(f);
      setFile(f);
    }
  };

  return (
    <div className="page-outer">
      <div className="center-card landing">
        <h1 className="title">AI Resume Analyzer</h1>
        <p className="subtitle">Upload your resume to analyze fit for any job description.</p>

        <label className="upload-btn">
          <input type="file" accept=".pdf,.docx,.txt" onChange={handleFile} />
          <div className="upload-text">{selected ? selected.name : "Click to upload or drag file here"}</div>
        </label>

        <div className="actions">
          <button className="ghost-btn" onClick={() => { setSelected(null); setFile(null); }}>Clear</button>
          <button className="primary-btn" onClick={onContinue} disabled={!selected}>
            Continue
          </button>
        </div>

        <p className="hint">Supported: PDF, DOCX, TXT — we do not store your resume permanently by default.</p>
      </div>
    </div>
  );
}
