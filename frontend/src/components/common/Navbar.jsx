import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import {
  Bell,
  ShoppingCart,
  User,
  LogOut,
  ChevronDown,
  Layers,
  Sparkles,
  ShieldCheck,
  CheckCircle,
  ExternalLink
} from 'lucide-react';
import './Navbar.css';

const Navbar = () => {
  const { user, logout, switchRole, notifications, markNotificationAsRead, cart } = useAuth();
  const isDemoMode = import.meta.env.DEV;
  const [roleMenuOpen, setRoleMenuOpen] = useState(false);
  const [notifMenuOpen, setNotifMenuOpen] = useState(false);
  const navigate = useNavigate();

  const unreadCount = notifications.filter((n) => !n.read).length;

  const roles = [
    { key: 'leader', label: 'SHG Leader Portal', path: '/leader', desc: 'Manage orders, members, allocations & finance' },
    { key: 'member', label: 'SHG Member Portal', path: '/member', desc: 'View tasks, earnings, voice assistant & quality' },
    { key: 'buyer', label: 'Wholesale Buyer Portal', path: '/buyer', desc: 'Create bulk orders & track live production' },
    { key: 'federation', label: 'Federation Officer', path: '/federation', desc: 'Cluster overview & Lakhpati Didi metrics' },
    { key: 'customer', label: 'Retail Customer View', path: '/marketplace', desc: 'Public artisanal marketplace' }
  ];

  const handleRoleSelect = (roleKey, path) => {
    switchRole(roleKey);
    setRoleMenuOpen(false);
    navigate(path);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="top-navbar">
      <div className="navbar-container">
        {/* Brand Logo & Tagline */}
        <div className="navbar-brand-section">
          <Link to="/" className="navbar-brand">
            <div className="brand-icon-box">
              <Sparkles size={20} className="brand-icon" />
            </div>
            <div className="brand-text">
              <span className="brand-title">SHG Saathi</span>
              <span className="brand-tagline">Agentic Rural Enterprise Platform</span>
            </div>
          </Link>

          {isDemoMode && <div className="demo-indicator-pill">
            <span className="demo-dot"></span>
            Demo Environment
          </div>}
        </div>

        {/* Global Navigation Links */}
        <nav className="navbar-nav-links">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/marketplace" className="nav-link">Artisan Marketplace</Link>
          <Link to="/about" className="nav-link">About NRLM</Link>
        </nav>

        {/* User & Role Controls */}
        <div className="navbar-actions">
          {/* Quick Role Switcher (Crucial for evaluation & demo testing) */}
          {isDemoMode && <div className="role-switcher-dropdown">
            <button
              className="role-switcher-btn"
              onClick={() => {
                setRoleMenuOpen(!roleMenuOpen);
                setNotifMenuOpen(false);
              }}
              title="Click to switch live persona"
            >
              <Layers size={16} className="text-secondary" />
              <div className="role-btn-text">
                <span className="role-btn-label">Active Role:</span>
                <span className="role-btn-current">{user?.role?.replace('_', ' ') || 'Guest'}</span>
              </div>
              <ChevronDown size={14} />
            </button>

            {roleMenuOpen && (
              <div className="dropdown-menu role-menu">
                <div className="dropdown-header">
                  <span>Switch Interactive Persona</span>
                  <small>Test role-isolated permissions</small>
                </div>
                {roles.map((r) => (
                  <button
                    key={r.key}
                    className={`dropdown-item role-item ${user?.role === r.key.toUpperCase() || (r.key === 'leader' && user?.role === 'SHG_LEADER') ? 'active' : ''}`}
                    onClick={() => handleRoleSelect(r.key, r.path)}
                  >
                    <div className="role-item-info">
                      <span className="role-item-name">{r.label}</span>
                      <span className="role-item-desc">{r.desc}</span>
                    </div>
                    {user?.role === r.key.toUpperCase() && <CheckCircle size={16} className="active-check" />}
                  </button>
                ))}
              </div>
            )}
          </div>}

          {/* Cart Icon for Retail Marketplace */}
          <Link to="/marketplace/cart" className="action-icon-btn" title="View Retail Cart">
            <ShoppingCart size={19} />
            {cart.length > 0 && <span className="action-badge">{cart.reduce((a, b) => a + b.quantity, 0)}</span>}
          </Link>

          {/* Notifications Bell */}
          <div className="notif-wrapper">
            <button
              className="action-icon-btn"
              onClick={() => {
                setNotifMenuOpen(!notifMenuOpen);
                setRoleMenuOpen(false);
              }}
              title="Notifications"
            >
              <Bell size={19} />
              {unreadCount > 0 && <span className="action-badge alert">{unreadCount}</span>}
            </button>

            {notifMenuOpen && (
              <div className="dropdown-menu notif-menu">
                <div className="dropdown-header">
                  <span>Notifications ({unreadCount} new)</span>
                  <small>Operational alerts</small>
                </div>
                <div className="notif-list">
                  {notifications.map((n) => (
                    <div
                      key={n.id}
                      className={`notif-item ${n.read ? 'read' : 'unread'}`}
                      onClick={() => markNotificationAsRead(n.id)}
                    >
                      <div className="notif-title-row">
                        <span className="notif-title">{n.title}</span>
                        <span className="notif-time">{n.time}</span>
                      </div>
                      <p className="notif-message">{n.message}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Logged in User Pill / Sign In */}
          {user ? (
            <div className="user-profile-badge">
              <div className="user-avatar-circle">
                {user.avatar ? (
                  <img src={user.avatar} alt={user.name} />
                ) : (
                  <User size={16} />
                )}
              </div>
              <div className="user-text-info">
                <span className="user-name">{user.name}</span>
                <span className="user-sub">{user.shgName || user.company || user.role}</span>
              </div>
              <button className="logout-btn" onClick={handleLogout} title="Sign Out">
                <LogOut size={16} />
              </button>
            </div>
          ) : (
            <Link to="/login" className="btn btn-secondary btn-sm">
              Sign In
            </Link>
          )}
        </div>
      </div>
    </header>
  );
};

export default Navbar;
