import React from 'react';
import { Sparkles } from 'lucide-react';

const EmptyState = ({ category, onCategoryChange, onGenerate, loading }) => {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !loading && category.trim()) {
      onGenerate();
    }
  };

  return (
    <div className="empty-page-inner">
      <div className="empty-brand">
        <Sparkles size={32} className="empty-brand-icon" />
        <h1>Blog Automation <span className="accent">AI</span></h1>
      </div>
      <p className="empty-tagline">
        Discover trending topics and generate SEO-optimized blog posts — powered by AI.
      </p>

      <div className="empty-form">
        <div className="empty-input-wrap">
          <label className="empty-label">Blog Category</label>
          <input
            className="empty-input"
            type="text"
            placeholder="e.g. MSME Loans, Fintech, Digital Payments"
            value={category}
            onChange={e => onCategoryChange(e.target.value)}
            onKeyDown={handleKeyDown}
            autoComplete="off"
            autoFocus
          />
        </div>
        <button
          className="empty-generate-btn"
          onClick={onGenerate}
          disabled={loading || !category.trim()}
        >
          <Sparkles size={20} />
          Discover Trending Topics
        </button>
      </div>
    </div>
  );
};

export default EmptyState;
