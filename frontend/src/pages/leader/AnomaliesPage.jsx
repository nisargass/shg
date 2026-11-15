import React, { useState } from 'react';
import {
  ShieldAlert,
  AlertTriangle,
  CheckCircle2,
  FileText,
  Clock,
  Search,
  Check,
  Eye
} from 'lucide-react';
import { DEMO_ANOMALY_ALERTS } from '../../mock/mockData';

const AnomaliesPage = () => {
  const [alerts, setAlerts] = useState(DEMO_ANOMALY_ALERTS);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [resolutionNote, setResolutionNote] = useState('');

  const handleResolve = (id) => {
    setAlerts(alerts.map((a) => a.id === id ? { ...a, status: 'RESOLVED', explanation: resolutionNote || 'Resolved by Leader.' } : a));
    setSelectedAlert(null);
    setResolutionNote('');
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h1 className="page-title">Financial Transparency & Anomaly Review</h1>
            <span className="demo-badge">Audit AI Engine</span>
          </div>
          <p className="page-subtitle">
            Automated verification of supplier invoices, cutting scrap variance, and post-approval transaction stability
          </p>
        </div>
      </div>

      <div className="alert-banner info" style={{ marginBottom: '24px' }}>
        <ShieldAlert size={20} />
        <div>
          <strong>Responsible AI Policy: Anomaly Detection is an Assistive Review Filter</strong>
          <p style={{ margin: '2px 0 0', fontSize: '13px' }}>
            AI alerts identify mathematical variances, duplicate invoice numbers, or sudden scrap spikes. They are designed to prompt constructive investigation, never to make automatic accusations.
          </p>
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {alerts.map((item) => (
          <div key={item.id} className="card" style={{ padding: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '12px' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                  <span className="badge badge-primary">{item.id}</span>
                  <span className={`badge ${item.severity === 'HIGH' ? 'badge-alert' : 'badge-accent'}`}>
                    {item.severity} RISK
                  </span>
                  <span className={`badge ${item.status === 'RESOLVED' ? 'badge-success' : 'badge-neutral'}`}>
                    {item.status.replace('_', ' ')}
                  </span>
                </div>
                <h3 style={{ fontSize: '16px', color: '#123B5D' }}>{item.title}</h3>
                <div style={{ fontSize: '12.5px', color: '#5e7386', marginTop: '2px' }}>
                  Transaction: <strong>{item.relatedTransaction}</strong> &bull; Detected on: {item.detectedDate}
                </div>
              </div>

              <div>
                {item.status !== 'RESOLVED' ? (
                  <button className="btn btn-sm btn-secondary" onClick={() => setSelectedAlert(item)}>
                    Investigate & Resolve
                  </button>
                ) : (
                  <span style={{ fontSize: '12px', color: '#168B80', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <CheckCircle2 size={15} /> Case Closed
                  </span>
                )}
              </div>
            </div>

            <div style={{ background: '#F8FAFC', padding: '14px', borderRadius: '8px', border: '1px solid #EEF2F5', marginTop: '14px', fontSize: '13px' }}>
              <p style={{ margin: '0 0 8px', color: '#243746' }}>{item.description}</p>
              <div style={{ fontSize: '12px', color: '#123B5D', fontStyle: 'italic' }}>
                <strong>Audit Explanation:</strong> {item.explanation}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Resolution Modal */}
      {selectedAlert && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3 style={{ fontSize: '16px', color: '#123B5D' }}>Resolve Financial Flag: {selectedAlert.id}</h3>
              <button onClick={() => setSelectedAlert(null)} style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer' }}>&times;</button>
            </div>
            <div className="modal-body">
              <div style={{ fontSize: '13px', color: '#243746', marginBottom: '14px' }}>
                <strong>Issue:</strong> {selectedAlert.title}
              </div>
              <div className="form-group">
                <label className="form-label">Leader Verification Notes & Actions Taken</label>
                <textarea
                  className="form-control"
                  rows="3"
                  value={resolutionNote}
                  onChange={(e) => setResolutionNote(e.target.value)}
                  placeholder="e.g., Contacted supplier accounts team; confirmed duplicate bill was voided and credit note issued..."
                ></textarea>
              </div>
            </div>
            <div className="modal-footer">
              <button className="btn btn-outline" onClick={() => setSelectedAlert(null)}>Cancel</button>
              <button className="btn btn-primary" onClick={() => handleResolve(selectedAlert.id)}>
                <Check size={16} /> Mark Anomaly as Resolved
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AnomaliesPage;

