// src/pages/CodeViewer.jsx
import React, { useEffect, useState } from "react";

function CodeViewer() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const saved = localStorage.getItem("uploadData");
    if (saved) {
      setData(JSON.parse(saved));
    }
  }, []);

  const viewURL = (file) => file ? URL.createObjectURL(file) : null;

  if (!data) return <h3>No Upload Data Found</h3>;

  return (
    <div style={{ padding: "20px" }}>
      <h2>Uploaded Design Files</h2>
      <h3>Top Module: {data.topModule}</h3>

      {data.uploads[data.topModule] && Object.entries(data.uploads[data.topModule]).map(([key, files]) => (
        <div key={key}>
          <b>{key}:</b>
          {Array.from(files).map((file, i) => (
            <div key={i}>
              <a href={viewURL(file)} target="_blank" rel="noopener noreferrer">View</a> |
              <a href={viewURL(file)} download={file.name}> Download</a>
            </div>
          ))}
        </div>
      ))}

      <hr />

      <h3>Sub Modules</h3>
      {data.subModules.map((sub, idx) => (
        <div key={idx} style={{ marginBottom: "10px" }}>
          <strong>{sub}</strong>
          <br />
          {data.uploads[sub] ? (
            Object.values(data.uploads[sub].communication).map((file, i) => (
              <div key={i}>
                <a href={viewURL(file)} target="_blank">View</a> |
                <a href={viewURL(file)} download={file.name}> Download</a>
              </div>
            ))
          ) : (
            <span>No communication docs</span>
          )}
        </div>
      ))}
    </div>
  );
}

export default CodeViewer;
