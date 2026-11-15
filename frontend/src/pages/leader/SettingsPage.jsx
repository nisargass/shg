import React, { useState } from 'react';
import { Settings, ShieldCheck, Building2, Save, CheckCircle2 } from 'lucide-react';

const SettingsPage = () => {
  const [shgName, setShgName] = useState('Pragati Mahila Sangha');
  const [cluster, setCluster] = useState('Channapatna Craft Cluster');
  const [bankAccount, setBankAccount] = useState('State Bank of India - SBIN0040192 (A/C: 38921104821)');
  const [quorumThreshold, setQuorumThreshold] = useState('60%');
  const [saved, setSaved] = useState(false);

  const handleSave = (e) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">SHG Enterprise & Governance Settings</h1>
          <p className="page-subtitle">Configure group bank mapping, quorum rules, and NRLM federation link</p>
        </div>
      </div>

      {saved && (
        <div className="alert-banner success" style={{ marginBottom: '20px' }}>
          <CheckCircle2 size={18} />
          <span>Group governance settings updated successfully.</span>
        </div>
      )}

      <div className="card" style={{ maxWidth: '720px' }}>
        <form onSubmit={handleSave}>
          <div className="form-group">
            <label className="form-label">SHG Registered Name</label>
            <input type="text" className="form-control" value={shgName} onChange={(e) => setShgName(e.target.value)} required />
          </div>

          <div className="form-group">
            <label className="form-label">Cluster / Village / Gram Panchayat</label>
            <input type="text" className="form-control" value={cluster} onChange={(e) => setCluster(e.target.value)} required />
          </div>

          <div className="form-group">
            <label className="form-label">SHG Collective Bank Account (PFMS / Bank Dispatch Linked)</label>
            <input type="text" className="form-control" value={bankAccount} onChange={(e) => setBankAccount(e.target.value)} required />
          </div>

          <div className="form-group">
            <label className="form-label">Democratic Quorum Requirement for Labor Payout Release</label>
            <select className="form-control" value={quorumThreshold} onChange={(e) => setQuorumThreshold(e.target.value)}>
              <option value="50%">50% Simple Majority</option>
              <option value="60%">60% Standard NRLM Governance (Recommended)</option>
              <option value="75%">75% Supermajority</option>
              <option value="100%">100% Full Group Unanimity</option>
            </select>
            <span style={{ fontSize: '11.5px', color: '#5e7386', marginTop: '4px', display: 'block' }}>
              Requires at least 5 out of 8 working members to vote YES on verified batches before release.
            </span>
          </div>

          <div style={{ marginTop: '24px' }}>
            <button type="submit" className="btn btn-primary">
              <Save size={16} /> Save Configuration
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SettingsPage;

