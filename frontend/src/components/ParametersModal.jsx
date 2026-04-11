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
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}><X size={18} /></button>

        <div className="modal-header">
          <div className="modal-topic-badge">
            <FileText size={13} /> {pendingTopic}
          </div>
          <h3>Configure Blog Parameters</h3>
          <p>Tailor the output — audience, length and goals</p>
        </div>

        <div className="modal-body">
          {/* Row 1 */}
          <div className="modal-row">
            <div className="input-group">
              <label><Users size={13} /> Target Audience</label>
              <input
                type="text"
                placeholder="e.g. Entrepreneurs in India"
                value={config.audience}
                onChange={e => setConfig({ ...config, audience: e.target.value })}
              />
            </div>
            <div className="input-group">
              <label><BarChart2 size={13} /> Word Count</label>
              <input
                type="number"
                value={config.wordCount}
                onChange={e => setConfig({ ...config, wordCount: parseInt(e.target.value) || 0 })}
              />
            </div>
          </div>

          {/* Row 2 */}
          <div className="input-group">
            <label><Target size={13} /> Specific Goal</label>
            <textarea
              rows="3"
              placeholder="What should this blog achieve? e.g. Drive organic traffic, promote MSME loan product"
              value={config.goal}
              onChange={e => setConfig({ ...config, goal: e.target.value })}
            />
          </div>

          {/* Accordion: Internal Links */}
          <div className="links-accordion">
            <button className="links-accordion-trigger" onClick={() => setLinksOpen(v => !v)}>
              <span><LinkIcon size={13} /> Internal Linking Strategy</span>
              <span className="links-accordion-meta">
                {config.internalLinks?.length > 0 && (
                  <span className="links-count-badge">{config.internalLinks.length}</span>
                )}
                {linksOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
              </span>
            </button>

            {linksOpen && (
              <div className="links-accordion-body">
                <div className="links-list">
                  {config.internalLinks?.map((link, index) => (
                    <div key={index} className="link-item">
                      <div className="link-info">
                        <span className="link-keyword">{link.product_keyword}</span>
                        <span className="link-url">{link.url}</span>
                        <span className="link-count">×{link.integration_count}</span>
                      </div>
                      <button className="remove-link-btn" onClick={() => removeInternalLink(index)}>
                        <Trash2 size={13} />
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
                    <Plus size={16} />
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="modal-footer">
          <button className="primary-btn" onClick={onFinalize}>
            <Sparkles size={18} /> Generate Blog Post
          </button>
        </div>
      </div>
    </div>
  );
};

export default ParametersModal;
