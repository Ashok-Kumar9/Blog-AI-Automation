import React, { useState, useEffect } from 'react';
import { blogService } from './services/blogService';
import { imageStorage } from './utils/imageStorage';
import './App.css';

// Components
import Header from './components/Header';
import EmptyState from './components/EmptyState';
import TopicsLoader from './components/TopicsLoader';
import TopicsGrid from './components/TopicsGrid';
import BlogViewer from './components/BlogViewer';
import ParametersModal from './components/ParametersModal';

function App() {
  // --- View: 'empty' | 'loading' | 'topics' | 'blog'
  const [view, setView] = useState(() => {
    const topics = localStorage.getItem('blog_topics');
    const parsed = topics ? JSON.parse(topics) : [];
    return parsed.length > 0 ? 'topics' : 'empty';
  });

  // --- Config (persisted)
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

  // --- Topics (persisted)
  const [topics, setTopics] = useState(() => {
    const saved = localStorage.getItem('blog_topics');
    return saved ? JSON.parse(saved) : [];
  });

  const [generatedBlogs, setGeneratedBlogs] = useState(() => {
    const saved = localStorage.getItem('blog_generated_map');
    return saved ? JSON.parse(saved) : {};
  });

  // --- Generated images map: { [topicString]: base64ImageString } (persisted via IndexedDB)
  const [generatedImages, setGeneratedImages] = useState({});
  const [imagesLoaded, setImagesLoaded] = useState(false);

  const [selectedTopic, setSelectedTopic] = useState(null);
  const [loadingBlog, setLoadingBlog] = useState(false);
  const [loadingImage, setLoadingImage] = useState(false);

  // --- Modal
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [pendingTopic, setPendingTopic] = useState(null);

  // --- Status
  const [status, setStatus] = useState({ text: 'Ready', type: 'success' });

  // --- Persistence effects
  useEffect(() => {
    localStorage.setItem('blog_config', JSON.stringify(config));
  }, [config]);

  useEffect(() => {
    localStorage.setItem('blog_topics', JSON.stringify(topics));
  }, [topics]);

  useEffect(() => {
    localStorage.setItem('blog_generated_map', JSON.stringify(generatedBlogs));
  }, [generatedBlogs]);

  useEffect(() => {
    imageStorage.getMap().then(map => {
      setGeneratedImages(map || {});
      setImagesLoaded(true);
      // Clean up old bloated localStorage key to free memory
      localStorage.removeItem('blog_generated_images_map');
    });
  }, []);

  useEffect(() => {
    if (imagesLoaded) {
      imageStorage.setMap(generatedImages);
    }
  }, [generatedImages, imagesLoaded]);

  // --- Handlers

  const handleGenerateTopics = async () => {
    if (!config.category.trim()) return;
    setView('loading');
    setStatus({ text: 'Researching topics...', type: 'pending' });
    // Clear previous topics and blogs before a fresh search
    setTopics([]);
    setGeneratedBlogs({});

    try {
      const data = await blogService.generateTopics(config.category);
      setTopics(data.topics);
      setStatus({ text: `Found ${data.topics.length} Topics`, type: 'success' });
      setView('topics');
    } catch (err) {
      console.error(err);
      setStatus({ text: 'Topics Generation Failed', type: 'error' });
      setView('empty');
    }
  };

  const handleSelectTopic = (topic) => {
    // If blog already generated — go straight to viewer
    if (generatedBlogs[topic]) {
      setSelectedTopic(topic);
      setView('blog');
      setStatus({ text: 'Blog Ready', type: 'success' });
      return;
    }
    // Otherwise open parameters modal
    setPendingTopic(topic);
    setIsModalOpen(true);
  };

  const handleFinalizeGeneration = async () => {
    if (!pendingTopic) return;
    const topic = pendingTopic;
    setIsModalOpen(false);
    setSelectedTopic(topic);
    setView('blog');
    setLoadingBlog(true);
    setStatus({ text: 'Crafting Blog...', type: 'pending' });

    try {
      const data = await blogService.generateBlog({
        topic,
        audience: config.audience,
        wordCount: config.wordCount,
        goal: config.goal,
        internalLinks: config.internalLinks,
      });
      setGeneratedBlogs(prev => ({ ...prev, [topic]: data.content }));
      setStatus({ text: 'Blog Generated!', type: 'success' });
    } catch (err) {
      console.error(err);
      setStatus({ text: 'Blog Creation Failed', type: 'error' });
    } finally {
      setLoadingBlog(false);
    }
  };

  const handleGenerateImage = async () => {
    if (!selectedTopic) return;
    setLoadingImage(true);
    setStatus({ text: 'Generating Image...', type: 'pending' });

    try {
      const data = await blogService.generateImage({
        blog_title: selectedTopic,
      });
      setGeneratedImages(prev => ({ ...prev, [selectedTopic]: data.image_base64 }));
      setStatus({ text: 'Image Generated!', type: 'success' });
    } catch (err) {
      console.error(err);
      setStatus({ text: 'Image Creation Failed', type: 'error' });
    } finally {
      setLoadingImage(false);
    }
  };

  // Regenerate: open modal for an already-generated topic
  const handleRegenerate = () => {
    setPendingTopic(selectedTopic);
    setIsModalOpen(true);
  };

  const copyToClipboard = () => {
    const content = generatedBlogs[selectedTopic] || '';
    navigator.clipboard.writeText(content);
    const prev = status.text;
    setStatus({ text: 'Copied!', type: 'success' });
    setTimeout(() => setStatus({ text: prev, type: 'success' }), 2000);
  };

  const downloadMarkdown = () => {
    const content = generatedBlogs[selectedTopic] || '';
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${selectedTopic?.toLowerCase().replace(/ /g, '_')}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadImage = () => {
    const base64Data = generatedImages[selectedTopic];
    if (!base64Data) return;
    const a = document.createElement('a');
    a.href = `data:image/png;base64,${base64Data}`;
    a.download = `${selectedTopic?.toLowerCase().replace(/ /g, '_')}_hero.png`;
    a.click();
  };

  return (
    <div className={`app-container ${view === 'empty' || view === 'loading' ? 'app-container--centered' : ''}`}>
      {/* Header only shows on topics/blog views */}
      {(view === 'topics' || view === 'blog') && <Header status={status} />}

      {view === 'empty' && (
        <EmptyState
          category={config.category}
          onCategoryChange={val => setConfig({ ...config, category: val })}
          onGenerate={handleGenerateTopics}
          loading={false}
        />
      )}

      {view === 'loading' && <TopicsLoader category={config.category} />}

      {view === 'topics' && (
        <TopicsGrid
          topics={topics}
          generatedBlogs={generatedBlogs}
          onSelectTopic={handleSelectTopic}
          onNewCategory={() => {
            setConfig(prev => ({ ...prev, category: '' }));
            setView('empty');
          }}
          category={config.category}
        />
      )}

      {view === 'blog' && (
        <BlogViewer
          selectedTopic={selectedTopic}
          blogContent={generatedBlogs[selectedTopic] || ''}
          topicImage={generatedImages[selectedTopic] || null}
          loadingImage={loadingImage}
          onGenerateImage={handleGenerateImage}
          onDownloadImage={downloadImage}
          onBack={() => setView('topics')}
          loading={loadingBlog}
          onCopy={copyToClipboard}
          onDownload={downloadMarkdown}
          onRegenerate={handleRegenerate}
        />
      )}

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
