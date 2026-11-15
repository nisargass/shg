import React, { useState } from 'react';
import {
  DollarSign,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  PieChart as PieChartIcon,
  ShieldAlert,
  Info,
  Sliders,
  Sparkles
} from 'lucide-react';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis
} from 'recharts';
import { DEMO_COSTING_MODELS, DEMO_BULK_ORDERS } from '../../mock/mockData';

const PricingPage = () => {
  const [selectedOrderId, setSelectedOrderId] = useState('ORD-2026-104');
  const costing = DEMO_COSTING_MODELS[selectedOrderId] || DEMO_COSTING_MODELS['ORD-2026-104'];

  const colors = ['#123B5D', '#168B80', '#E6A23C', '#27c5b4', '#899ba8', '#ab711b', '#3b82f6', '#64748b'];

  const pieData = costing.costComponents.map((c, idx) => ({
    name: c.name.split('(')[0],
    value: c.total,
    color: colors[idx % colors.length]
  }));

  return (
    <div>
      <div className="page-header">
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h1 className="page-title">Smart Pricing & Cost Calculator</h1>
            <span className="demo-badge">Anti-Underpricing Engine</span>
          </div>
          <p className="page-subtitle">
            Scientific unit costing ensuring material, fair labor, packaging, freight, and group margin are never compromised
          </p>
        </div>
        <div className="page-actions">
          <select
            className="form-control"
            style={{ width: '260px', fontWeight: '600' }}
            value={selectedOrderId}
            onChange={(e) => setSelectedOrderId(e.target.value)}
          >
            {DEMO_BULK_ORDERS.map((o) => (
              <option key={o.id} value={o.id}>{o.id} - {o.productName.substring(0, 22)}...</option>
            ))}
          </select>
        </div>
      </div>

      {/* Underpricing Health Banner */}
      {!costing.aiPricingInsights.underpricingAlert ? (
        <div className="alert-banner success" style={{ marginBottom: '24px' }}>
          <CheckCircle2 size={20} />
          <div>
            <strong>Viable Pricing Verified: Fair Margin Protected</strong>
            <p style={{ margin: '2px 0 0', fontSize: '13px' }}>
              {costing.aiPricingInsights.advice}
            </p>
          </div>
        </div>
      ) : (
        <div className="alert-banner danger" style={{ marginBottom: '24px' }}>
          <AlertTriangle size={20} />
          <div>
            <strong>CRITICAL UNDERPRICING WARNING: Bid is Below Break-Even Cost</strong>
            <p style={{ margin: '2px 0 0', fontSize: '13px' }}>
              Quoting below ₹{costing.suggestedMinSellingPrice} will cause the group to absorb transport and scrap losses.
            </p>
          </div>
        </div>
      )}

      {/* Summary KPI Cards */}
      <div className="grid grid-cols-4" style={{ marginBottom: '24px' }}>
        <div className="stat-card">
          <div className="stat-icon primary">
            <DollarSign size={22} />
          </div>
          <div className="stat-info">
            <div className="stat-label">Total Unit Production Cost</div>
            <div className="stat-value">₹{costing.totalProductionCost}</div>
            <div className="stat-sub">Break-even baseline</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon secondary">
            <TrendingUp size={22} />
          </div>
          <div className="stat-info">
            <div className="stat-label">Agreed Selling Price</div>
            <div className="stat-value">₹{costing.buyerAgreedPrice}</div>
            <div className="stat-sub">Contract revenue: ₹{costing.buyerTotalRevenue.toLocaleString()}</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon success">
            <DollarSign size={22} />
          </div>
          <div className="stat-info">
            <div className="stat-label">Group Net Reserve Surplus</div>
            <div className="stat-value">₹{costing.groupNetProfitTotal.toLocaleString()}</div>
            <div className="stat-sub">{costing.marginPercentage}% Net Margin (₹{costing.groupNetMargin}/unit)</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon accent">
            <Sparkles size={22} />
          </div>
          <div className="stat-info">
            <div className="stat-label">Market Benchmark</div>
            <div className="stat-value">₹160 - ₹175</div>
            <div className="stat-sub">Bangalore wholesale rates</div>
          </div>
        </div>
      </div>

      {/* Main Breakdown Layout */}
      <div className="grid grid-cols-12" style={{ gap: '24px' }}>
        {/* Left Column: Cost Itemization Table */}
        <div style={{ gridColumn: 'span 7' }}>
          <div className="card">
            <div className="card-header">
              <div>
                <h3 className="card-title">Detailed Cost Component Breakdown (Per Unit & Batch)</h3>
                <p className="card-subtitle">Calculated for {costing.orderQty} units contract</p>
              </div>
              <span className="demo-badge">FastAPI Logic</span>
            </div>
            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>Cost Element</th>
                    <th>Cost / Unit</th>
                    <th>Total Contract Amount</th>
                    <th>% of Cost</th>
                  </tr>
                </thead>
                <tbody>
                  {costing.costComponents.map((c, idx) => {
                    const percent = ((c.total / costing.totalProductionCostTotal) * 100).toFixed(1);
                    return (
                      <tr key={idx}>
                        <td>
                          <strong>{c.name}</strong>
                        </td>
                        <td>₹{c.unitCost.toFixed(2)}</td>
                        <td><strong>₹{c.total.toLocaleString()}</strong></td>
                        <td>
                          <span className="badge badge-neutral">{percent}%</span>
                        </td>
                      </tr>
                    );
                  })}
                  <tr style={{ background: '#f8fafc', fontWeight: '700' }}>
                    <td>TOTAL PRODUCTION COST</td>
                    <td>₹{costing.totalProductionCost}</td>
                    <td>₹{costing.totalProductionCostTotal.toLocaleString()}</td>
                    <td>100.0%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Right Column: Chart & Pricing Simulator */}
        <div style={{ gridColumn: 'span 5' }}>
          <div className="card" style={{ marginBottom: '20px' }}>
            <div className="card-header">
              <h3 className="card-title">Expense Allocation Share</h3>
            </div>
            <div style={{ width: '100%', height: 240 }}>
              <ResponsiveContainer>
                <PieChart>
                  <Pie data={pieData} cx="50%" cy="50%" outerRadius={80} dataKey="value" label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}>
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => `₹${value.toLocaleString()}`} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="card" style={{ background: '#F8FAFC', border: '1px solid #DCE3E8' }}>
            <h3 style={{ fontSize: '14px', color: '#123B5D', marginBottom: '8px' }}>
              Pricing Optimization Intelligence
            </h3>
            <p style={{ fontSize: '12.5px', color: '#5e7386', lineHeight: '1.5', margin: 0 }}>
              {costing.aiPricingInsights.marketBenchmark}
            </p>
            <div style={{ marginTop: '12px', padding: '10px', background: '#FFFFFF', borderRadius: '6px', border: '1px solid #EEF2F5', fontSize: '12px' }}>
              <div>Recommended Optimal Re-order Bid: <strong>₹{costing.recommendedOptimalPrice} / unit</strong></div>
              <div style={{ color: '#168B80', marginTop: '2px' }}>Protects a 12.5% SHG group infrastructure renewal fund.</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PricingPage;

