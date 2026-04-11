import React, { useState, useEffect } from 'react';
import { blogService } from './services/blogService';
import './App.css';

// Components
import Header from './components/Header';
import ConfigSidebar from './components/ConfigSidebar';
import TopicsGrid from './components/TopicsGrid';
import BlogViewer from './components/BlogViewer';
import ParametersModal from './components/ParametersModal';

function App() {
  // --- State ---
  const [config, setConfig] = useState(() => {
    const saved = localStorage.getItem('blog_config');
    const parsed = saved ? JSON.parse(saved) : {};
    return {
      category: parsed.category || '',
      audience: parsed.audience || '',
      wordCount: parsed.wordCount || 2500,
      goal: parsed.goal || '',
      internalLinks: parsed.internalLinks || [],
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

  // --- Handlers ---
  const handleGenerateTopics = async () => {
    setLoading({ ...loading, topics: true });
    setStatus({ text: 'Researching topics...', type: 'pending' });
    setTopics([]);

    try {
      const data = await blogService.generateTopics(config.category);
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
      const data = await blogService.generateBlog({
        topic,
        audience: config.audience,
        wordCount: config.wordCount,
        goal: config.goal,
        internalLinks: config.internalLinks,
      });
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

  return (
    <div className="app-container">
      <Header status={status} />

      <main className="content-grid">
        <ConfigSidebar 
          config={config} 
          setConfig={setConfig} 
          onGenerateTopics={handleGenerateTopics} 
          loading={loading.topics} 
        />

        <section className="workspace">
          {view === 'topics' ? (
            <TopicsGrid 
              topics={topics} 
              onSelectTopic={handleSelectTopic} 
            />
          ) : (
            <BlogViewer 
              selectedTopic={selectedTopic} 
              blogContent={blogContent} 
              onBack={() => setView('topics')} 
              loading={loading.blog} 
              onCopy={copyToClipboard} 
              onDownload={downloadMarkdown} 
            />
          )}
        </section>
      </main>

      <ParametersModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        pendingTopic={pendingTopic} 
        config={config} 
        setConfig={setConfig} 
        onFinalize={handleFinalizeGeneration} 
      />
    </div>
  );
}

export default App;
