import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Sparkles, Lock, Mail, Eye, EyeOff, ArrowRight, ShieldCheck } from 'lucide-react';

const LoginPage = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const isDemoMode = import.meta.env.DEV;

  const [selectedRoleKey, setSelectedRoleKey] = useState('leader');
  const [email, setEmail] = useState(isDemoMode ? 'savitribai@pragati-shg.org' : '');
  const [password, setPassword] = useState(isDemoMode ? 'Saathi@2026' : '');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const demoAccounts = [
    { key: 'leader', label: 'SHG Leader', email: 'savitribai@pragati-shg.org', path: '/leader', desc: 'Savitribai Shinde (Pragati SHG)' },
    { key: 'member', label: 'SHG Member', email: 'sunita.rathod@shg.in', path: '/member', desc: 'Sunita Rathod (Stitching Artisan)' },
    { key: 'buyer', label: 'Wholesale Buyer', email: 'procurement@ecofab.in', path: '/buyer', desc: 'Arvind Deshmukh (EcoFab Ltd.)' },
    { key: 'federation', label: 'Federation Officer', email: 'deepa.narayan@ksrlps.gov.in', path: '/federation', desc: 'Deepa Narayan, KAS (NRLM)' },
    { key: 'customer', label: 'Retail Customer', email: 'pooja.h@gmail.com', path: '/marketplace', desc: 'Pooja Hegde (Artisan Shopper)' }
  ];

  const handleRoleTabClick = (account) => {
    setSelectedRoleKey(account.key);
    setEmail(account.email);
    setErrorMessage('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage('');

    try {
      const loggedInUser = isDemoMode
        ? await login(selectedRoleKey)
        : await login({ email, password });
      const rolePaths = {
        SHG_LEADER: '/leader',
        SHG_MEMBER: '/member',
        BUYER: '/buyer',
        FEDERATION_OFFICER: '/federation',
        CUSTOMER: '/marketplace',
      };
      navigate(rolePaths[loggedInUser.role] || '/');
    } catch (error) {
      setErrorMessage(error.response?.data?.detail || 'Authentication failed. Please verify your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: 'calc(100vh - 120px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '40px 20px', background: '#F5F7F9' }}>
      <div style={{ maxWidth: '520px', width: '100%', background: '#FFFFFF', borderRadius: '14px', border: '1px solid #DCE3E8', boxShadow: '0 10px 25px -5px rgba(18, 59, 93, 0.1)', overflow: 'hidden' }}>
        {/* Header */}
        <div style={{ background: '#123B5D', color: '#FFFFFF', padding: '28px 30px', textAlign: 'center' }}>
          <div style={{ width: '44px', height: '44px', background: 'rgba(22, 139, 128, 0.4)', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 12px' }}>
            <Sparkles size={24} color="#FFFFFF" />
          </div>
          <h2 style={{ color: '#FFFFFF', fontSize: '22px', fontWeight: '800' }}>SHG Saathi Portal</h2>
          <p style={{ color: 'rgba(255, 255, 255, 0.75)', fontSize: '13px', marginTop: '4px' }}>
            Sign in to access your authorized role dashboard
          </p>
        </div>

        {/* Demo Fast Selector */}
        {isDemoMode && <div style={{ padding: '20px 24px 10px', background: '#f8fafc', borderBottom: '1px solid #EEF2F5' }}>
          <span style={{ fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', color: '#5e7386', letterSpacing: '0.5px', display: 'block', marginBottom: '8px' }}>
            1-Click Demo Personas (Select to test role-isolation)
          </span>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(90px, 1fr))', gap: '6px' }}>
            {demoAccounts.map((acc) => (
              <button
                key={acc.key}
                type="button"
                onClick={() => handleRoleTabClick(acc)}
                style={{
                  padding: '7px 4px',
                  borderRadius: '6px',
                  fontSize: '11px',
                  fontWeight: '600',
                  border: selectedRoleKey === acc.key ? '1px solid #168B80' : '1px solid #DCE3E8',
                  background: selectedRoleKey === acc.key ? '#e6f6f4' : '#FFFFFF',
                  color: selectedRoleKey === acc.key ? '#123B5D' : '#5e7386',
                  cursor: 'pointer',
                  textAlign: 'center'
                }}
              >
                {acc.label}
              </button>
            ))}
          </div>
        </div>}

        {/* Form */}
        <form onSubmit={handleSubmit} style={{ padding: '24px 30px' }}>
          {errorMessage && (
            <div className="alert-banner danger" style={{ marginBottom: '16px', padding: '10px 14px' }}>
              {errorMessage}
            </div>
          )}

          <div className="form-group">
            <label className="form-label">Email or Phone Number</label>
            <div style={{ position: 'relative' }}>
              <input
                type="text"
                className="form-control"
                style={{ paddingLeft: '36px' }}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
              <Mail size={16} color="#899ba8" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <div style={{ position: 'relative' }}>
              <input
                type={showPassword ? 'text' : 'password'}
                className="form-control"
                style={{ paddingLeft: '36px', paddingRight: '36px' }}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <Lock size={16} color="#899ba8" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{ position: 'absolute', right: '12px', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: '#899ba8' }}
              >
                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', fontSize: '13px' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#5e7386', cursor: 'pointer' }}>
              <input type="checkbox" defaultChecked /> Remember login on this device
            </label>
            <span style={{ color: '#168B80', cursor: 'pointer', fontWeight: '500' }}>Forgot password?</span>
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            style={{ width: '100%', padding: '12px', fontSize: '15px' }}
            disabled={loading}
          >
            {loading ? 'Authenticating...' : isDemoMode ? `Enter as ${demoAccounts.find(a => a.key === selectedRoleKey)?.label || 'User'}` : 'Sign in'}
            <ArrowRight size={16} />
          </button>

          <div style={{ marginTop: '20px', padding: '12px', background: '#f8fafc', borderRadius: '8px', border: '1px solid #EEF2F5', fontSize: '12px', color: '#5e7386', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <ShieldCheck size={18} color="#168B80" style={{ flexShrink: 0 }} />
            <span>Role-Based Access Control verified by FastAPI JWT tokens. Never stores plain passwords.</span>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;

