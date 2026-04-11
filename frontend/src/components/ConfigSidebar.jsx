import React from 'react';
import { Settings, Sparkles, Loader2 } from 'lucide-react';

const ConfigSidebar = ({ config, setConfig, onGenerateTopics, loading }) => {
  return (
    <aside className="config-sidebar">
      <div className="card">
        <h3><Settings size={20} /> Generation Settings</h3>
        <div className="input-group">
          <label>Blog Category</label>
          <input
            type="text"
            placeholder="e.g. MSME Loan"
            value={config.category}
            onChange={e => setConfig({ ...config, category: e.target.value })}
          />
        </div>
        <button
          className="primary-btn"
          onClick={onGenerateTopics}
          disabled={loading}
        >
          {loading ? <Loader2 className="spinner" /> : <Sparkles size={18} />}
          Generate Trending Topics
        </button>
      </div>
    </aside>
  );
};

export default ConfigSidebar;
