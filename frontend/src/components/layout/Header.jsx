import React from 'react';
import { Menu, Search, Bell, User } from 'lucide-react';

/**
 * Header component with search and user menu
 */
const Header = ({ onMenuClick }) => {
  return (
    <header className="h-16 bg-white border-b border-neutral-200 px-6 flex items-center justify-between sticky top-0 z-30">
      {/* Left section */}
      <div className="flex items-center gap-4">
        {/* Mobile menu button */}
        <button
          onClick={onMenuClick}
          className="lg:hidden text-neutral-600 hover:text-neutral-900 transition-colors"
        >
          <Menu size={24} />
        </button>

        {/* Search bar */}
        <div className="relative hidden md:block">
          <Search
            className="absolute left-3 top-1/2 -translate-y-1/2 text-neutral-400"
            size={20}
          />
          <input
            type="text"
            placeholder="Search courses, videos..."
            className="pl-10 pr-4 py-2 w-64 lg:w-96 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
          />
        </div>
      </div>

      {/* Right section */}
      <div className="flex items-center gap-4">
        {/* Notifications */}
        <button className="relative p-2 text-neutral-600 hover:text-neutral-900 hover:bg-neutral-100 rounded-lg transition-colors">
          <Bell size={22} />
          {/* Notification badge */}
          <span className="absolute top-1 right-1 w-2 h-2 bg-danger-500 rounded-full" />
        </button>

        {/* User menu */}
        <button className="flex items-center gap-3 p-2 hover:bg-neutral-100 rounded-lg transition-colors">
          <div className="w-8 h-8 bg-gradient-primary rounded-full flex items-center justify-center">
            <User size={18} className="text-white" />
          </div>
          <div className="hidden md:block text-left">
            <p className="text-sm font-medium text-neutral-900">John Doe</p>
            <p className="text-xs text-neutral-500">Instructor</p>
          </div>
        </button>
      </div>
    </header>
  );
};

export default Header;
