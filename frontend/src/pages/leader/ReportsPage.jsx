import React from 'react';
import {
  BarChart3,
  TrendingUp,
  Award,
  CheckCircle2,
  Calendar,
  Download,
  DollarSign
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
  LineChart,
  Line
} from 'recharts';

const ReportsPage = () => {
  // Monthly fulfilled orders & revenue
  const monthlyRevenueData = [
    { month: 'Jun', revenue: 78000, margin: 8200 },
    { month: 'Jul', revenue: 112000, margin: 12400 },
    { month: 'Aug', revenue: 94000, margin: 9800 },
    { month: 'Sep', revenue: 145000, margin: 16200 },
    { month: 'Oct', revenue: 198000, margin: 22100 },
    { month: 'Nov (Proj)', revenue: 230000, margin: 26500 }
  ];

  // Quality Acceptance Trend
  const qualityTrendData = [
    { batch: 'Batch 1-10', passRate: 91.2 },
    { batch: 'Batch 11-20', passRate: 93.8 },
    { batch: 'Batch 21-30', passRate: 96.4 },
    { batch: 'Batch 31-40', passRate: 98.1 }
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Executive Reports & Cluster Analytics</h1>
          <p className="page-subtitle">
            Longitudinal performance audit &bull; Order fulfilment rates &bull; Member income growth
          </p>
        </div>
        <div className="page-actions">
          <button className="btn btn-outline" onClick={() => alert('Generating PDF / Excel Report export...')}>
            <Download size={16} /> Download Quarterly Audit PDF
          </button>
        </div>
      </div>

      {/* KPI Stats */}
      <div className="grid grid-cols-4" style={{ marginBottom: '24px' }}>
        <div className="stat-card">
          <div className="stat-icon primary"><TrendingUp size={22} /></div>
          <div className="stat-info">
            <div className="stat-label">6-Month Gross Turnover</div>
            <div className="stat-value">₹8,57,000</div>
            <div className="stat-sub">Across 14 Bulk Contracts</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon success"><Award size={22} /></div>
          <div className="stat-info">
            <div className="stat-label">On-Time Delivery Rate</div>
            <div className="stat-value">96.8%</div>
            <div className="stat-sub">Zero missed buyer deadlines in Q3</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon secondary"><CheckCircle2 size={22} /></div>
          <div className="stat-info">
            <div className="stat-label">First-Time Quality Pass</div>
            <div className="stat-value">97.4%</div>
            <div className="stat-sub">+6.2% since CV pre-screening</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon accent"><DollarSign size={22} /></div>
          <div className="stat-info">
            <div className="stat-label">Avg. Member Annualized</div>
            <div className="stat-value">₹1,14,000</div>
            <div className="stat-sub">Exceeds Lakhpati Didi criteria</div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-2" style={{ gap: '24px' }}>
        <div className="card">
          <div className="card-header">
            <div>
              <h3 className="card-title">Turnover & Group Net Surplus (₹)</h3>
              <p className="card-subtitle">Monthly revenue progression</p>
            </div>
          </div>
          <div style={{ width: '100%', height: 260 }}>
            <ResponsiveContainer>
              <BarChart data={monthlyRevenueData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#EEF2F5" />
                <XAxis dataKey="month" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip formatter={(val) => `₹${val.toLocaleString()}`} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Bar dataKey="revenue" fill="#123B5D" name="Gross Bulk Revenue" radius={[4, 4, 0, 0]} />
                <Bar dataKey="margin" fill="#168B80" name="SHG Net Reserve Fund" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <div>
              <h3 className="card-title">Quality Acceptance Trend (%)</h3>
              <p className="card-subtitle">Impact of AI-assisted visual pre-inspection</p>
            </div>
          </div>
          <div style={{ width: '100%', height: 260 }}>
            <ResponsiveContainer>
              <LineChart data={qualityTrendData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#EEF2F5" />
                <XAxis dataKey="batch" tick={{ fontSize: 12 }} />
                <YAxis domain={[85, 100]} tick={{ fontSize: 12 }} />
                <Tooltip formatter={(val) => `${val}%`} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Line type="monotone" dataKey="passRate" stroke="#168B80" strokeWidth={3} name="Quality Pass Rate %" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReportsPage;

