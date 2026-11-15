import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Sparkles, Heart } from 'lucide-react';

const Footer = () => {
  return (
    <footer style={{ backgroundColor: '#0c273e', color: '#cbd5e1', padding: '40px 24px 24px', marginTop: 'auto', borderTop: '1px solid #1e3a5f' }}>
      <div style={{ maxWidth: '1440px', margin: '0 auto', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '32px', marginBottom: '32px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#FFFFFF', marginBottom: '12px' }}>
            <Sparkles size={20} color="#168B80" />
            <span style={{ fontSize: '18px', fontWeight: '800' }}>SHG Saathi</span>
          </div>
          <p style={{ fontSize: '13px', lineHeight: '1.6', color: '#94a3b8' }}>
            Agentic AI-powered Business Management, Fair Work Allocation, Production Coordination and Transparent Payout Platform for Women's Self-Help Groups.
          </p>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginTop: '12px', fontSize: '12px', color: '#E6A23C' }}>
            <ShieldCheck size={16} />
            <span>Empowering Rural Artisans & Lakhpati Didis</span>
          </div>
        </div>

        <div>
          <h4 style={{ color: '#FFFFFF', fontSize: '14px', marginBottom: '14px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Core Platform</h4>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '13px' }}>
            <li><Link to="/leader" style={{ color: '#94a3b8' }}>Leader Operations</Link></li>
            <li><Link to="/leader/allocation" style={{ color: '#94a3b8' }}>AI Work Allocation</Link></li>
            <li><Link to="/leader/quality" style={{ color: '#94a3b8' }}>Computer Vision QC</Link></li>
            <li><Link to="/leader/finance" style={{ color: '#94a3b8' }}>Transparent Group Payouts</Link></li>
            <li><Link to="/leader/pricing" style={{ color: '#94a3b8' }}>Cost & Margin Calculator</Link></li>
          </ul>
        </div>

        <div>
          <h4 style={{ color: '#FFFFFF', fontSize: '14px', marginBottom: '14px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Portals</h4>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '13px' }}>
            <li><Link to="/member" style={{ color: '#94a3b8' }}>SHG Member Portal</Link></li>
            <li><Link to="/member/assistant" style={{ color: '#94a3b8' }}>Multilingual Voice Saathi</Link></li>
            <li><Link to="/buyer" style={{ color: '#94a3b8' }}>Wholesale Buyer Portal</Link></li>
            <li><Link to="/federation" style={{ color: '#94a3b8' }}>NRLM Federation Dashboard</Link></li>
            <li><Link to="/marketplace" style={{ color: '#94a3b8' }}>Public Artisan Marketplace</Link></li>
          </ul>
        </div>

        <div>
          <h4 style={{ color: '#FFFFFF', fontSize: '14px', marginBottom: '14px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Security & Governance</h4>
          <p style={{ fontSize: '12.5px', color: '#94a3b8', lineHeight: '1.6' }}>
            All member earnings calculations, allocation recommendations, and disbursements require human confirmation and verifiable 60% group quorum voting before execution.
          </p>
          <div style={{ marginTop: '12px', fontSize: '11.5px', color: '#64748b' }}>
            FastAPI Backend + PostgreSQL + AI Microservice Architecture
          </div>
        </div>
      </div>

      <div style={{ maxWidth: '1440px', margin: '0 auto', paddingTop: '20px', borderTop: '1px solid rgba(255, 255, 255, 0.08)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px', fontSize: '12px', color: '#64748b' }}>
        <span>&copy; {new Date().getFullYear()} SHG Saathi. Dedicated to Women's Economic Independence.</span>
        <span>Built with care for Hackathon 2026</span>
      </div>
    </footer>
  );
};

export default Footer;
