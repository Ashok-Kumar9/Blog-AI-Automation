import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { Sparkles, ArrowLeft, Copy, Download, Loader2, CheckCircle2, AlertCircle } from 'lucide-react';
import './App.css';

const API_BASE = 'http://127.0.0.1:8000';

function App() {
  // --- State ---
  const [config, setConfig] = useState({
    category: '',
    competitors: '',
    audience: '',
    wordCount: 2500,
    goal: '',
  });
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [blogContent, setBlogContent] = useState('');
  const [status, setStatus] = useState({ text: 'System Ready', type: 'success' });
  const [loading, setLoading] = useState({ topics: false, blog: false });
  const [view, setView] = useState('topics'); // 'topics' or 'blog'

  // --- Effects: Load Defaults ---
  useEffect(() => {
    fetch(`${API_BASE}/api/defaults`)
      .then(res => res.json())
      .then(data => {
        setConfig({
          category: data.category,
          competitors: data.competitors.join(', '),
          audience: data.audience,
          wordCount: data.word_count,
          goal: data.goal,
        });
      })
      .catch(err => {
        console.error('Failed to fetch defaults:', err);
        setStatus({ text: 'API Sync Offline', type: 'error' });
      });
  }, []);

  // --- Handlers ---
  const handleGenerateTopics = async () => {
    setLoading({ ...loading, topics: true });
    setStatus({ text: 'Scanning competitors...', type: 'pending' });
    setTopics([]);

    try {
      const resp = await fetch(`${API_BASE}/api/generate-topics`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          category: config.category,
          competitors: config.competitors.split(',').map(c => c.trim()).filter(c => c)
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

  const handleSelectTopic = async (topic) => {
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
    if (status.type === 'pending') return <Loader2 className="spinner" size={14} />;
    if (status.type === 'error') return <AlertCircle color="#ef4444" size={14} />;
    return <CheckCircle2 color="#10b981" size={14} />;
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
          <div className="card glass">
            <h3>Generation Settings</h3>
            <div className="input-group">
              <label>Blog Category</label>
              <input 
                type="text" 
                value={config.category} 
                onChange={e => setConfig({...config, category: e.target.value})}
              />
            </div>
            <div className="input-group">
              <label>Competitors</label>
              <textarea 
                rows="3" 
                value={config.competitors} 
                onChange={e => setConfig({...config, competitors: e.target.value})}
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

          <div className="card glass" style={{ marginTop: '1.5rem' }}>
            <h3>Blog Parameters</h3>
            <div className="input-group">
              <label>Target Audience</label>
              <input 
                type="text" 
                value={config.audience} 
                onChange={e => setConfig({...config, audience: e.target.value})}
              />
            </div>
            <div className="input-group">
              <label>Word Count Goal</label>
              <input 
                type="number" 
                value={config.wordCount} 
                onChange={e => setConfig({...config, wordCount: parseInt(e.target.value)})}
              />
            </div>
            <div className="input-group">
              <label>Specific Goal</label>
              <textarea 
                rows="2" 
                value={config.goal} 
                onChange={e => setConfig({...config, goal: e.target.value})}
              />
            </div>
          </div>
        </aside>

        {/* Workspace */}
        <section className="workspace">
          {view === 'topics' ? (
            <div className="topics-view">
              <h2>Available Topics</h2>
              <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
                Select a trending topic to generate a full-length, SEO-optimized blog post.
              </p>
              
              <div className="topic-grid">
                {topics.length > 0 ? topics.map((topic, i) => (
                  <div key={i} className="topic-card" onClick={() => handleSelectTopic(topic)}>
                    <div style={{ color: 'var(--accent-color)', fontSize: '0.8rem', marginBottom: '0.5rem' }}>
                      Topic #{i+1}
                    </div>
                    <h4>{topic}</h4>
                    <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                      Generate Post →
                    </div>
                  </div>
                )) : (
                  <div style={{ padding: '5rem', textAlign: 'center', gridColumn: '1/-1', opacity: 0.5 }}>
                    <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📂</div>
                    <p>No topics generated yet. Configure settings and start exploring.</p>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="blog-view">
              <button 
                className="btn-back" 
                style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer', marginBottom: '1rem' }}
                onClick={() => setView('topics')}
              >
                <ArrowLeft size={16} /> Back to Topics
              </button>
              
              <div className="blog-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h2>{selectedTopic}</h2>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <button className="secondary-btn" onClick={copyToClipboard}><Copy size={16} /> Copy</button>
                  <button className="secondary-btn" onClick={downloadMarkdown}><Download size={16} /> .md</button>
                </div>
              </div>

              <div className="card glass blog-content-wrapper">
                {loading.blog ? (
                  <div style={{ textAlign: 'center', padding: '5rem' }}>
                    <Loader2 className="spinner-large" style={{ margin: '0 auto 2rem' }} />
                    <h3>Crafting your professional blog...</h3>
                    <p style={{ color: 'var(--text-secondary)' }}>This may take a minute to ensure high-quality content.</p>
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
    </div>
  );
}

export default App;
