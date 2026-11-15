import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import {
  ShoppingBag,
  Clock,
  CheckCircle2,
  DollarSign,
  Mic,
  Calendar,
  AlertCircle,
  HelpCircle,
  ArrowRight,
  ShieldCheck,
  TrendingUp,
  Sparkles
} from 'lucide-react';

const MemberDashboard = () => {
  const { user } = useAuth();
  const memberName = user?.name || 'Sunita Rathod';

  // Personal task metrics for Sunita Rathod (ORD-2026-104)
  const myTask = {
    orderId: 'ORD-2026-104',
    productName: 'Organic Cotton Tote Bags',
    roleTask: 'Main Body Stitching & Handle Assembly',
    allocatedQty: 220,
    completedQty: 180,
    approvedQty: 180,
    remainingQty: 40,
    deadline: '2026-11-20',
    daysRemaining: 13,
    pieceRate: 32.0,
    estimatedEarnings: 7040.0,
    approvedEarnings: 5760.0,
    // Metric 1: Actual Verified Production Progress
    actualProgressPercent: 82, // 180 / 220
    // Metric 2: AI Predicted Completion Likelihood
    completionLikelihoodPercent: 94,
    estimatedFinishDate: 'Nov 09, 2026 (11 days ahead of buyer cutoff)',
    predictionExplanation: 'At your steady daily speed of 3.2 bags/hour over 5 daily hours, you are projected to complete all 40 remaining units in 2.5 work days.'
  };

  return (
    <div>
      {/* Friendly, Accessible Header */}
      <div className="card" style={{ background: 'linear-gradient(135deg, #123B5D 0%, #174b75 100%)', color: '#FFFFFF', marginBottom: '24px', padding: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <span className="badge" style={{ background: '#168B80', color: '#FFFFFF', marginBottom: '6px' }}>
              Artisan Mobile Portal
            </span>
            <h1 style={{ fontSize: '24px', color: '#FFFFFF', fontWeight: '800' }}>
              Namaste, {memberName}!
            </h1>
            <p style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.85)', marginTop: '4px' }}>
              Pragati Mahila Sangha &bull; Channapatna Village &bull; Skill: Heavy Fabric Stitching
            </p>
          </div>

          <div>
            <Link to="/member/assistant" className="btn btn-accent btn-lg" style={{ color: '#000000', fontWeight: '700' }}>
              <Mic size={20} /> Open Voice Saathi (Kannada / Hindi / English)
            </Link>
          </div>
        </div>
      </div>

      {/* Privacy Notice Banner */}
      <div className="alert-banner info" style={{ marginBottom: '20px' }}>
        <ShieldCheck size={18} />
        <span style={{ fontSize: '13px' }}>
          <strong>Private Artisan Workspace:</strong> Only your personal assigned quantities, earnings, and progress are displayed on this screen.
        </span>
      </div>

      {/* Two Different Metrics Showcase: Actual Progress vs Predicted Likelihood */}
      <div className="grid grid-cols-2" style={{ gap: '20px', marginBottom: '24px' }}>
        {/* Metric 1: Actual Production Progress */}
        <div className="card" style={{ borderLeft: '4px solid #168B80' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
            <span style={{ fontSize: '12px', fontWeight: '700', textTransform: 'uppercase', color: '#5e7386' }}>
              Metric 1: Actual Production Progress
            </span>
            <span className="badge badge-secondary">Verified Units</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px', marginBottom: '8px' }}>
            <span style={{ fontSize: '32px', fontWeight: '800', color: '#168B80' }}>
              {myTask.actualProgressPercent}%
            </span>
            <span style={{ fontSize: '14px', color: '#5e7386' }}>
              ({myTask.completedQty} of {myTask.allocatedQty} units finished)
            </span>
          </div>
          <div className="progress-bar" style={{ height: '10px', marginBottom: '10px' }}>
            <div className="progress-fill" style={{ width: `${myTask.actualProgressPercent}%` }}></div>
          </div>
          <p style={{ fontSize: '12.5px', color: '#5e7386', margin: 0 }}>
            Remaining to stitch: <strong>{myTask.remainingQty} units</strong> before {myTask.deadline}.
          </p>
        </div>

        {/* Metric 2: Predicted Completion Likelihood */}
        <div className="card" style={{ borderLeft: '4px solid #E6A23C' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
            <span style={{ fontSize: '12px', fontWeight: '700', textTransform: 'uppercase', color: '#5e7386' }}>
              Metric 2: AI Completion Likelihood
            </span>
            <span className="badge badge-accent">Model Projection</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px', marginBottom: '8px' }}>
            <span style={{ fontSize: '32px', fontWeight: '800', color: '#ab711b' }}>
              {myTask.completionLikelihoodPercent}%
            </span>
            <span style={{ fontSize: '13px', color: '#168B80', fontWeight: '700' }}>
              HIGH ON-TIME CONFIDENCE
            </span>
          </div>
          <p style={{ fontSize: '12.5px', color: '#243746', margin: 0, lineHeight: '1.45' }}>
            {myTask.predictionExplanation}
          </p>
        </div>
      </div>

      {/* Current Task Detail Card */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <div>
            <h3 className="card-title">My Current Active Work Assignment</h3>
            <p className="card-subtitle">Order #{myTask.orderId} &bull; Deadline: {myTask.deadline} ({myTask.daysRemaining} days left)</p>
          </div>
          <Link to="/member/production" className="btn btn-primary btn-sm">
            Submit Completed Units
          </Link>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '16px', background: '#F8FAFC', padding: '16px', borderRadius: '8px', border: '1px solid #EEF2F5', marginBottom: '16px' }}>
          <div>
            <span style={{ fontSize: '11px', color: '#5e7386', textTransform: 'uppercase' }}>Product</span>
            <div style={{ fontSize: '14px', fontWeight: '700', color: '#123B5D' }}>{myTask.productName}</div>
          </div>
          <div>
            <span style={{ fontSize: '11px', color: '#5e7386', textTransform: 'uppercase' }}>My Role</span>
            <div style={{ fontSize: '14px', fontWeight: '700', color: '#123B5D' }}>{myTask.roleTask}</div>
          </div>
          <div>
            <span style={{ fontSize: '11px', color: '#5e7386', textTransform: 'uppercase' }}>Agreed Piece Rate</span>
            <div style={{ fontSize: '14px', fontWeight: '700', color: '#168B80' }}>₹{myTask.pieceRate} / bag</div>
          </div>
          <div>
            <span style={{ fontSize: '11px', color: '#5e7386', textTransform: 'uppercase' }}>Approved Earnings</span>
            <div style={{ fontSize: '16px', fontWeight: '800', color: '#168B80' }}>₹{myTask.approvedEarnings.toLocaleString()}</div>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          <Link to="/member/production" className="btn btn-secondary">
            <CheckCircle2 size={16} /> Submit Today's Completed Bags
          </Link>
          <Link to="/member/earnings" className="btn btn-outline">
            <DollarSign size={16} /> View Earnings Ledger
          </Link>
          <Link to="/member/payments" className="btn btn-outline">
            <ShieldCheck size={16} /> Cast Vote on Group Payout
          </Link>
        </div>
      </div>
    </div>
  );
};

export default MemberDashboard;

