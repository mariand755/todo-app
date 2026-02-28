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
            fill="#f5f5f5"
            stroke="#333"
            strokeWidth="2"
            rx="4"
          />

          {/* Spiral binding */}
          <circle cx="35" cy="40" r="3" fill="#999" />
          <circle cx="35" cy="70" r="3" fill="#999" />
          <circle cx="35" cy="100" r="3" fill="#999" />
          <circle cx="35" cy="130" r="3" fill="#999" />
          <circle cx="35" cy="160" r="3" fill="#999" />

          {/* Lines on notepad */}
          <line
            x1="50"
            y1="50"
            x2="160"
            y2="50"
            stroke="#ddd"
            strokeWidth="1"
          />
          <line
            x1="50"
            y1="70"
            x2="160"
            y2="70"
            stroke="#ddd"
            strokeWidth="1"
          />
          <line
            x1="50"
            y1="90"
            x2="160"
            y2="90"
            stroke="#ddd"
            strokeWidth="1"
          />
          <line
            x1="50"
            y1="110"
            x2="160"
            y2="110"
            stroke="#ddd"
            strokeWidth="1"
          />
          <line
            x1="50"
            y1="130"
            x2="160"
            y2="130"
            stroke="#ddd"
            strokeWidth="1"
          />
          <line
            x1="50"
            y1="150"
            x2="160"
            y2="150"
            stroke="#ddd"
            strokeWidth="1"
          />
          <line
            x1="50"
            y1="170"
            x2="160"
            y2="170"
            stroke="#ddd"
            strokeWidth="1"
          />

          {/* Pen */}
          <g className="pen">
            <line
              x1="150"
              y1="30"
              x2="170"
              y2="10"
              stroke="#666"
              strokeWidth="3"
              strokeLinecap="round"
            />
            <circle cx="152" cy="32" r="5" fill="#ff6b6b" />
          </g>
        </svg>
      </div>
      <p className="loading-text">Loading your folder...</p>
    </div>
  );
};

export default LoadingContent;
