import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { Sparkles, ArrowLeft, Copy, Download, Loader2, CheckCircle2, AlertCircle, Layout, BookOpen, Settings, X } from 'lucide-react';
import './App.css';

const API_BASE = 'http://127.0.0.1:8000';

function App() {
  // --- State ---
  const [config, setConfig] = useState(() => {
    const saved = localStorage.getItem('blog_config');
    return saved ? JSON.parse(saved) : {
      category: '',
      audience: '',
      wordCount: 2500,
      goal: '',
    };
  });
  const [topics, setTopics] = useState(() => {
    const saved = localStorage.getItem('blog_topics');
    return saved ? JSON.parse(saved) : [];
  });
  const [selectedTopic, setSelectedTopic] = useState(() => {
    return localStorage.getItem('blog_selected_topic') || null;
  });
  const [blogContent, setBlogContent] = useState(() => {
    return localStorage.getItem('blog_content') || '';
  });
  const [status, setStatus] = useState({ text: 'Ready', type: 'success' });
  const [loading, setLoading] = useState({ topics: false, blog: false });
  const [view, setView] = useState(() => {
    return localStorage.getItem('blog_view') || 'topics';
  });
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [pendingTopic, setPendingTopic] = useState(null);

  // --- Persistence Effects ---
  useEffect(() => {
    localStorage.setItem('blog_config', JSON.stringify(config));
  }, [config]);

  useEffect(() => {
    localStorage.setItem('blog_topics', JSON.stringify(topics));
  }, [topics]);

  useEffect(() => {
    if (selectedTopic) localStorage.setItem('blog_selected_topic', selectedTopic);
    else localStorage.removeItem('blog_selected_topic');
  }, [selectedTopic]);

  useEffect(() => {
    localStorage.setItem('blog_content', blogContent);
  }, [blogContent]);

  useEffect(() => {
    localStorage.setItem('blog_view', view);
  }, [view]);

  // --- Effects: Load Defaults ---
  useEffect(() => {
    const hasStoredConfig = localStorage.getItem('blog_config');
    if (!hasStoredConfig) {
      fetch(`${API_BASE}/api/defaults`)
        .then(res => res.json())
        .then(data => {
          setConfig({
            category: data.category,
            audience: data.audience,
            wordCount: data.word_count,
            goal: data.goal,
          });
        })
        .catch(err => {
          console.error('Failed to fetch defaults:', err);
          setStatus({ text: 'API Sync Offline', type: 'error' });
        });
    }
  }, []);

  // --- Handlers ---
  const handleGenerateTopics = async () => {
    setLoading({ ...loading, topics: true });
    setStatus({ text: 'Researching topics...', type: 'pending' });
    setTopics([]);

    try {
      const resp = await fetch(`${API_BASE}/api/generate-topics`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          category: config.category
        }),
      });
      if (!resp.ok) throw new Error('Generation failed');
      const data = await resp.json();
      setTopics(data.topics);
      setStatus({ text: `Found ${data.topics.length} Topics`, type: 'success' });
    } catch (err) {
      console.error(err);
      setStatus({ text: 'Topics Generation Failed', type: 'error' });
    } finally {
      setLoading({ ...loading, topics: false });
    }
  };

  const handleSelectTopic = (topic) => {
    setPendingTopic(topic);
    setIsModalOpen(true);
  };

  const handleFinalizeGeneration = async () => {
    if (!pendingTopic) return;
    
    const topic = pendingTopic;
    setIsModalOpen(false);
    setSelectedTopic(topic);
    setView('blog');
    setLoading({ ...loading, blog: true });
    setStatus({ text: 'Crafting Blog...', type: 'pending' });
    setBlogContent('');

    try {
      const resp = await fetch(`${API_BASE}/api/generate-blog`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic,
          target_audience: config.audience,
          word_count_goal: config.wordCount,
          specific_goal: config.goal,
        }),
      });
      if (!resp.ok) throw new Error('Article generation failed');
      const data = await resp.json();
      setBlogContent(data.content);
      setStatus({ text: 'Blog Generated!', type: 'success' });
    } catch (err) {
      console.error(err);
      setStatus({ text: 'Blog Creation Failed', type: 'error' });
    } finally {
      setLoading({ ...loading, blog: false });
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(blogContent);
    const oldText = status.text;
    setStatus({ text: 'Copied!', type: 'success' });
    setTimeout(() => setStatus({ text: oldText, type: 'success' }), 2000);
  };

  const downloadMarkdown = () => {
    const blob = new Blob([blogContent], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${selectedTopic?.toLowerCase().replace(/ /g, '_')}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // --- Render Helpers ---
  const renderStatusIcon = () => {
    if (status.type === 'pending') return <Loader2 className="spinner" size={16} color="var(--warning-color)" />;
    if (status.type === 'error') return <AlertCircle color="var(--error-color)" size={16} />;
    return <CheckCircle2 color="var(--success-color)" size={16} />;
  };

  return (
    <div className="app-container">
      <header className="main-header">
        <div className="brand-name">Blog Automation <span className="accent">AI</span></div>
        <div className="status-badge">
          {renderStatusIcon()}
          <span>{status.text}</span>
        </div>
      </header>

      <main className="content-grid">
        {/* Sidebar */}
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
              onClick={handleGenerateTopics}
              disabled={loading.topics}
            >
              {loading.topics ? <Loader2 className="spinner" /> : <Sparkles size={18} />}
              Generate Trending Topics
            </button>
          </div>
        </aside>

        {/* Workspace */}
        <section className="workspace">
          {view === 'topics' ? (
            <div className="topics-view">
              <h2>Available Topics</h2>
              <p className="subtitle" style={{ color: 'var(--text-secondary)', marginBottom: '1rem', fontSize: '0.9rem' }}>
                Select a trending topic to generate a high-quality, SEO-optimized blog post for Credit Saison India.
              </p>

              <div className="topic-grid">
                {topics.length > 0 ? topics.map((topic, i) => (
                  <div key={i} className="topic-card" onClick={() => handleSelectTopic(topic)}>
                    <div className="topic-tag">
                      Topic #{i + 1}
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
          ) : (
            <div className="blog-view">
              <button
                className="btn-back"
                onClick={() => setView('topics')}
              >
                <ArrowLeft size={18} /> Back to Topics
              </button>

              <div className="blog-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', gap: '2rem', margin: '1.5rem 0 2rem' }}>
                <div style={{ flex: 1 }}>
                  <div className="topic-tag" style={{ marginBottom: '0.75rem' }}>Selected Topic</div>
                  <h2 style={{ margin: 0 }}>{selectedTopic}</h2>
                </div>
                <div style={{ display: 'flex', gap: '0.75rem', paddingBottom: '0.5rem' }}>
                  <button className="secondary-btn" onClick={copyToClipboard}><Copy size={18} /> Copy</button>
                  <button className="secondary-btn" onClick={downloadMarkdown}><Download size={18} /> .md</button>
                </div>
              </div>

              <div className="blog-content-wrapper card">
                {loading.blog ? (
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
          )}
        </section>
      </main>

      {/* Blog Parameters Modal */}
      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content card">
            <button className="modal-close" onClick={() => setIsModalOpen(false)}>
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
            </div>

            <div className="modal-footer">
              <button 
                className="primary-btn" 
                onClick={handleFinalizeGeneration}
              >
                <Sparkles size={18} /> Generate Full Blog Post
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
