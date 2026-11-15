import React from 'react';
import { Link } from 'react-router-dom';
import {
  ShoppingBag,
  Clock,
  CheckCircle2,
  Truck,
  Plus,
  ArrowRight,
  FileText,
  ShieldCheck
} from 'lucide-react';
import { DEMO_BULK_ORDERS } from '../../mock/mockData';

const BuyerDashboard = () => {
  const buyerOrder = DEMO_BULK_ORDERS[0]; // EcoFab order

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Wholesale Buyer Operations Portal</h1>
          <p className="page-subtitle">
            EcoFab Bangalore Retailers Ltd. &bull; Sourcing from Pragati Mahila Sangha
          </p>
        </div>
        <div className="page-actions">
          <Link to="/buyer/create" className="btn btn-primary">
            <Plus size={16} /> Place New Bulk Contract
          </Link>
        </div>
      </div>

      {/* KPI Stats */}
      <div className="grid grid-cols-4" style={{ marginBottom: '24px' }}>
        <div className="stat-card">
          <div className="stat-icon primary"><ShoppingBag size={22} /></div>
          <div className="stat-info">
            <div className="stat-label">Active Sourcing Orders</div>
            <div className="stat-value">1 Bulk Order</div>
            <div className="stat-sub">1,200 Total Bags</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon secondary"><Clock size={22} /></div>
          <div className="stat-info">
            <div className="stat-label">Production Completed</div>
            <div className="stat-value">{buyerOrder.completedQuantity} Units</div>
            <div className="stat-sub">70% of target fulfilled</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon success"><CheckCircle2 size={22} /></div>
          <div className="stat-info">
            <div className="stat-label">Passed QC Inspection</div>
            <div className="stat-value">{buyerOrder.approvedQuantity} Units</div>
            <div className="stat-sub">98.2% acceptance rate</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon accent"><Truck size={22} /></div>
          <div className="stat-info">
            <div className="stat-label">Batch 1 Dispatched</div>
            <div className="stat-value">500 Units</div>
            <div className="stat-sub">In transit via VRL Logistics</div>
          </div>
        </div>
      </div>

      {/* Live Order Tracker (Without private member data) */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <div>
            <h3 className="card-title">Live Contract Progress: {buyerOrder.id}</h3>
            <p className="card-subtitle">{buyerOrder.productName} &bull; Delivery Cutoff: {buyerOrder.deadline}</p>
          </div>
          <Link to="/buyer/orders" className="btn btn-sm btn-outline">
            Full Tracking Details <ArrowRight size={14} />
          </Link>
        </div>

        <div style={{ marginBottom: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '6px' }}>
            <span>Verified Finished Stock</span>
            <strong>{buyerOrder.completedQuantity} / {buyerOrder.totalQuantity} units ({Math.round((buyerOrder.completedQuantity / buyerOrder.totalQuantity) * 100)}%)</strong>
          </div>
          <div className="progress-bar" style={{ height: '12px' }}>
            <div className="progress-fill" style={{ width: `${(buyerOrder.completedQuantity / buyerOrder.totalQuantity) * 100}%` }}></div>
          </div>
        </div>

        <div className="grid grid-cols-4" style={{ gap: '16px', background: '#F8FAFC', padding: '16px', borderRadius: '8px', border: '1px solid #EEF2F5', fontSize: '12.5px' }}>
          <div>
            <span style={{ color: '#5e7386', display: 'block' }}>Contract Value:</span>
            <strong>₹{buyerOrder.totalOrderValue.toLocaleString()}</strong> (@ ₹{buyerOrder.unitAgreedPrice}/unit)
          </div>
          <div>
            <span style={{ color: '#5e7386', display: 'block' }}>Estimated Arrival:</span>
            <strong style={{ color: '#168B80' }}>Nov 08, 2026 (Batch 1)</strong>
          </div>
          <div>
            <span style={{ color: '#5e7386', display: 'block' }}>Carrier Partner:</span>
            <strong>VRL Rural Express (KA-42-B-8912)</strong>
          </div>
          <div>
            <span style={{ color: '#5e7386', display: 'block' }}>Quality Standard:</span>
            <span className="badge badge-success">Passed Export QC</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BuyerDashboard;

