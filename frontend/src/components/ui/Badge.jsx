import React from 'react';

/**
 * Badge component for status indicators
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Badge content
 * @param {string} props.variant - Badge variant (primary, success, warning, danger)
 * @param {string} props.className - Additional CSS classes
 */
const Badge = ({
  children,
  variant = 'primary',
  className = '',
  ...props
}) => {
  // Variant classes
  const variantClasses = {
    primary: 'badge-primary',
    success: 'badge-success',
    warning: 'badge-warning',
    danger: 'badge-danger',
  };

  return (
    <span
      className={`
        badge
        ${variantClasses[variant]}
        ${className}
      `.trim()}
      {...props}
    >
      {children}
    </span>
  );
};

export default Badge;
