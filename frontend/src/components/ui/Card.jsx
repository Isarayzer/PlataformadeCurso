import React from 'react';

/**
 * Card component for content containers
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Card content
 * @param {string} props.title - Card title
 * @param {React.ReactNode} props.actions - Action buttons/elements
 * @param {boolean} props.hover - Whether card has hover effect
 * @param {string} props.className - Additional CSS classes
 */
const Card = ({
  children,
  title,
  actions,
  hover = false,
  className = '',
  ...props
}) => {
  return (
    <div
      className={`
        card
        ${hover ? 'card-hover cursor-pointer' : ''}
        ${className}
      `.trim()}
      {...props}
    >
      {/* Card header */}
      {(title || actions) && (
        <div className="flex items-center justify-between mb-4">
          {title && (
            <h3 className="text-lg font-semibold text-neutral-900">
              {title}
            </h3>
          )}
          {actions && (
            <div className="flex items-center gap-2">
              {actions}
            </div>
          )}
        </div>
      )}

      {/* Card content */}
      <div>{children}</div>
    </div>
  );
};

export default Card;
