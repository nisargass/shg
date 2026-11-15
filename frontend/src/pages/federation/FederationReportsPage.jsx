import React from 'react';
import { Award, TrendingUp, CheckCircle2, Download, DollarSign } from 'lucide-react';

const FederationReportsPage = () => {
  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Lakhpati Didi Mission Progress & Impact Analysis</h1>
          <p className="page-subtitle">Ministry of Rural Development &bull; Ramanagara Cluster Report 2026</p>
        </div>
        <div className="page-actions">
          <button className="btn btn-primary" onClick={() => alert('Downloading official Lakhpati Didi Certification register...')}>
            <Download size={16} /> Download Certified Registry
          </button>
        </div>
      </div>

      <div className="grid grid-cols-3" style={{ gap: '20px', marginBottom: '24px' }}>
        <div className="card">
          <span style={{ fontSize: '12px', color: '#5e7386' }}>Verified Lakhpati Members</span>
          <div style={{ fontSize: '28px', fontWeight: '800', color: '#168B80', margin: '4px 0' }}>42 Members</div>
          <div style={{ fontSize: '12px', color: '#123B5D' }}>Earning &gt; ₹1,00,000 annually via bulk crafts</div>
        </div>

        <div className="card">
          <span style={{ fontSize: '12px', color: '#5e7386' }}>Target for March 2027</span>
          <div style={{ fontSize: '28px', fontWeight: '800', color: '#123B5D', margin: '4px 0' }}>80 Members</div>
          <div style={{ fontSize: '12px', color: '#5e7386' }}>52.5% target achieved in year 1</div>
        </div>

        <div className="card">
          <span style={{ fontSize: '12px', color: '#5e7386' }}>Cumulative Labor Payouts</span>
          <div style={{ fontSize: '28px', fontWeight: '800', color: '#E6A23C', margin: '4px 0' }}>₹24.8 Lakhs</div>
          <div style={{ fontSize: '12px', color: '#168B80' }}>100% direct bank account credit</div>
        </div>
      </div>

      <div className="card">
        <h3 style={{ fontSize: '16px', color: '#123B5D', marginBottom: '12px' }}>Methodology & Impact Assessment</h3>
        <p style={{ fontSize: '13.5px', color: '#5e7386', lineHeight: '1.6' }}>
          SHG Saathi's integration of fair piece-rate work allocation, anti-underpricing calculators, and automated quorum payouts has eliminated middleman leakages. Artisan income has increased by an average of 34% compared to verbal contract arrangements.
        </p>
      </div>
    </div>
  );
};

export default FederationReportsPage;

