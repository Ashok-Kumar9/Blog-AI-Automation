import React from 'react';
import { Sparkles, CheckCircle2, RefreshCw, Tag, Briefcase, TrendingUp, Lightbulb, Target, Monitor, Rocket } from 'lucide-react';

const TOPIC_ICONS = [Briefcase, TrendingUp, Lightbulb, Target, Monitor, Rocket];

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
          const Icon = TOPIC_ICONS[i % TOPIC_ICONS.length];
          return (
            <div
              key={i}
              className={`topic-card ${hasBlog ? 'topic-card--done' : ''}`}
            >
              {hasBlog && (
                <div className="blog-ready-badge">
                  <CheckCircle2 size={12} /> Blog Ready
                </div>
              )}
              
              <div className="topic-icon-box">
                <Icon size={20} />
              </div>
              
              <h4>{topic}</h4>
              
              <div className="topic-card-footer">
                <div className="ai-optimized-label">
                  <Sparkles size={14} /> AI Optimized
                </div>
                <button 
                  className={`generate-post-btn ${hasBlog ? 'btn-view' : ''}`}
                  onClick={(e) => {
                    e.stopPropagation();
                    onSelectTopic(topic);
                  }}
                >
                  {hasBlog ? 'View Post' : 'Generate Post'}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default TopicsGrid;
