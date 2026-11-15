import React, { useState } from 'react';
import {
  Vote,
  ShieldCheck,
  CheckCircle2,
  Clock,
  AlertCircle,
  ThumbsUp,
  ThumbsDown,
  Info
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { financialApi } from '../../api/services';

const MemberPaymentsPage = () => {
  const { user } = useAuth();
  const [hasVoted, setHasVoted] = useState(true); // Sunita already voted YES in the mockData
  const [voteDecision, setVoteDecision] = useState('APPROVED');
  const [voteCount, setVoteCount] = useState(4);
  const [actionSuccess, setActionSuccess] = useState('');

  const handleCastVote = async (decision) => {
    await financialApi.submitMemberVote('ORD-2026-104', user?.id || 'mem_01', decision);
    setVoteDecision(decision);
    setHasVoted(true);
    setVoteCount(5); // Reach quorum!
    setActionSuccess(`Your vote (${decision}) has been registered in the SHG quorum book. Quorum now met!`);
    setTimeout(() => setActionSuccess(''), 6000);
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Group Payout Quorum & Voting</h1>
          <p className="page-subtitle">
            Democratic consent portal &bull; Review group milestone calculations and vote before release
          </p>
        </div>
      </div>

      {actionSuccess && (
        <div className="alert-banner success" style={{ marginBottom: '20px' }}>
          <CheckCircle2 size={20} />
          <span>{actionSuccess}</span>
        </div>
      )}

      {/* Quorum Governance Explanation */}
      <div className="alert-banner info" style={{ marginBottom: '24px' }}>
        <ShieldCheck size={20} />
        <div>
          <strong>Democratic Quorum Rule: Group Approval Protects Every Artisan</strong>
          <p style={{ margin: '2px 0 0', fontSize: '13px' }}>
            Under SHG by-laws, no leader can trigger bank disbursement without minimum 60% member confirmation. This ensures piece counts and rate deductions are completely agreed upon by the artisans who did the work.
          </p>
        </div>
      </div>

      {/* Voting Card */}
      <div className="card" style={{ maxWidth: '720px', margin: '0 auto', padding: '28px' }}>
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <span className="badge badge-primary">ACTIVE MILESTONE BALLOT</span>
          <h2 style={{ fontSize: '20px', color: '#123B5D', marginTop: '8px' }}>
            ORD-2026-104: Interim Milestone 1 (600 Bags)
          </h2>
          <div style={{ fontSize: '14px', color: '#5e7386', marginTop: '4px' }}>
            Total Group Labor Allocation: <strong>₹19,200</strong> across working members
          </div>
        </div>

        {/* My Individual Calculation Snapshot */}
        <div style={{ background: '#f8fafc', padding: '16px', borderRadius: '8px', border: '1px solid #EEF2F5', marginBottom: '24px' }}>
          <h4 style={{ fontSize: '13.5px', color: '#123B5D', marginBottom: '8px' }}>Your Personal Entitlement in this Ballot:</h4>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '4px' }}>
            <span>Verified Stitched Bags:</span>
            <strong>180 units</strong>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '4px' }}>
            <span>Agreed Labor Rate:</span>
            <strong>₹32.00 / bag</strong>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '4px' }}>
            <span>Tool / Advance Deduction:</span>
            <strong>₹0.00</strong>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '15px', fontWeight: '800', color: '#168B80', borderTop: '1px solid #DCE3E8', paddingTop: '6px', marginTop: '6px' }}>
            <span>Your Net Bank Credit:</span>
            <span>₹5,760.00</span>
          </div>
        </div>

        {/* Quorum Progress Indicator */}
        <div style={{ marginBottom: '28px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '6px' }}>
            <span>Quorum Threshold Status</span>
            <strong>{voteCount} of 5 required votes received ({voteCount >= 5 ? 'Quorum Met' : '80% achieved'})</strong>
          </div>
          <div className="progress-bar" style={{ height: '10px' }}>
            <div className="progress-fill" style={{ width: `${(voteCount / 5) * 100}%`, backgroundColor: voteCount >= 5 ? '#22C55E' : '#E6A23C' }}></div>
          </div>
        </div>

        {/* Cast Ballot Controls */}
        <div>
          {hasVoted ? (
            <div style={{ textAlign: 'center', padding: '16px', background: '#e8f5e9', borderRadius: '8px', border: '1px solid #c8e6c9' }}>
              <CheckCircle2 size={32} color="#2e7d32" style={{ margin: '0 auto 6px' }} />
              <div style={{ fontSize: '15px', fontWeight: '700', color: '#1b5e20' }}>
                Your Affirmative Vote (APPROVED) is Recorded
              </div>
              <p style={{ fontSize: '12.5px', color: '#2e7d32', margin: '4px 0 0' }}>
                You have confirmed your 180 units @ ₹32.00 calculation. Leader will initiate bank dispatch once all votes are in.
              </p>
            </div>
          ) : (
            <div>
              <div style={{ fontSize: '13.5px', fontWeight: '700', textAlign: 'center', marginBottom: '12px' }}>
                Do you confirm that your completed units and earnings calculation are accurate?
              </div>
              <div style={{ display: 'flex', gap: '14px' }}>
                <button
                  className="btn btn-secondary btn-lg"
                  style={{ flex: 1, padding: '14px' }}
                  onClick={() => handleCastVote('APPROVED')}
                >
                  <ThumbsUp size={18} /> Yes, Approve Payout (₹5,760)
                </button>
                <button
                  className="btn btn-outline btn-lg"
                  style={{ flex: 1, padding: '14px' }}
                  onClick={() => handleCastVote('DISPUTED')}
                >
                  <ThumbsDown size={18} /> Raise Unit Dispute
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MemberPaymentsPage;

