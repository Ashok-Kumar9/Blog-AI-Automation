import React from 'react';
import { Sparkles } from 'lucide-react';

const TopicsGrid = ({ topics, onSelectTopic }) => {
  return (
    <div className="topics-view">
      <h2>Available Topics</h2>
      <p className="subtitle" style={{ color: 'var(--text-secondary)', marginBottom: '1rem', fontSize: '0.9rem' }}>
        Select a trending topic to generate a high-quality, SEO-optimized blog post for Credit Saison India.
      </p>

      <div className="topic-grid">
        {topics.length > 0 ? topics.map((topic, i) => (
          <div key={i} className="topic-card" onClick={() => onSelectTopic(topic)}>
            <div className="topic-tag">
              #{i + 1}
            </div>
            <h4>{topic}</h4>
            <div className="card-footer" style={{ marginTop: 'auto', paddingTop: '1rem', borderTop: '1px solid var(--border-color)', fontSize: '0.85rem', fontWeight: '700', color: 'var(--primary-color)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              Generate Post <Sparkles size={16} />
            </div>
          </div>
        )) : (
          <div className="empty-state" style={{ padding: '4rem 2rem', textAlign: 'center', gridColumn: '1/-1', background: 'white', borderRadius: 'var(--border-radius)', border: '2px dashed var(--border-color)', boxShadow: 'var(--shadow-lg)' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>✨</div>
            <h3 style={{ marginBottom: '0.5rem', justifyContent: 'center' }}>No Topics Generated Yet</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Configure your settings in the sidebar and click "Generate Trending Topics" to start.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TopicsGrid;
