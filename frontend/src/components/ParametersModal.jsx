import React, { useState } from 'react';
import { X, Layout, Link as LinkIcon, Trash2, Plus, Sparkles } from 'lucide-react';

const ParametersModal = ({ isOpen, onClose, pendingTopic, config, setConfig, onFinalize }) => {
  const [newLink, setNewLink] = useState({ product_keyword: '', url: '', integration_count: 1 });

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
    <div className="modal-overlay">
      <div className="modal-content card">
        <button className="modal-close" onClick={onClose}>
          <X size={24} />
        </button>
        <div className="modal-header">
          <h3><Layout size={24} /> Blog Parameters</h3>
          <p>Configure the specifics for: <strong>{pendingTopic}</strong></p>
        </div>
        
        <div className="modal-body">
          <div className="input-group">
            <label>Target Audience</label>
            <input
              type="text"
              placeholder="e.g. Entrepreneurs in India"
              value={config.audience}
              onChange={e => setConfig({ ...config, audience: e.target.value })}
            />
          </div>
          
          <div className="input-row">
            <div className="input-group">
              <label>Word Count Goal</label>
              <input
                type="number"
                value={config.wordCount}
                onChange={e => setConfig({ ...config, wordCount: parseInt(e.target.value) || 0 })}
              />
            </div>
          </div>

          <div className="input-group">
            <label>Specific Goal</label>
            <textarea
              rows="3"
              placeholder="What should this blog achieve? (e.g. Brand awareness, Lead generation)"
              value={config.goal}
              onChange={e => setConfig({ ...config, goal: e.target.value })}
            />
          </div>

          <div className="internal-links-section">
            <label><LinkIcon size={14} style={{ marginRight: '6px' }} /> Internal Linking Strategy</label>
            
            <div className="links-list">
              {config.internalLinks?.map((link, index) => (
                <div key={index} className="link-item">
                  <div className="link-info">
                    <span className="link-keyword">{link.product_keyword}</span>
                    <span className="link-url">{link.url}</span>
                    <span className="link-count">×{link.integration_count}</span>
                  </div>
                  <button className="remove-link-btn" onClick={() => removeInternalLink(index)}>
                    <Trash2 size={14} />
                  </button>
                </div>
              ))}
            </div>

            <div className="add-link-form">
              <input
                type="text"
                placeholder="Keyword"
                value={newLink.product_keyword}
                onChange={e => setNewLink({ ...newLink, product_keyword: e.target.value })}
              />
              <input
                type="text"
                placeholder="URL"
                value={newLink.url}
                onChange={e => setNewLink({ ...newLink, url: e.target.value })}
              />
              <input
                type="number"
                value={newLink.integration_count}
                onChange={e => setNewLink({ ...newLink, integration_count: parseInt(e.target.value) || 1 })}
              />
              <button className="add-btn" onClick={addInternalLink}>
                <Plus size={18} />
              </button>
            </div>
          </div>
        </div>

        <div className="modal-footer">
          <button 
            className="primary-btn" 
            onClick={onFinalize}
          >
            <Sparkles size={18} /> Generate Full Blog Post
          </button>
        </div>
      </div>
    </div>
  );
};

export default ParametersModal;
