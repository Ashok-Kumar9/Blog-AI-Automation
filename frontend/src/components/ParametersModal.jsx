import React, { useState } from 'react';
import { X, FileText, Users, BarChart2, Target, Link as LinkIcon, Trash2, Plus, Sparkles, ChevronDown, ChevronUp } from 'lucide-react';

const ParametersModal = ({ isOpen, onClose, pendingTopic, config, setConfig, onFinalize }) => {
  const [newLink, setNewLink] = useState({ product_keyword: '', url: '', integration_count: 1 });
  const [linksOpen, setLinksOpen] = useState(false);

  if (!isOpen) return null;

  const addInternalLink = () => {
    if (!newLink.product_keyword || !newLink.url) return;
    setConfig({
      ...config,
      internalLinks: [...(config.internalLinks || []), { ...newLink }]
    });
    setNewLink({ product_keyword: '', url: '', integration_count: 1 });
  };

  const removeInternalLink = (index) => {
    const updatedLinks = config.internalLinks.filter((_, i) => i !== index);
    setConfig({ ...config, internalLinks: updatedLinks });
  };

  return (
    <div className="modal-fullscreen-overlay">
      <div className="modal-fullscreen-content">
        <button className="modal-close-fullscreen" onClick={onClose}><X size={24} /></button>

        <div className="fullscreen-header">
          <div className="modal-topic-badge">
            <FileText size={13} /> {pendingTopic}
          </div>
          <h1>Configure Blog Parameters</h1>
        </div>

        <div className="fullscreen-body">
          <div className="form-row-2col">
            <div className="form-group">
              <label><Users size={16} /> Target Audience</label>
              <input
                type="text"
                className="grey-input"
                placeholder="e.g. Entrepreneurs in India"
                value={config.audience}
                onChange={e => setConfig({ ...config, audience: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label><BarChart2 size={16} /> Word Count</label>
              <input
                type="number"
                className="grey-input"
                placeholder="1200"
                value={config.wordCount}
                onChange={e => setConfig({ ...config, wordCount: parseInt(e.target.value) || 0 })}
              />
            </div>
          </div>

          <div className="form-group">
            <label><Target size={16} /> Specific Goal</label>
            <textarea
              rows="4"
              className="grey-input"
              placeholder="What should this blog achieve? e.g. Drive organic traffic to the SaaS pricing page..."
              value={config.goal}
              onChange={e => setConfig({ ...config, goal: e.target.value })}
            />
          </div>

          <div className="internal-links-section-fullscreen">
            <div className="internal-links-header">
              <label><LinkIcon size={16} /> Internal Linking Strategy</label>
              <span className="advanced-settings-label">ADVANCED SETTINGS</span>
            </div>
            
            <div className="internal-links-box">
              <div className="add-link-form-fullscreen">
                <div className="form-group-small">
                  <label>KEYWORD</label>
                  <input
                    type="text"
                    placeholder="e.g. SEO tips"
                    value={newLink.product_keyword}
                    onChange={e => setNewLink({ ...newLink, product_keyword: e.target.value })}
                  />
                </div>
                <div className="form-group-small">
                  <label>TARGET URL</label>
                  <input
                    type="text"
                    placeholder="https://curator.io/blog/seo"
                    value={newLink.url}
                    onChange={e => setNewLink({ ...newLink, url: e.target.value })}
                  />
                </div>
                <div className="form-group-small count-col">
                  <label>COUNT</label>
                  <input
                    type="number"
                    value={newLink.integration_count}
                    onChange={e => setNewLink({ ...newLink, integration_count: parseInt(e.target.value) || 1 })}
                  />
                </div>
                <div className="form-group-small btn-col">
                  <label>&nbsp;</label>
                  <button className="add-btn-fullscreen" onClick={addInternalLink}>
                    <Plus size={20} />
                  </button>
                </div>
              </div>
              
              {config.internalLinks?.length > 0 && (
                <div className="links-pill-list">
                  {config.internalLinks.map((link, index) => (
                    <div key={index} className="link-pill">
                      <span className="pill-keyword">{link.product_keyword}</span>
                      <span className="pill-url">{link.url}</span>
                      <span className="pill-count">×{link.integration_count}</span>
                      <button className="pill-remove" title="Remove link" onClick={() => removeInternalLink(index)}><X size={14} /></button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="fullscreen-footer">
          <div className="footer-status">
            <div className="status-dot"></div>
            <span>AI Content Engine Ready</span>
          </div>
          <button className="generate-fullscreen-btn" onClick={onFinalize}>
            Generate Blog Post <Sparkles size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ParametersModal;
