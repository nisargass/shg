import React, { useState } from 'react';
import {
  Clock,
  CheckCircle2,
  AlertTriangle,
  Users,
  Calendar,
  Layers,
  ArrowRight,
  TrendingUp,
  FileCheck2,
  RefreshCw
} from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid
} from 'recharts';
import { DEMO_BULK_ORDERS, DEMO_MEMBERS } from '../../mock/mockData';

const ProductionPage = () => {
  const [selectedOrder, setSelectedOrder] = useState(DEMO_BULK_ORDERS[0]);

  // Production burn-up curve: Actual vs Planned vs Predicted
  const burnUpData = [
    { day: 'Day 1', planned: 50, actual: 48, predicted: 48 },
    { day: 'Day 4', planned: 200, actual: 210, predicted: 210 },
    { day: 'Day 8', planned: 450, actual: 430, predicted: 430 },
    { day: 'Day 12', planned: 700, actual: 690, predicted: 690 },
    { day: 'Day 16 (Today)', planned: 850, actual: 840, predicted: 840 },
    { day: 'Day 20 (Est)', planned: 1050, actual: null, predicted: 1060 },
    { day: 'Day 24 (Deadline)', planned: 1200, actual: null, predicted: 1200 }
  ];

  const totalAssigned = selectedOrder.totalQuantity;
  const completed = selectedOrder.completedQuantity;
  const approved = selectedOrder.approvedQuantity;
  const rework = selectedOrder.reworkQuantity;
  const remaining = selectedOrder.pendingQuantity;

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Production Monitoring Dashboard</h1>
          <p className="page-subtitle">
            Real-time shop-floor tracking &bull; Actual verified progress distinct from model projections
          </p>
        </div>
        <div className="page-actions">
          <select
            className="form-control"
            style={{ width: '260px', fontWeight: '600' }}
            value={selectedOrder.id}
            onChange={(e) => {
              const ord = DEMO_BULK_ORDERS.find((o) => o.id === e.target.value);
              if (ord) setSelectedOrder(ord);
            }}
          >
            {DEMO_BULK_ORDERS.map((o) => (
              <option key={o.id} value={o.id}>
                {o.id} - {o.productName.substring(0, 22)}...
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Production Health Alert */}
      <div className="alert-banner info" style={{ marginBottom: '20px' }}>
        <Clock size={20} />
        <div>
          <strong>AI Production Forecast: Order is on Schedule for Nov 18</strong>
          <p style={{ margin: '2px 0 0', fontSize: '13px' }}>
            Current group burn rate is <strong>52.5 units/day</strong>. Projected completion is 2 days ahead of the buyer's Nov 20 deadline.
          </p>
        </div>
      </div>

      {/* Key Metric Counters */}
      <div className="grid grid-cols-4" style={{ marginBottom: '24px' }}>
        <div className="stat-card">
          <div className="stat-icon primary">
            <Layers size={22} />
          </div>
          <div className="stat-info">
            <div className="stat-label">Total Assigned</div>
            <div className="stat-value">{totalAssigned} units</div>
            <div className="stat-sub">Target Contract</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon secondary">
            <Clock size={22} />
          </div>
          <div className="stat-info">
            <div className="stat-label">Actual Completed</div>
            <div className="stat-value">{completed} units</div>
            <div className="stat-sub">{Math.round((completed / totalAssigned) * 100)}% of target</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon success">
            <CheckCircle2 size={22} />
          </div>
          <div className="stat-info">
            <div className="stat-label">Quality Approved</div>
            <div className="stat-value">{approved} units</div>
            <div className="stat-sub">Passed CV & Human Check</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon alert">
            <AlertTriangle size={22} />
          </div>
          <div className="stat-info">
            <div className="stat-label">Rework Units</div>
            <div className="stat-value">{rework} units</div>
            <div className="stat-sub">Under minor restitching</div>
          </div>
        </div>
      </div>

      {/* Burn-Up Timeline Chart */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <div>
            <h3 className="card-title">Cumulative Production Burn-Up (Planned vs Actual vs Predicted)</h3>
            <p className="card-subtitle">
              Verified historical submissions up to Day 16 plotted alongside AI forecast curve
            </p>
          </div>
          <span className="demo-badge">Live Tracking</span>
        </div>
        <div style={{ width: '100%', height: 280 }}>
          <ResponsiveContainer>
            <LineChart data={burnUpData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#EEF2F5" />
              <XAxis dataKey="day" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Line type="monotone" dataKey="planned" stroke="#899ba8" strokeDasharray="5 5" name="Buyer Planned Baseline" />
              <Line type="monotone" dataKey="actual" stroke="#168B80" strokeWidth={3} name="Verified Actual Completed" />
              <Line type="monotone" dataKey="predicted" stroke="#E6A23C" strokeWidth={2} name="AI Predicted Trajectory" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Member-Wise Production Tracking Table */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">Member-Wise Production Roster</h3>
            <p className="card-subtitle">
              Individual artisan milestone records, verified units, rework flags, and estimated completion dates
            </p>
          </div>
        </div>
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Member Artisan</th>
                <th>Assigned Process</th>
                <th>Target Assigned</th>
                <th>Actual Progress</th>
                <th>Approved Qty</th>
                <th>Rework Units</th>
                <th>Predicted Finish Date</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {DEMO_MEMBERS.slice(0, 6).map((mem, idx) => {
                const assigned = 160 + idx * 20;
                const completedUnits = Math.min(assigned, Math.round(assigned * 0.75 + idx * 4));
                const progressPercent = Math.round((completedUnits / assigned) * 100);
                return (
                  <tr key={mem.id}>
                    <td>
                      <strong>{mem.name}</strong>
                      <div style={{ fontSize: '11.5px', color: '#5e7386' }}>{mem.village} &bull; {mem.phone}</div>
                    </td>
                    <td>{mem.skills[0]}</td>
                    <td><strong>{assigned} units</strong></td>
                    <td style={{ minWidth: '150px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11.5px', marginBottom: '3px' }}>
                        <span>{completedUnits} units</span>
                        <strong>{progressPercent}%</strong>
                      </div>
                      <div className="progress-bar">
                        <div className="progress-fill" style={{ width: `${progressPercent}%` }}></div>
                      </div>
                    </td>
                    <td>
                      <span className="badge badge-success">{completedUnits - (idx === 3 ? 4 : 0)} units</span>
                    </td>
                    <td>
                      {idx === 3 ? (
                        <span className="badge badge-alert">4 units</span>
                      ) : (
                        <span style={{ color: '#899ba8', fontSize: '12px' }}>0</span>
                      )}
                    </td>
                    <td>
                      <div style={{ fontSize: '13px', fontWeight: '600', color: '#123B5D' }}>
                        Nov 14, 2026
                      </div>
                      <span style={{ fontSize: '11px', color: '#168B80' }}>6 days before deadline</span>
                    </td>
                    <td>
                      <span className="badge badge-secondary">ON TRACK</span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default ProductionPage;

