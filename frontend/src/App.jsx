import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './components/layout/MainLayout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';

/**
 * Main application component with routing
 */
function App() {
  // TODO: Implement proper authentication state management
  const isAuthenticated = false; // This will be replaced with actual auth state

  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected routes with main layout */}
        <Route element={<MainLayout />}>
          <Route path="/" element={<Dashboard />} />

          {/* Placeholder routes - will be implemented later */}
          <Route path="/videos" element={<div className="text-center text-neutral-600">Videos page coming soon...</div>} />
          <Route path="/courses" element={<div className="text-center text-neutral-600">Courses page coming soon...</div>} />
          <Route path="/categories" element={<div className="text-center text-neutral-600">Categories page coming soon...</div>} />
          <Route path="/learning-paths" element={<div className="text-center text-neutral-600">Learning Paths page coming soon...</div>} />
          <Route path="/settings" element={<div className="text-center text-neutral-600">Settings page coming soon...</div>} />
        </Route>

        {/* Catch all - redirect to home */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
