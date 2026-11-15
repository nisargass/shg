import React, { useState } from 'react';
import {
  Wallet,
  ShieldCheck,
  CheckCircle2,
  Clock,
  AlertTriangle,
  Users,
  Vote,
  DollarSign,
  ArrowRight,
  FileCheck2,
  FileText
} from 'lucide-react';
import { DEMO_PAYOUT_WORKFLOW } from '../../mock/mockData';
import { financialApi } from '../../api/services';

const FinancePage = () => {
  const [workflow, setWorkflow] = useState(DEMO_PAYOUT_WORKFLOW);
  const [leaderConfirmed, setLeaderConfirmed] = useState(false);
  const [actionNotice, setActionNotice] = useState('');

  const quorumReached = workflow.votesReceived >= workflow.quorumRequired;

  const handleLeaderConfirm = async () => {
    if (!quorumReached) {
      alert(`Cannot confirm payout: Requires ${workflow.quorumRequired} affirmative member quorum votes. Currently has ${workflow.votesReceived}.`);
      return;
    }
    await financialApi.confirmPayout(workflow.orderId);
    setLeaderConfirmed(true);
    setActionNotice('Quorum-approved member payout confirmed and registered in bank dispatch ledger.');
    setTimeout(() => setActionNotice(''), 6000);
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h1 className="page-title">Financial Transparency & Group-Approved Payouts</h1>
            <span className="demo-badge">Quorum Protected</span>
          </div>
          <p className="page-subtitle">
            Democratic, auditable member piece-rate distribution requiring 60% affirmative member voting before disbursement
          </p>
        </div>
        <div className="page-actions">
          <button className="btn btn-outline" onClick={() => alert('Exporting full audit trail report to CSV/PDF...')}>
            <FileText size={16} /> Export Audit Ledger
          </button>
        </div>
      </div>

      {actionNotice && (
        <div className="alert-banner success" style={{ marginBottom: '20px' }}>
          <CheckCircle2 size={20} />
          <span>{actionNotice}</span>
        </div>
      )}

      {/* Quorum Governance Card */}
      <div className="card" style={{ marginBottom: '24px', background: 'linear-gradient(135deg, #123B5D 0%, #174b75 100%)', color: '#FFFFFF' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '20px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
              <span className="badge" style={{ background: 'rgba(255,255,255,0.2)', color: '#FFFFFF' }}>{workflow.orderId}</span>
              <span className="badge" style={{ background: '#E6A23C', color: '#000000', fontWeight: '800' }}>{workflow.batchMilestone}</span>
            </div>
            <h2 style={{ fontSize: '22px', color: '#FFFFFF' }}>Total Group Milestone Payout: ₹{workflow.totalApprovedAmount.toLocaleString()}</h2>
            <p style={{ fontSize: '13px', color: 'rgba(255,255,255,0.8)', marginTop: '4px' }}>
              600 Quality-Approved Cotton Tote Bags @ agreed ₹32.00 piece-rate labor compensation
            </p>
          </div>

          <div style={{ background: 'rgba(255, 255, 255, 0.1)', padding: '16px 20px', borderRadius: '10px', textAlign: 'center', border: '1px solid rgba(255, 255, 255, 0.2)' }}>
            <div style={{ fontSize: '11px', textTransform: 'uppercase', color: 'rgba(255,255,255,0.7)', fontWeight: '700' }}>
              Quorum Voting Status
            </div>
            <div style={{ fontSize: '26px', fontWeight: '800', color: quorumReached ? '#22C55E' : '#E6A23C', margin: '4px 0' }}>
              {workflow.votesReceived} / {workflow.quorumRequired} Votes
            </div>
            <span style={{ fontSize: '11.5px', color: 'rgba(255,255,255,0.9)' }}>
              {quorumReached ? 'Quorum Threshold Achieved' : 'Awaiting 1 More Member Vote'}
            </span>
          </div>
        </div>
      </div>

      {/* Member-Wise Payout Breakdown Table */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <div>
            <h3 className="card-title">Transparent Member Labor Compensation Breakdown</h3>
            <p className="card-subtitle">
              Calculated strictly from verified quality inspection records with democratic voting confirmation
            </p>
          </div>
        </div>
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Artisan Member</th>
                <th>Quality-Approved Units</th>
                <th>Agreed Piece Rate</th>
                <th>Gross Earnings</th>
                <th>Deductions / Tool Loan</th>
                <th>Net Payable Amount</th>
                <th>Member Quorum Vote</th>
                <th>Vote Recorded At</th>
              </tr>
            </thead>
            <tbody>
              {workflow.membersPayoutList.map((m) => (
                <tr key={m.memberId}>
                  <td>
                    <strong>{m.memberName}</strong>
                    <div style={{ fontSize: '11px', color: '#5e7386' }}>{m.memberId}</div>
                  </td>
                  <td><strong>{m.approvedUnits} units</strong></td>
                  <td>₹{m.pieceRate.toFixed(2)}</td>
                  <td>₹{m.grossEarnings.toLocaleString()}</td>
                  <td>₹{m.toolSupportDeduction.toFixed(2)}</td>
                  <td>
                    <strong style={{ fontSize: '15px', color: '#168B80' }}>
                      ₹{m.netPayable.toLocaleString()}
                    </strong>
                  </td>
                  <td>
                    {m.voted ? (
                      <span className="badge badge-success">
                        <CheckCircle2 size={13} /> APPROVED
                      </span>
                    ) : (
                      <span className="badge badge-accent">
                        <Clock size={13} /> VOTE PENDING
                      </span>
                    )}
                  </td>
                  <td>
                    <span style={{ fontSize: '12px', color: '#5e7386' }}>{m.voteTimestamp || '—'}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Leader Final Confirmation Action Bar */}
      <div className="card" style={{ border: '2px solid #DCE3E8' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <h3 style={{ fontSize: '15px', color: '#123B5D' }}>Executive Leader Confirmation</h3>
            <p style={{ fontSize: '12.5px', color: '#5e7386', margin: '2px 0 0' }}>
              Final authorization initiates bulk batch credit to members' mapped bank accounts via public PFMS / Bank API.
            </p>
          </div>

          <div>
            {leaderConfirmed ? (
              <span className="badge badge-success" style={{ padding: '8px 16px', fontSize: '13px' }}>
                <CheckCircle2 size={16} /> Disbursement Authorized & Recorded in Bank Ledger
              </span>
            ) : (
              <button
                className="btn btn-primary"
                onClick={handleLeaderConfirm}
                disabled={!quorumReached}
                title={!quorumReached ? 'Requires 5 affirmative member votes' : 'Authorize payment'}
              >
                <ShieldCheck size={16} /> Confirm Quorum & Release Payout
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FinancePage;

