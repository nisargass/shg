import React from 'react';
import { Link } from 'react-router-dom';
import {
  Building2,
  Users,
  Award,
  TrendingUp,
  ShoppingBag,
  DollarSign,
  CheckCircle2,
  ShieldCheck,
  Download
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid
} from 'recharts';

const FederationDashboard = () => {
  // Comparative SHG Performance Data across Ramanagara Cluster
  const shgComparisonData = [
    { name: 'Pragati Sangha', fulfilledOrders: 14, revenueLakhs: 8.57, onTimeRate: 96.8, lakhpatiDidis: 6 },
    { name: 'Sannidhi Farmers', fulfilledOrders: 10, revenueLakhs: 6.20, onTimeRate: 94.2, lakhpatiDidis: 4 },
    { name: 'Kala Chaitanya', fulfilledOrders: 12, revenueLakhs: 7.10, onTimeRate: 95.0, lakhpatiDidis: 5 },
    { name: 'Cauvery Mahila', fulfilledOrders: 8, revenueLakhs: 4.80, onTimeRate: 91.5, lakhpatiDidis: 3 }
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h1 className="page-title">Sanjeevini KSRLPS - Federation Oversight Portal</h1>
            <span className="demo-badge">NRLM Cluster Dashboard</span>
          </div>
          <p className="page-subtitle">
            Ramanagara District &bull; Cluster Development Officer: Deepa Narayan, KAS
          </p>
        </div>
        <div className="page-actions">
          <button className="btn btn-outline" onClick={() => alert('Generating NRLM State Performance PDF...')}>
            <Download size={16} /> Export State MIS Report
          </button>
        </div>
      </div>

      {/* Cluster KPI Counters */}
      <div className="grid grid-cols-4" style={{ marginBottom: '24px' }}>
        <div className="stat-card">
          <div className="stat-icon primary"><Building2 size={24} /></div>
          <div className="stat-info">
            <div className="stat-label">Affiliated SHGs in Cluster</div>
            <div className="stat-value">24 SHGs</div>
            <div className="stat-sub">280 Registered Artisans</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon secondary"><ShoppingBag size={24} /></div>
          <div className="stat-info">
            <div className="stat-label">Active Bulk Contracts</div>
            <div className="stat-value">9 Orders</div>
            <div className="stat-sub">₹16,40,000 Pipeline Value</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon success"><Award size={24} /></div>
          <div className="stat-info">
            <div className="stat-label">Cluster On-Time Fulfilment</div>
            <div className="stat-value">95.4%</div>
            <div className="stat-sub">+18% vs State Rural Average</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon accent"><TrendingUp size={24} /></div>
          <div className="stat-info">
            <div className="stat-label">Lakhpati Didi Milestone</div>
            <div className="stat-value">42 Members</div>
            <div className="stat-sub">Earning &gt; ₹1,00,000 / year</div>
          </div>
        </div>
      </div>

      {/* Cluster Performance Comparison Chart */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <div>
            <h3 className="card-title">Comparative SHG Cluster Performance (Turnover & Lakhpati Members)</h3>
            <p className="card-subtitle">
              Evaluating economic self-reliance and contract delivery capacity across village sanghas
            </p>
          </div>
          <span className="badge badge-secondary">Quarterly Audit Active</span>
        </div>
        <div style={{ width: '100%', height: 280 }}>
          <ResponsiveContainer>
            <BarChart data={shgComparisonData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#EEF2F5" />
              <XAxis dataKey="name" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="revenueLakhs" fill="#123B5D" name="Gross Bulk Revenue (₹ Lakhs)" radius={[4, 4, 0, 0]} />
              <Bar dataKey="lakhpatiDidis" fill="#168B80" name="Verified Lakhpati Didis (Count)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* SHG Cluster Roster Table */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">Cluster Self-Help Group Registry</h3>
            <p className="card-subtitle">Aggregated capacity, active contracts, and on-time fulfillment scores</p>
          </div>
        </div>
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>SHG Name & Village</th>
                <th>Core Craft Domain</th>
                <th>Working Members</th>
                <th>Active Orders</th>
                <th>On-Time Rate</th>
                <th>Quarterly Revenue</th>
                <th>Lakhpati Status</th>
              </tr>
            </thead>
            <tbody>
              {shgComparisonData.map((shg, idx) => (
                <tr key={idx}>
                  <td>
                    <strong>{shg.name}</strong>
                    <div style={{ fontSize: '11px', color: '#5e7386' }}>Channapatna Taluk, Ramanagara</div>
                  </td>
                  <td>
                    <span className="badge badge-neutral">
                      {idx === 0 ? 'Textiles & Tote Bags' : idx === 1 ? 'Food & Organic Turmeric' : 'Channapatna Toys'}
                    </span>
                  </td>
                  <td><strong>{idx === 0 ? 8 : 12} artisans</strong></td>
                  <td>{shg.fulfilledOrders} batches</td>
                  <td>
                    <strong style={{ color: '#168B80' }}>{shg.onTimeRate}%</strong>
                  </td>
                  <td><strong>₹{shg.revenueLakhs} Lakhs</strong></td>
                  <td>
                    <span className="badge badge-success">
                      <CheckCircle2 size={12} /> {shg.lakhpatiDidis} Members Verified
                    </span>
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

export default FederationDashboard;

