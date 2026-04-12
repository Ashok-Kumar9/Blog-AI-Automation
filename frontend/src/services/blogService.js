import { API_BASE } from '../constants/api';

/**
 * Service for blog-related API calls
 */
export const blogService = {
  /**
   * Fetches trending topics based on a category
   * @param {string} category 
   * @returns {Promise<Object>}
   */
  async generateTopics(category) {
    const resp = await fetch(`${API_BASE}/api/generate-topics`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category }),
    });
    if (!resp.ok) throw new Error('Generation failed');
    return await resp.json();
  },

  /**
   * Fetches the full blog content for a given topic and configuration
   * @param {Object} params 
   * @returns {Promise<Object>}
   */
  async generateBlog(params) {
    const resp = await fetch(`${API_BASE}/api/generate-blog`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        topic: params.topic,
        target_audience: params.audience,
        word_count_goal: params.wordCount,
        specific_goal: params.goal,
        internal_links: params.internalLinks,
      }),
    });
    if (!resp.ok) throw new Error('Article generation failed');
    return await resp.json();
  },

  /**
   * Fetches the hero image for a given topic
   * @param {Object} params 
   * @returns {Promise<Object>}
   */
  async generateImage(params) {
    const resp = await fetch(`${API_BASE}/api/generate-image`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        blog_title: params.blog_title || params.topic,
      }),
    });
    if (!resp.ok) throw new Error('Image generation failed');
    return await resp.json();
  }
};
