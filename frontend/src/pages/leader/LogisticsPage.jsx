import React, { useState } from 'react';
import {
  Truck,
  Package,
  MapPin,
  Clock,
  CheckCircle2,
  AlertTriangle,
  FileText,
  DollarSign,
  Sparkles,
  ArrowRight
} from 'lucide-react';
import { DEMO_LOGISTICS } from '../../mock/mockData';

const LogisticsPage = () => {
  const [shipments] = useState(DEMO_LOGISTICS);
  const [activeTab, setActiveTab] = useState('ALL');

  const filtered = activeTab === 'ALL'
    ? shipments
    : shipments.filter((s) => s.type === activeTab);

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Transportation & Logistics Coordination</h1>
          <p className="page-subtitle">
            Coordinated freight management for inbound raw materials and outbound finished carton shipments
          </p>
        </div>
        <div className="page-actions">
          <button className="btn btn-primary" onClick={() => alert('New Shipment Dispatch created.')}>
            <Truck size={16} /> Schedule Shipment
          </button>
        </div>
      </div>

      {/* AI Freight Consolidation Advice */}
      <div className="alert-banner info" style={{ marginBottom: '24px' }}>
        <Sparkles size={20} />
        <div>
          <strong>AI Route Optimization Recommendation:</strong>
          <p style={{ margin: '2px 0 0', fontSize: '13px' }}>
            Consolidating Outbound Batch 1 (Peenya, Bangalore) with the nearby Ramanagara Channapatna woodcraft pickup saves <strong>₹450</strong> on shared truck freight.
          </p>
        </div>
      </div>

      {/* Logistics Type Tabs */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '20px' }}>
        <button
          className={`btn btn-sm ${activeTab === 'ALL' ? 'btn-primary' : 'btn-outline'}`}
          onClick={() => setActiveTab('ALL')}
        >
          All Logistics ({shipments.length})
        </button>
        <button
          className={`btn btn-sm ${activeTab === 'OUTBOUND' ? 'btn-primary' : 'btn-outline'}`}
          onClick={() => setActiveTab('OUTBOUND')}
        >
          Outbound (Buyer Delivery Dispatches)
        </button>
        <button
          className={`btn btn-sm ${activeTab === 'INBOUND' ? 'btn-primary' : 'btn-outline'}`}
          onClick={() => setActiveTab('INBOUND')}
        >
          Inbound (Raw Material Consignments)
        </button>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {filtered.map((ship) => (
          <div key={ship.id} className="card" style={{ padding: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '12px', marginBottom: '14px' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span className="badge badge-primary">{ship.id}</span>
                  <span className={`badge ${ship.type === 'OUTBOUND' ? 'badge-secondary' : 'badge-neutral'}`}>
                    {ship.type}
                  </span>
                  <span className="badge badge-success">
                    {ship.status.replace('_', ' ')}
                  </span>
                </div>
                <h3 style={{ fontSize: '16px', color: '#123B5D', marginTop: '6px' }}>
                  {ship.cargoDescription}
                </h3>
                <div style={{ fontSize: '13px', color: '#5e7386', marginTop: '2px' }}>
                  {ship.type === 'OUTBOUND' ? `Recipient: ${ship.recipient}` : `Origin Supplier: ${ship.supplierName}`}
                </div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '18px', fontWeight: '800', color: '#123B5D' }}>
                  ₹{ship.transportCost.toLocaleString()}
                </div>
                <div style={{ fontSize: '11.5px', color: '#5e7386' }}>Freight Cost Billed</div>
              </div>
            </div>

            <div className="grid grid-cols-3" style={{ background: '#F8FAFC', padding: '14px', borderRadius: '8px', border: '1px solid #EEF2F5', fontSize: '12.5px', gap: '12px' }}>
              <div>
                <span style={{ color: '#5e7386', display: 'block', fontSize: '11px' }}>Destination / Hub:</span>
                <strong>{ship.destination}</strong>
              </div>
              <div>
                <span style={{ color: '#5e7386', display: 'block', fontSize: '11px' }}>Logistics Partner & Vehicle:</span>
                <strong>{ship.carrierName}</strong> &bull; {ship.vehicleNumber}
              </div>
              <div>
                <span style={{ color: '#5e7386', display: 'block', fontSize: '11px' }}>Assigned Driver Contact:</span>
                <strong>{ship.driverName}</strong>
              </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '14px', fontSize: '12px', color: '#5e7386' }}>
              <div>
                Dispatch Date: <strong>{ship.dispatchDate}</strong> &bull; Est. Delivery: <strong>{ship.expectedDelivery}</strong>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#168B80', cursor: 'pointer' }} onClick={() => alert(`Opening Proof of Pickup document: ${ship.proofOfPickup}`)}>
                <FileText size={14} /> View Waybill / Proof of Pickup
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LogisticsPage;

