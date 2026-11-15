import React from 'react';
import { Link } from 'react-router-dom';
import {
  ShoppingBag,
  Users,
  Clock,
  CheckCircle2,
  AlertTriangle,
  TrendingUp,
  Wallet,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Package,
  Truck
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import {
  DEMO_BULK_ORDERS,
  DEMO_MEMBERS,
  DEMO_AGENT_ACTIVITIES,
  DEMO_ANOMALY_ALERTS
} from '../../mock/mockData';

const LeaderDashboard = () => {
  // Chart data: Production Progress per Order
  const productionData = [
    { name: 'ORD-104 (Tote Bags)', completed: 840, target: 1200, remaining: 360 },
    { name: 'ORD-108 (Kasuti Runners)', completed: 120, target: 500, remaining: 380 },
    { name: 'ORD-112 (Turmeric Jars)', completed: 0, target: 800, remaining: 800 }
  ];

  // Pie chart data: Order Status Distribution
  const orderStatusData = [
    { name: 'In Production', value: 2, color: '#168B80' },
    { name: 'Awaiting Allocation', value: 1, color: '#E6A23C' },
    { name: 'Quality Review', value: 1, color: '#123B5D' }
  ];

  return (
    <div>
      {/* Page Title & Quick Actions */}
      <div className="page-header">
        <div>
          <h1 className="page-title">Pragati Mahila Sangha - Leader Portal</h1>
          <p className="page-subtitle">
            Operations Center &bull; Channapatna Cluster &bull; Ramanagara District
          </p>
        </div>
        <div className="page-actions">
          <Link to="/leader/allocation" className="btn btn-secondary">
            <Sparkles size={16} /> AI Work Allocation
          </Link>
          <Link to="/leader/orders" className="btn btn-primary">
            <ShoppingBag size={16} /> Manage Bulk Orders
          </Link>
        </div>
      </div>

      {/* Prominent Operational Alert Banners */}
      <div className="alert-banner warning">
        <AlertTriangle size={20} style={{ flexShrink: 0 }} />
        <div style={{ flex: 1 }}>
          <strong>Action Required: AI Work Allocation Pending Approval</strong>
          <p style={{ margin: '2px 0 0', fontSize: '13px' }}>
            New Bulk Order <strong>ORD-2026-112 (800 Turmeric Jars)</strong> has an AI-recommended member allocation proposal waiting for your review.
          </p>
        </div>
        <Link to="/leader/allocation" className="btn btn-sm btn-accent" style={{ color: '#FFFFFF' }}>
          Review Allocation
        </Link>
      </div>

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-4" style={{ marginBottom: '24px' }}>
        <div className="stat-card">
          <div className="stat-icon primary">
            <ShoppingBag size={24} />
          </div>
          <div className="stat-info">
            <div className="stat-label">Active Bulk Orders</div>
            <div className="stat-value">3 Orders</div>
            <div className="stat-sub">
              <span>₹5,44,000 Total Value</span>
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon secondary">
            <Users size={24} />
          </div>
          <div className="stat-info">
            <div className="stat-label">Active Working Members</div>
            <div className="stat-value">8 Artisans</div>
            <div className="stat-sub">
              <span>85% Current Utilization</span>
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon accent">
            <CheckCircle2 size={24} />
          </div>
          <div className="stat-info">
            <div className="stat-label">Batch Production Completed</div>
            <div className="stat-value">960 Units</div>
            <div className="stat-sub">
              <span>96.2% Quality Pass Rate</span>
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon success">
            <Wallet size={24} />
          </div>
          <div className="stat-info">
            <div className="stat-label">Member Labor Earnings</div>
            <div className="stat-value">₹84,200</div>
            <div className="stat-sub">
              <span>100% Group Quorum Audited</span>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Section: Production vs Target & Status */}
      <div className="grid grid-cols-12" style={{ marginBottom: '24px' }}>
        <div className="card" style={{ gridColumn: 'span 8' }}>
          <div className="card-header">
            <div>
              <h3 className="card-title">Production Progress vs Target Quantity</h3>
              <p className="card-subtitle">Actual verified completed units compared to buyer target</p>
            </div>
            <span className="demo-badge">Verified Records</span>
          </div>
          <div style={{ width: '100%', height: 280 }}>
            <ResponsiveContainer>
              <BarChart data={productionData} margin={{ top: 10, right: 20, left: 0, bottom: 5 }}>
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Bar dataKey="completed" fill="#168B80" name="Completed & Verified Units" radius={[4, 4, 0, 0]} />
                <Bar dataKey="remaining" fill="#DCE3E8" name="Units Remaining in Production" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card" style={{ gridColumn: 'span 4' }}>
          <div className="card-header">
            <div>
              <h3 className="card-title">Order Lifecycle Status</h3>
              <p className="card-subtitle">Current stage of active bulk orders</p>
            </div>
          </div>
          <div style={{ width: '100%', height: 200, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie data={orderStatusData} cx="50%" cy="50%" innerRadius={55} outerRadius={80} dataKey="value" paddingAngle={4}>
                  {orderStatusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '10px', fontSize: '12px' }}>
            {orderStatusData.map((item, idx) => (
              <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: item.color }}></span>
                  {item.name}
                </span>
                <span style={{ fontWeight: '700' }}>{item.value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Active Bulk Orders Table */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <div>
            <h3 className="card-title">Active Bulk Orders (Under Management)</h3>
            <p className="card-subtitle">Real-time status, specifications and assigned capacity</p>
          </div>
          <Link to="/leader/orders" className="btn btn-sm btn-outline">
            View All Orders <ArrowRight size={14} />
          </Link>
        </div>
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Order ID & Buyer</th>
                <th>Product Description</th>
                <th>Target Quantity</th>
                <th>Progress (Actual vs Target)</th>
                <th>Deadline</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {DEMO_BULK_ORDERS.map((ord) => {
                const percent = Math.round((ord.completedQuantity / ord.totalQuantity) * 100);
                return (
                  <tr key={ord.id}>
                    <td>
                      <strong>{ord.id}</strong>
                      <div style={{ fontSize: '12px', color: '#5e7386' }}>{ord.buyerName}</div>
                    </td>
                    <td>
                      <div>{ord.productName}</div>
                      <span className="badge badge-neutral" style={{ fontSize: '11px', marginTop: '2px' }}>{ord.category}</span>
                    </td>
                    <td>
                      <strong>{ord.totalQuantity} units</strong>
                      <div style={{ fontSize: '11.5px', color: '#168B80' }}>₹{ord.unitAgreedPrice}/unit</div>
                    </td>
                    <td style={{ minWidth: '150px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11.5px', marginBottom: '4px' }}>
                        <span>{ord.completedQuantity} / {ord.totalQuantity}</span>
                        <strong>{percent}%</strong>
                      </div>
                      <div className="progress-bar">
                        <div className="progress-fill" style={{ width: `${percent}%` }}></div>
                      </div>
                    </td>
                    <td>
                      <div>{ord.deadline}</div>
                      <span style={{ fontSize: '11.5px', color: ord.daysRemaining < 15 ? '#C83D43' : '#5e7386' }}>
                        {ord.daysRemaining} days left
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${ord.status === 'IN_PRODUCTION' ? 'badge-secondary' : 'badge-accent'}`}>
                        {ord.status.replace('_', ' ')}
                      </span>
                    </td>
                    <td>
                      <Link to={`/leader/allocation?orderId=${ord.id}`} className="btn btn-sm btn-outline">
                        Allocation &bull; Details
                      </Link>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* AI Agents & Autonomous Activity Feed */}
      <div className="grid grid-cols-2" style={{ marginBottom: '24px' }}>
        <div className="card">
          <div className="card-header">
            <div>
              <h3 className="card-title">
                <Sparkles size={18} color="#168B80" /> Agentic AI Live Activity Log
              </h3>
              <p className="card-subtitle">Real-time actions from 10 autonomous agents</p>
            </div>
            <Link to="/leader/ai" className="btn btn-sm btn-outline">
              AI Console
            </Link>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {DEMO_AGENT_ACTIVITIES.slice(0, 4).map((act) => (
              <div key={act.id} style={{ display: 'flex', gap: '12px', paddingBottom: '12px', borderBottom: '1px solid #EEF2F5' }}>
                <div style={{ width: '36px', height: '36px', borderRadius: '8px', background: '#e6f6f4', color: '#168B80', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                  <Sparkles size={18} />
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <strong style={{ fontSize: '13px', color: '#123B5D' }}>{act.agentName}</strong>
                    <span style={{ fontSize: '11px', color: '#899ba8' }}>{act.timestamp}</span>
                  </div>
                  <p style={{ fontSize: '12.5px', color: '#5e7386', margin: '4px 0' }}>{act.recommendation}</p>
                  {act.requiresHumanAction && (
                    <span className="badge badge-accent" style={{ fontSize: '11px' }}>
                      Awaiting Leader Confirmation
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Financial Transparency & Anomaly Review */}
        <div className="card">
          <div className="card-header">
            <div>
              <h3 className="card-title">
                <ShieldCheck size={18} color="#C83D43" /> Financial Anomaly Alerts & Audits
              </h3>
              <p className="card-subtitle">Automated ledger cross-check for duplicate billing</p>
            </div>
            <Link to="/leader/anomalies" className="btn btn-sm btn-outline">
              Review Ledgers
            </Link>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {DEMO_ANOMALY_ALERTS.map((anom) => (
              <div key={anom.id} style={{ padding: '14px', borderRadius: '8px', background: anom.severity === 'HIGH' ? '#fbebed' : '#fdfaf4', border: `1px solid ${anom.severity === 'HIGH' ? '#f5c6cb' : '#faebcc'}` }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <strong style={{ fontSize: '13px', color: anom.severity === 'HIGH' ? '#C83D43' : '#ab711b' }}>
                    {anom.title}
                  </strong>
                  <span className={`badge ${anom.severity === 'HIGH' ? 'badge-alert' : 'badge-accent'}`}>
                    {anom.severity} RISK
                  </span>
                </div>
                <p style={{ fontSize: '12px', color: '#5e7386', margin: 0 }}>
                  {anom.description}
                </p>
                <div style={{ marginTop: '8px', fontSize: '11.5px', color: '#123B5D', fontStyle: 'italic' }}>
                  {anom.explanation}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LeaderDashboard;
