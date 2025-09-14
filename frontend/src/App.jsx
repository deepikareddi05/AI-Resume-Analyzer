import React, { useState } from "react";
import Landing from "./components/Landing";
import Analyzer from "./components/Analyzer";

export default function App() {
  const [page, setPage] = useState("landing");
  const [file, setFile] = useState(null);

  return (
    <>
      {page === "landing" && (
        <Landing setFile={setFile} onContinue={() => setPage("analyzer")} />
      )}
      {page === "analyzer" && <Analyzer file={file} onBack={() => setPage("landing")} />}
    </>
  );
}
