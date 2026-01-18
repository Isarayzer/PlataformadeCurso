import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Video,
  BookOpen,
  FolderTree,
  GitBranch,
  Settings,
  LogOut,
} from 'lucide-react';

/**
 * Sidebar navigation component
 */
const Sidebar = ({ isOpen, onClose }) => {
  const location = useLocation();

  // Navigation items
  const navItems = [
    {
      name: 'Dashboard',
      path: '/',
      icon: LayoutDashboard,
    },
    {
      name: 'Videos',
      path: '/videos',
      icon: Video,
    },
    {
      name: 'Courses',
      path: '/courses',
      icon: BookOpen,
    },
    {
      name: 'Categories',
      path: '/categories',
      icon: FolderTree,
    },
    {
      name: 'Learning Paths',
      path: '/learning-paths',
      icon: GitBranch,
    },
  ];

  // Check if current path is active
  const isActive = (path) => {
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 lg:hidden z-40"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed top-0 left-0 z-50 h-full w-64 bg-white border-r border-neutral-200
          transition-transform duration-300 ease-in-out
          lg:translate-x-0 lg:static lg:z-auto
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
      >
        {/* Logo */}
        <div className="h-16 flex items-center px-6 border-b border-neutral-200">
          <h1 className="text-2xl font-bold text-gradient font-display">
            CourseHub
          </h1>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 py-6 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.path);

            return (
              <Link
                key={item.path}
                to={item.path}
                onClick={onClose}
                className={`
                  flex items-center gap-3 px-4 py-3 rounded-lg
                  transition-all duration-200
                  ${
                    active
                      ? 'bg-primary-50 text-primary-700 font-medium'
                      : 'text-neutral-600 hover:bg-neutral-50 hover:text-neutral-900'
                  }
                `}
              >
                <Icon size={20} />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>

        {/* Bottom actions */}
        <div className="border-t border-neutral-200 p-4 space-y-1">
          <Link
            to="/settings"
            onClick={onClose}
            className={`
              flex items-center gap-3 px-4 py-3 rounded-lg
              transition-all duration-200
              ${
                isActive('/settings')
                  ? 'bg-primary-50 text-primary-700 font-medium'
                  : 'text-neutral-600 hover:bg-neutral-50 hover:text-neutral-900'
              }
            `}
          >
            <Settings size={20} />
            <span>Settings</span>
          </Link>

          <button
            onClick={() => {
              // TODO: Implement logout
              console.log('Logout');
            }}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-neutral-600 hover:bg-danger-50 hover:text-danger-600 transition-all duration-200"
          >
            <LogOut size={20} />
            <span>Logout</span>
          </button>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
