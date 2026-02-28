import React from "react";
import "./LandingContent.css";

const LandingContent = () => {
  return (
    <div className="landing-container">
      {/* Hero Section */}
      <section className="landing-hero">
        <div className="hero-content">
          <h1 className="hero-title">
            Todo App
            <span className="title-accent"></span>
          </h1>
          <p className="hero-subtitle">
            Organize your tasks into folders and stay productive
          </p>
          <p className="hero-description">
            A simple, intuitive way to manage your to-do lists. Create folders,
            add items, and track your progress.
          </p>
        </div>
        <div className="hero-icon">
          <span className="icon-large">📋</span>
        </div>
      </section>

      {/* Features Section */}
      <section className="landing-features">
        <h2>Key Features</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">📁</div>
            <h3>Organize</h3>
            <p>
              Create and manage multiple folders to keep your tasks organized by
              project or category.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">✅</div>
            <h3>Track Progress</h3>
            <p>
              Check off completed items and watch your progress grow as you
              complete your tasks.
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="landing-cta">
        <p>
          👈 Check the <strong>"Sidebar"</strong> to get started
        </p>
      </section>
    </div>
  );
};

export default LandingContent;
