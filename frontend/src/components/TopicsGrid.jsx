import React from 'react';
import { Sparkles, CheckCircle2, RefreshCw, Tag } from 'lucide-react';

const TopicsGrid = ({ topics, generatedBlogs, onSelectTopic, onNewCategory, category }) => {
  return (
    <div className="topics-page">
      <div className="topics-page-header">
        <div>
          {category && (
            <div className="topics-category-badge">
              <Tag size={12} /> {category}
            </div>
          )}
          <h2 className="topics-heading">Trending Topics</h2>
        </div>
        <button className="new-category-btn" onClick={onNewCategory}>
          <RefreshCw size={15} />
          Explore New Category
        </button>
      </div>

      <div className="topic-grid">
        {topics.map((topic, i) => {
          const hasBlog = !!generatedBlogs?.[topic];
          return (
            <div
              key={i}
              className={`topic-card ${hasBlog ? 'topic-card--done' : ''}`}
              onClick={() => onSelectTopic(topic)}
            >
              {hasBlog && (
                <div className="blog-ready-badge">
                  <CheckCircle2 size={12} /> Blog Ready
                </div>
              )}
              <div className="topic-tag">#{i + 1}</div>
              <h4>{topic}</h4>
              <div className="topic-card-footer">
                {hasBlog ? (
                  <>View Blog <CheckCircle2 size={15} /></>
                ) : (
                  <>Generate Post <Sparkles size={15} /></>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default TopicsGrid;
