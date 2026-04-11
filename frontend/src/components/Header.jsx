import React from 'react';
import { Loader2, AlertCircle, CheckCircle2 } from 'lucide-react';

const Header = ({ status }) => {
  const renderStatusIcon = () => {
    if (status.type === 'pending') return <Loader2 className="spinner" size={16} color="var(--warning-color)" />;
    if (status.type === 'error') return <AlertCircle color="var(--error-color)" size={16} />;
    return <CheckCircle2 color="var(--success-color)" size={16} />;
  };

  return (
    <header className="main-header">
      <div className="brand-name">Blog Automation <span className="accent">AI</span></div>
      <div className="status-badge">
        {renderStatusIcon()}
        <span>{status.text}</span>
      </div>
    </header>
  );
};

export default Header;
