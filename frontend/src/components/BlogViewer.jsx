import React from 'react';
import ReactMarkdown from 'react-markdown';
import { ArrowLeft, Copy, Download, Loader2, RefreshCw, Image as ImageIcon } from 'lucide-react';

const BlogViewer = ({
  selectedTopic,
  blogContent,
  topicImage,
  loadingImage,
  onGenerateImage,
  onDownloadImage,
  onBack,
  loading,
  onCopy,
  onDownload,
  onRegenerate
}) => {
  return (
    <div className="blog-view">
      <div className="blog-view-topbar">
        <button className="btn-back" onClick={onBack}>
          <ArrowLeft size={16} /> Back to Topics
        </button>
        <div className="blog-action-group">
          <button className="secondary-btn" onClick={onRegenerate} title="Change parameters and regenerate">
            <RefreshCw size={16} /> Regenerate
          </button>
          <button className="secondary-btn" onClick={onGenerateImage} disabled={loadingImage} title="Generate Hero Image">
            {loadingImage ? <Loader2 size={16} className="spinner" /> : <ImageIcon size={16} />}
            Image
          </button>
          {topicImage && (
            <button className="secondary-btn" onClick={onDownloadImage} title="Download Hero Image">
              <Download size={16} /> .png
            </button>
          )}
          <button className="secondary-btn" onClick={onCopy}>
            <Copy size={16} /> Copy
          </button>
          <button className="secondary-btn" onClick={onDownload}>
            <Download size={16} /> .md
          </button>
        </div>
      </div>

      <div className="blog-meta">
        <h2>{selectedTopic}</h2>
      </div>

      <div className="blog-content-wrapper card">
        {loading ? (
          <div className="blog-loading">
            <div className="blog-loading-orb">
              <Loader2 className="spinner-large" size={44} />
            </div>
            <h3>Crafting your blog post...</h3>
            <p>Our AI is researching, structuring, and writing expert-level content for you.</p>
            <div className="blog-loading-steps">
              <span>Researching topic</span>
              <span className="loading-sep">·</span>
              <span>Structuring outline</span>
              <span className="loading-sep">·</span>
              <span>Writing content</span>
              <span className="loading-sep">·</span>
              <span>Optimising for SEO</span>
            </div>
          </div>
        ) : (
          <div className="markdown-body">
            {topicImage && (
              <div className="blog-hero-image" style={{ marginBottom: '32px' }}>
                <img
                  src={`data:image/png;base64,${topicImage}`}
                  alt="Blog Hero"
                  style={{ width: '100%', height: 'auto', borderRadius: '8px', display: 'block' }}
                />
              </div>
            )}
            <ReactMarkdown>{blogContent}</ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
};

export default BlogViewer;
