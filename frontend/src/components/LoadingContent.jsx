import React from "react";
import "./LoadingContent.css";

const LoadingContent = () => {
  return (
    <div className="loading-container">
      <div className="notepad-animation">
        <svg viewBox="0 0 200 240" width="120" height="144">
          {/* Notepad */}
          <rect
            x="30"
            y="20"
            width="140"
            height="180"
            className="notepad-bg"
            rx="4"
          />

          {/* Spiral binding */}
          <circle cx="35" cy="40" r="3" className="notepad-spiral" />
          <circle cx="35" cy="70" r="3" className="notepad-spiral" />
          <circle cx="35" cy="100" r="3" className="notepad-spiral" />
          <circle cx="35" cy="130" r="3" className="notepad-spiral" />
          <circle cx="35" cy="160" r="3" className="notepad-spiral" />

          {/* Lines on notepad */}
          <line x1="50" y1="50" x2="160" y2="50" className="notepad-line" />
          <line x1="50" y1="70" x2="160" y2="70" className="notepad-line" />
          <line x1="50" y1="90" x2="160" y2="90" className="notepad-line" />
          <line x1="50" y1="110" x2="160" y2="110" className="notepad-line" />
          <line x1="50" y1="130" x2="160" y2="130" className="notepad-line" />
          <line x1="50" y1="150" x2="160" y2="150" className="notepad-line" />
          <line x1="50" y1="170" x2="160" y2="170" className="notepad-line" />

          {/* Pen */}
          <g className="pen">
            <line x1="150" y1="30" x2="170" y2="10" className="pen-body" />
            <circle cx="152" cy="32" r="5" className="pen-tip" />
          </g>
        </svg>
      </div>
      <p className="loading-text">Loading your folder...</p>
    </div>
  );
};

export default LoadingContent;
