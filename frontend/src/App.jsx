import React from 'react';
import { useAuthStore } from './store';
import LandingPage from './pages/LandingPage';
import AuthPage from './pages/AuthPage';
import DashboardPage from './pages/DashboardPage';
import './App.css';

function App() {
  const { isAuthenticated } = useAuthStore();

  if (!isAuthenticated) {
    return <LandingPage />;
  }

  return isAuthenticated ? <DashboardPage /> : <AuthPage />;
}

export default App;
