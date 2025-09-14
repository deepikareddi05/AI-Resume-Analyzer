import React, { useState } from "react";

function ProgressBar({ value }) {
  return (
    <div className="progress-outer" role="progressbar" aria-valuenow={value}>
      <div className="progress-inner" style={{ width: `${value}%` }} />
      <div className="progress-label">{value}%</div>
    </div>
  );
}

export default function Analyzer({ file, onBack }) {
  const [jd, setJd] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    if (!file) return alert("Please upload a resume first (go back).");
    setLoading(true);
    const fd = new FormData();
    fd.append("resume", file);
    fd.append("job_desc", jd);

    try {
      const res = await fetch("https://ai-resume-analyzer-c336.onrender.com", {
        method: "POST",
        body: fd
      });
      if (!res.ok) throw new Error("Server error");
      const data = await res.json();
      setResult(data);
    } catch (e) {
      alert("Error: " + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-outer">
      <div className="center-card analyze">
        <div className="row top-row">
          <button className="link-btn" onClick={onBack}>← Back</button>
          <h2 className="card-title">Analyze Resume</h2>
        </div>

        <div className="resume-info">
          <div><strong>Uploaded:</strong> {file ? file.name : "No file selected"}</div>
          <div className="tiny">Tip: Paste the exact job description for best results</div>
        </div>

        <textarea
          className="jd-input"
          placeholder="Paste Job Description here (optional)"
          value={jd}
          onChange={(e) => setJd(e.target.value)}
        />

        <div className="actions">
          <button className="ghost-btn" onClick={() => setJd("")}>Clear JD</button>
          <button className="primary-btn" onClick={submit} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </div>

        {result && (
          <div className="result-area">
            <div className="overall">
              <div className="overall-left">
                <div className="big-score">{result.score}<span className="pct">%</span></div>
                <div className="overall-label">Overall Match</div>
                <div className="overall-sub">{result.interpretation && result.interpretation.skills_label}</div>
              </div>
              <div className="overall-right">
                <div className="metric">
                  <div className="metric-title">Skills Match</div>
                  <ProgressBar value={result.details.skills_match_pct} />
                  <div className="metric-small">Goal: 80%+</div>
                </div>

                <div className="metric">
                  <div className="metric-title">Experience Relevance</div>
                  <ProgressBar value={result.details.experience_relevance_pct} />
                  <div className="metric-small">Good: 70%+</div>
                </div>

                <div className="metric">
                  <div className="metric-title">Achievements</div>
                  <ProgressBar value={result.details.achievements_pct} />
                  <div className="metric-small">Prefer 50%+ bullets with metrics</div>
                </div>

                <div className="metric">
                  <div className="metric-title">Format Quality</div>
                  <ProgressBar value={result.details.format_score_pct} />
                  <div className="metric-small">Target: 75%+</div>
                </div>
              </div>
            </div>

            <div className="suggestions">
              <h3>Suggestions</h3>
              <ul>
                {result.suggestions.map((s, i) => <li key={i}>{s}</li>)}
              </ul>

              <h4>Skills Detected</h4>
              <div className="skill-list">{result.skills_detected.length ? result.skills_detected.join(", ") : "No skills found"}</div>

              {result.skills_in_jd && result.skills_in_jd.length > 0 && (
                <>
                  <h4>Skills Required in JD</h4>
                  <div className="skill-list">{result.skills_in_jd.join(", ") || "—"}</div>
                </>
              )}

              {result.skills_missing && result.skills_missing.length > 0 && (
                <>
                  <h4>Skills Missing</h4>
                  <div className="skill-list missing">{result.skills_missing.join(", ")}</div>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
