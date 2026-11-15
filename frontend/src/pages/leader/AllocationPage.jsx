import React, { useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import {
  GitPullRequest,
  Sparkles,
  CheckCircle,
  AlertTriangle,
  User,
  Clock,
  Award,
  TrendingUp,
  Brain,
  ShieldCheck,
  RefreshCw,
  Sliders,
  Info
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend
} from 'recharts';
import { DEMO_BULK_ORDERS, DEMO_ALLOCATIONS } from '../../mock/mockData';
import { allocationApi } from '../../api/services';

const AllocationPage = () => {
  const [searchParams] = useSearchParams();
  const initialOrderId = searchParams.get('orderId') || 'ORD-2026-104';

  const [selectedOrderId, setSelectedOrderId] = useState(initialOrderId);
  const [allocations, setAllocations] = useState(DEMO_ALLOCATIONS[initialOrderId] || DEMO_ALLOCATIONS['ORD-2026-104']);
  const [isApproved, setIsApproved] = useState(true);
  const [feedbackText, setFeedbackText] = useState('');
  const [actionSuccessMsg, setActionSuccessMsg] = useState('');
  const [rebalancing, setRebalancing] = useState(false);

  const currentOrder = DEMO_BULK_ORDERS.find((o) => o.id === selectedOrderId) || DEMO_BULK_ORDERS[0];

  // Visual allocation chart data
  const chartData = allocations.map((item) => ({
    name: item.memberName.split(' ')[0],
    allocated: item.allocatedQty,
    feasible: item.feasibleQty,
    completed: item.completedQty
  }));

  const totalAllocated = allocations.reduce((sum, item) => sum + item.allocatedQty, 0);
  const unallocatedQty = currentOrder.totalQuantity - totalAllocated;

  const handleApprove = async () => {
    await allocationApi.approveAllocation(selectedOrderId, { approvedBy: 'Leader', timestamp: new Date() });
    setIsApproved(true);
    setActionSuccessMsg(`Work allocation for ${selectedOrderId} approved and locked. Notifications dispatched to all assigned members.`);
    setTimeout(() => setActionSuccessMsg(''), 5000);
  };

  const handleRebalance = async () => {
    setRebalancing(true);
    await allocationApi.requestRebalance(selectedOrderId, feedbackText);
    setTimeout(() => {
      setRebalancing(false);
      setActionSuccessMsg('AI Optimization Agent revised allocation proposals based on member workload limits.');
      setTimeout(() => setActionSuccessMsg(''), 5000);
    }, 1000);
  };

  return (
    <div>
      {/* Header */}
      <div className="page-header">
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h1 className="page-title">Intelligent AI Work Allocation</h1>
            <span className="demo-badge">Multi-Agent Algorithm</span>
          </div>
          <p className="page-subtitle">
            Fair distribution engine balancing member skill, daily available hours, speed, and predicted on-time likelihood
          </p>
        </div>
        <div className="page-actions">
          {/* Order Selector */}
          <select
            className="form-control"
            style={{ width: '240px', fontWeight: '600' }}
            value={selectedOrderId}
            onChange={(e) => {
              setSelectedOrderId(e.target.value);
              setAllocations(DEMO_ALLOCATIONS[e.target.value] || DEMO_ALLOCATIONS['ORD-2026-104']);
            }}
          >
            {DEMO_BULK_ORDERS.map((o) => (
              <option key={o.id} value={o.id}>
                {o.id} - {o.productName.substring(0, 24)}...
              </option>
            ))}
          </select>
        </div>
      </div>

      {actionSuccessMsg && (
        <div className="alert-banner success" style={{ marginBottom: '20px' }}>
          <CheckCircle size={20} />
          <span>{actionSuccessMsg}</span>
        </div>
      )}

      {/* Order Context Banner */}
      <div className="card" style={{ marginBottom: '24px', background: 'linear-gradient(to right, #ffffff, #f7fafc)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <span className="badge badge-primary">{currentOrder.id}</span>
            <h2 style={{ fontSize: '18px', color: '#123B5D', margin: '6px 0 2px' }}>
              {currentOrder.productName}
            </h2>
            <div style={{ fontSize: '12.5px', color: '#5e7386' }}>
              Buyer: <strong>{currentOrder.buyerName}</strong> &bull; Deadline: <strong>{currentOrder.deadline}</strong> ({currentOrder.daysRemaining} days remaining)
            </div>
          </div>

          <div style={{ display: 'flex', gap: '24px', textAlign: 'center' }}>
            <div>
              <span style={{ fontSize: '11px', color: '#5e7386', textTransform: 'uppercase', fontWeight: '600' }}>Target Quantity</span>
              <div style={{ fontSize: '20px', fontWeight: '800', color: '#123B5D' }}>{currentOrder.totalQuantity}</div>
            </div>
            <div>
              <span style={{ fontSize: '11px', color: '#5e7386', textTransform: 'uppercase', fontWeight: '600' }}>Total Allocated</span>
              <div style={{ fontSize: '20px', fontWeight: '800', color: '#168B80' }}>{totalAllocated}</div>
            </div>
            <div>
              <span style={{ fontSize: '11px', color: '#5e7386', textTransform: 'uppercase', fontWeight: '600' }}>Unallocated Buffer</span>
              <div style={{ fontSize: '20px', fontWeight: '800', color: unallocatedQty > 0 ? '#E6A23C' : '#22C55E' }}>
                {unallocatedQty}
              </div>
            </div>
            <div>
              <span style={{ fontSize: '11px', color: '#5e7386', textTransform: 'uppercase', fontWeight: '600' }}>Leader Decision</span>
              <div>
                <span className={`badge ${isApproved ? 'badge-success' : 'badge-accent'}`}>
                  {isApproved ? 'ALLOCATION APPROVED' : 'PROPOSAL PENDING'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Allocation Visualization: Member vs Feasible Capacity */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <div>
            <h3 className="card-title">Member Allocation vs Feasible Capacity Comparison</h3>
            <p className="card-subtitle">
              Intelligent comparison between proposed assigned units and realistic feasible quantity based on speed rate
            </p>
          </div>
          <span className="badge badge-secondary">Optimization Active</span>
        </div>
        <div style={{ width: '100%', height: 260 }}>
          <ResponsiveContainer>
            <BarChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <XAxis dataKey="name" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="feasible" fill="#DCE3E8" name="Predicted Max Feasible Capacity" radius={[4, 4, 0, 0]} />
              <Bar dataKey="allocated" fill="#168B80" name="Proposed Assigned Quantity" radius={[4, 4, 0, 0]} />
              <Bar dataKey="completed" fill="#E6A23C" name="Actual Progress to Date" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Detailed Member Allocation Cards */}
      <h3 style={{ fontSize: '16px', color: '#123B5D', marginBottom: '14px' }}>
        Member Capacity Analysis & AI Likelihood Predictions
      </h3>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginBottom: '28px' }}>
        {allocations.map((alloc) => {
          const isHighLikelihood = alloc.completionLikelihood >= 90;
          return (
            <div key={alloc.memberId} className="card" style={{ padding: '20px' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1.5fr 1fr', gap: '20px', alignItems: 'flex-start' }}>
                {/* Column 1: Member profile & task */}
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                    <div style={{ width: '36px', height: '36px', borderRadius: '50%', background: '#e6f6f4', color: '#168B80', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: '700' }}>
                      {alloc.memberName.charAt(0)}
                    </div>
                    <div>
                      <h4 style={{ fontSize: '15px', color: '#123B5D' }}>{alloc.memberName}</h4>
                      <span style={{ fontSize: '12px', color: '#5e7386' }}>{alloc.memberId} &bull; {alloc.speedRate}</span>
                    </div>
                  </div>
                  <div style={{ fontSize: '12.5px', color: '#243746', marginBottom: '6px' }}>
                    <strong>Role / Process:</strong> {alloc.roleTask}
                  </div>
                  <div style={{ fontSize: '12px', color: '#5e7386' }}>
                    Available Hours: <strong>{alloc.availableHoursDaily}h / day</strong> &bull; Skill Match: <strong>{alloc.skillMatchScore}%</strong>
                  </div>
                </div>

                {/* Column 2: AI Prediction & Explanation */}
                <div style={{ background: '#F8FAFC', padding: '14px', borderRadius: '8px', border: '1px solid #EEF2F5' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#168B80', fontSize: '12px', fontWeight: '700', marginBottom: '4px' }}>
                    <Brain size={16} />
                    <span>AI PREDICTION EXPLANATION (Confidence: {alloc.predictionConfidence})</span>
                  </div>
                  <p style={{ fontSize: '12.5px', color: '#243746', margin: '4px 0 8px', lineHeight: '1.45' }}>
                    {alloc.explanation}
                  </p>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                    {alloc.factors.map((f, fIdx) => (
                      <span key={fIdx} style={{ fontSize: '11px', background: '#FFFFFF', border: '1px solid #DCE3E8', padding: '2px 6px', borderRadius: '4px', color: '#5e7386' }}>
                        &bull; {f}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Column 3: Likelihood Metrics & Quantities */}
                <div style={{ textAlign: 'right' }}>
                  <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'baseline', gap: '6px' }}>
                    <span style={{ fontSize: '24px', fontWeight: '800', color: isHighLikelihood ? '#168B80' : '#E6A23C' }}>
                      {alloc.completionLikelihood}%
                    </span>
                    <span style={{ fontSize: '11px', color: '#5e7386', fontWeight: '600' }}>ON-TIME PROBABILITY</span>
                  </div>

                  <div style={{ marginTop: '8px', fontSize: '13px' }}>
                    Proposed Quantity: <strong>{alloc.allocatedQty} units</strong>
                  </div>
                  <div style={{ fontSize: '12px', color: '#5e7386', marginTop: '2px' }}>
                    Feasible Capacity: <strong>{alloc.feasibleQty} units</strong>
                  </div>
                  <div style={{ fontSize: '12px', color: '#168B80', marginTop: '2px' }}>
                    Verified Done: <strong>{alloc.completedQty} units</strong>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Leader Decision Panel */}
      <div className="card" style={{ background: '#fdfdfd', border: '2px solid #DCE3E8' }}>
        <div className="card-header">
          <div>
            <h3 className="card-title">
              <ShieldCheck size={18} color="#168B80" /> Leader Decision & Approval Control
            </h3>
            <p className="card-subtitle">
              AI suggestions are NOT official work orders until approved by the SHG Leader
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
          <div style={{ maxWidth: '600px' }}>
            <p style={{ fontSize: '13px', color: '#5e7386', margin: 0 }}>
              Approving publishes individual assignments directly to each member's mobile dashboard and initializes their piece-rate earning ledger.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '12px' }}>
            <button className="btn btn-outline" onClick={handleRebalance} disabled={rebalancing}>
              <RefreshCw size={16} className={rebalancing ? 'animate-spin' : ''} />
              {rebalancing ? 'Rebalancing...' : 'Request AI Rebalance'}
            </button>
            <button className="btn btn-primary" onClick={handleApprove}>
              <CheckCircle size={16} /> Approve & Lock Allocation
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AllocationPage;

