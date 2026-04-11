import React from 'react';
import ReactMarkdown from 'react-markdown';
import { ArrowLeft, Copy, Download, Loader2 } from 'lucide-react';

const BlogViewer = ({ selectedTopic, blogContent, onBack, loading, onCopy, onDownload }) => {
  return (
    <div className="blog-view">
      <button
        className="btn-back"
        onClick={onBack}
      >
        <ArrowLeft size={18} /> Back to Topics
      </button>

      <div className="blog-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', gap: '2rem', margin: '1.5rem 0 2rem' }}>
        <div style={{ flex: 1 }}>
          <div className="topic-tag" style={{ marginBottom: '0.75rem' }}>Selected Topic</div>
          <h2 style={{ margin: 0 }}>{selectedTopic}</h2>
        </div>
        <div style={{ display: 'flex', gap: '0.75rem', paddingBottom: '0.5rem' }}>
          <button className="secondary-btn" onClick={onCopy}><Copy size={18} /> Copy</button>
          <button className="secondary-btn" onClick={onDownload}><Download size={18} /> .md</button>
        </div>
      </div>

      <div className="blog-content-wrapper card">
        {loading ? (
          <div className="loading-state" style={{ textAlign: 'center', padding: '4rem 2rem' }}>
            <Loader2 className="spinner-large" style={{ margin: '0 auto 2rem' }} size={48} />
            <h3 style={{ fontSize: '1.5rem', justifyContent: 'center' }}>Crafting your professional blog...</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '1rem', marginTop: '0.75rem' }}>Our AI is researching and writing deep, expert-level content for you.</p>
          </div>
        ) : (
          <div className="markdown-body">
            <ReactMarkdown>{blogContent}</ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
};

export default BlogViewer;
