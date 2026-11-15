import React, { createContext, useContext, useState, useEffect } from 'react';
import { DEMO_USERS, DEMO_NOTIFICATIONS } from '../mock/mockData';
import apiClient from '../api/apiClient';

const AuthContext = createContext(null);
const isDemoMode = import.meta.env.DEV;

const normalizeUser = (user) => ({
  ...user,
  name: user.name || user.full_name,
  shgName: user.shgName || user.shg_name,
});

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    if (!isDemoMode) return null;
    const saved = localStorage.getItem('shg_auth_user');
    if (saved) {
      try { return JSON.parse(saved); } catch (error) {
        console.warn('Could not restore the saved demo user.', error);
      }
    }
    return DEMO_USERS.leader; // Default to leader
  });

  const [notifications, setNotifications] = useState(isDemoMode ? DEMO_NOTIFICATIONS : []);
  const [cart, setCart] = useState(() => {
    const savedCart = localStorage.getItem('shg_retail_cart');
    if (savedCart) {
      try { return JSON.parse(savedCart); } catch (e) { /* ignore */ }
    }
    return [];
  });

  useEffect(() => {
    if (user) {
      localStorage.setItem('shg_auth_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('shg_auth_user');
    }
  }, [user]);

  useEffect(() => {
    if (isDemoMode) return;
    const token = localStorage.getItem('authToken');
    if (!token || token.startsWith('demo-jwt-token-')) {
      localStorage.removeItem('authToken');
      return;
    }

    apiClient.get('/auth/me')
      .then((currentUser) => setUser(normalizeUser(currentUser)))
      .catch((error) => {
        console.warn('Could not restore the authenticated session.', error);
        localStorage.removeItem('authToken');
        setUser(null);
      });
  }, []);

  useEffect(() => {
    localStorage.setItem('shg_retail_cart', JSON.stringify(cart));
  }, [cart]);

  const login = async (credentialsOrRoleKey = {}) => {
    if (typeof credentialsOrRoleKey === 'string') {
      if (!isDemoMode) {
        throw new Error('Demo sign-in is disabled in production.');
      }
      const targetUser = DEMO_USERS[credentialsOrRoleKey] || DEMO_USERS.leader;
      setUser(targetUser);
      localStorage.setItem('authToken', `demo-jwt-token-${targetUser.role.toLowerCase()}`);
      return targetUser;
    }

    const response = await apiClient.post('/auth/login/json', credentialsOrRoleKey);
    if (!response.access_token || !response.user) {
      throw new Error('The authentication server returned an invalid response.');
    }
    localStorage.setItem('authToken', response.access_token);
    const authenticatedUser = normalizeUser(response.user);
    setUser(authenticatedUser);
    return authenticatedUser;
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('shg_auth_user');
    localStorage.removeItem('authToken');
  };

  const switchRole = (roleKey) => {
    return login(roleKey);
  };

  const markNotificationAsRead = (id) => {
    setNotifications(prev => prev.map(n => n.id === id ? { ...n, read: true } : n));
  };

  const addToCart = (product) => {
    setCart(prev => {
      const existing = prev.find(item => item.id === product.id);
      if (existing) {
        return prev.map(item => item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item);
      }
      return [...prev, { ...product, quantity: 1 }];
    });
  };

  const removeFromCart = (productId) => {
    setCart(prev => prev.filter(item => item.id !== productId));
  };

  const clearCart = () => setCart([]);

  return (
    <AuthContext.Provider value={{
      user,
      login,
      logout,
      switchRole,
      notifications,
      markNotificationAsRead,
      cart,
      addToCart,
      removeFromCart,
      clearCart
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

