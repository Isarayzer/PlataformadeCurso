import React from 'react';

/**
 * Loading spinner component
 * @param {Object} props - Component props
 * @param {string} props.size - Spinner size (sm, md, lg)
 * @param {string} props.className - Additional CSS classes
 */
const Loading = ({ size = 'md', className = '' }) => {
  // Size classes
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  return (
    <div className={`spinner ${sizeClasses[size]} ${className}`} />
  );
};

/**
 * Full page loading component
 */
export const LoadingPage = ({ message = 'Loading...' }) => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <Loading size="lg" />
      <p className="mt-4 text-neutral-600">{message}</p>
    </div>
  );
};

export default Loading;
