import React, { useState, useEffect } from 'react';
import { Sparkles } from 'lucide-react';

const STAGES = [
  'Scanning the web for trends...',
  'Analysing SEO opportunities...',
  'Ranking by search potential...',
  'Curating the best topics...',
  'Almost there...',
];

const TopicsLoader = ({ category }) => {
  const [stageIndex, setStageIndex] = useState(0);
  const [dots, setDots] = useState('');

  useEffect(() => {
    const stageTimer = setInterval(() => {
      setStageIndex(prev => Math.min(prev + 1, STAGES.length - 1));
    }, 1600);
    return () => clearInterval(stageTimer);
  }, []);

  useEffect(() => {
    const dotsTimer = setInterval(() => {
      setDots(prev => (prev.length >= 3 ? '' : prev + '.'));
    }, 400);
    return () => clearInterval(dotsTimer);
  }, []);

  return (
    <div className="topics-loader">
      <div className="topics-loader-inner">
        <div className="loader-orb">
          <Sparkles size={36} className="loader-orb-icon" />
          <div className="loader-ring" />
          <div className="loader-ring loader-ring--2" />
        </div>

        <div className="loader-category-badge">
          {category}
        </div>

        <h2 className="loader-heading">Finding the best topics</h2>
        <p className="loader-stage">
          {STAGES[stageIndex]}<span className="loader-dots">{dots}</span>
        </p>

        <div className="loader-progress">
          <div
            className="loader-progress-fill"
            style={{ width: `${((stageIndex + 1) / STAGES.length) * 100}%` }}
          />
        </div>

        <div className="loader-steps">
          {STAGES.map((s, i) => (
            <div
              key={i}
              className={`loader-step ${i <= stageIndex ? 'loader-step--done' : ''} ${i === stageIndex ? 'loader-step--active' : ''}`}
            >
              <span className="loader-step-dot" />
              <span className="loader-step-label">{s.replace('...', '')}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TopicsLoader;
