import React from 'react';
import {
  Wallet,
  DollarSign,
  CheckCircle2,
  Clock,
  ShieldCheck,
  FileText,
  TrendingUp,
  Download
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

const MemberEarningsPage = () => {
  const { user } = useAuth();
  const memberName = user?.name || 'Sunita Rathod';

  const myEarningsData = {
    currentOrder: 'ORD-2026-104 (Cotton Tote Bags)',
    approvedUnits: 180,
    pieceRate: 32.0,
    grossEarnings: 5760.0,
    adjustments: 0.0,
    netCurrentPayable: 5760.0,
    payoutStatus: 'VOTING_IN_PROGRESS',
    bankAccount: 'State Bank of India - SBIN0040192 (A/C: ...4821)',
    history: [
      { id: 'PAY-2026-08', date: '2026-10-18', order: 'ORD-98 (Khadi Bags)', units: 140, rate: 30.0, net: 4200.0, status: 'DISBURSED_TO_BANK', utr: 'SBI20261018990142' },
      { id: 'PAY-2026-06', date: '2026-09-25', order: 'ORD-92 (Spice Pouches)', units: 160, rate: 28.0, net: 4480.0, status: 'DISBURSED_TO_BANK', utr: 'SBI20260925771029' },
      { id: 'PAY-2026-03', date: '2026-08-30', order: 'ORD-88 (Cotton Mask Liners)', units: 250, rate: 18.0, net: 4500.0, status: 'DISBURSED_TO_BANK', utr: 'SBI20260830441920' }
    ]
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">My Earnings Ledger</h1>
          <p className="page-subtitle">
            Personal compensation records &bull; Strictly private to {memberName}
          </p>
        </div>
      </div>

      {/* Private Ledger Alert */}
      <div className="alert-banner info" style={{ marginBottom: '24px' }}>
        <ShieldCheck size={20} />
        <div>
          <strong>Transparent Piece-Rate Accounting: Zero Hidden Cuts</strong>
          <p style={{ margin: '2px 0 0', fontSize: '13px' }}>
            Every rupee is computed as: <strong>Approved Units &times; Agreed Labor Rate</strong>. Your payments are disbursed directly into your Aadhaar-linked bank account without intermediary cash handling.
          </p>
        </div>
      </div>

      {/* Current Pending Milestone Card */}
      <div className="card" style={{ marginBottom: '24px', background: 'linear-gradient(135deg, #168B80 0%, #116860 100%)', color: '#FFFFFF' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <span className="badge" style={{ background: 'rgba(255,255,255,0.2)', color: '#FFFFFF', marginBottom: '6px' }}>
              Current Active Contract: {myEarningsData.currentOrder}
            </span>
            <div style={{ fontSize: '32px', fontWeight: '800', color: '#FFFFFF' }}>
              ₹{myEarningsData.netCurrentPayable.toLocaleString()}
            </div>
            <p style={{ fontSize: '13px', color: 'rgba(255, 255, 255, 0.85)', marginTop: '4px' }}>
              180 Quality-Approved Bags &times; ₹32.00 piece rate
            </p>
          </div>

          <div style={{ background: 'rgba(255,255,255,0.1)', padding: '16px', borderRadius: '10px', border: '1px solid rgba(255,255,255,0.2)', textAlign: 'right' }}>
            <span style={{ fontSize: '11px', textTransform: 'uppercase', color: 'rgba(255,255,255,0.8)' }}>Mapped Bank Account</span>
            <div style={{ fontSize: '13px', fontWeight: '700', color: '#FFFFFF', marginTop: '2px' }}>
              {myEarningsData.bankAccount}
            </div>
            <span className="badge" style={{ background: '#E6A23C', color: '#000000', fontWeight: '700', marginTop: '6px' }}>
              Awaiting Group Quorum Confirmation
            </span>
          </div>
        </div>
      </div>

      {/* Historical Payout Ledger */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">My Historical Bank Disbursement Statements</h3>
            <p className="card-subtitle">Previous cycles completed and credited to your account</p>
          </div>
          <button className="btn btn-sm btn-outline" onClick={() => alert('Downloading personal bank passbook slip...')}>
            <Download size={14} /> Download Passbook Slip
          </button>
        </div>
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Disbursement ID</th>
                <th>Order Description</th>
                <th>Approved Pieces</th>
                <th>Rate / Piece</th>
                <th>Net Bank Credit</th>
                <th>Bank UTR Ref No.</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {myEarningsData.history.map((h) => (
                <tr key={h.id}>
                  <td><strong>{h.id}</strong><div style={{ fontSize: '11px', color: '#5e7386' }}>{h.date}</div></td>
                  <td>{h.order}</td>
                  <td><strong>{h.units} units</strong></td>
                  <td>₹{h.rate.toFixed(2)}</td>
                  <td><strong style={{ color: '#168B80', fontSize: '14px' }}>₹{h.net.toLocaleString()}</strong></td>
                  <td><code style={{ fontSize: '11.5px', color: '#123B5D' }}>{h.utr}</code></td>
                  <td>
                    <span className="badge badge-success"><CheckCircle2 size={12} /> CREDITED</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default MemberEarningsPage;

