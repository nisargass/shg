import React from 'react';
import {
  Clock,
  CheckCircle2,
  Truck,
  FileText,
  ShieldCheck,
  Package,
  Layers
} from 'lucide-react';
import { DEMO_BULK_ORDERS, DEMO_LOGISTICS } from '../../mock/mockData';

const BuyerOrdersPage = () => {
  const order = DEMO_BULK_ORDERS[0];
  const shipment = DEMO_LOGISTICS[0];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Live Contract Production Tracker</h1>
          <p className="page-subtitle">
            Transparent milestone inspection without compromising artisan workshop privacy
          </p>
        </div>
      </div>

      <div className="card" style={{ marginBottom: '24px', padding: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '14px', marginBottom: '16px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span className="badge badge-primary">{order.id}</span>
              <span className="badge badge-secondary">IN PRODUCTION</span>
            </div>
            <h2 style={{ fontSize: '20px', color: '#123B5D', marginTop: '6px' }}>
              {order.productName}
            </h2>
            <div style={{ fontSize: '13px', color: '#5e7386' }}>
              Producer: <strong>Pragati Mahila Sangha (Channapatna Cluster)</strong> &bull; Cutoff: {order.deadline}
            </div>
          </div>

          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '22px', fontWeight: '800', color: '#168B80' }}>
              840 / 1,200 Finished
            </div>
            <div style={{ fontSize: '12px', color: '#5e7386' }}>70% target achieved</div>
          </div>
        </div>

        {/* Milestone Steps */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px', margin: '24px 0' }}>
          <div style={{ padding: '14px', background: '#e8f5e9', borderRadius: '8px', border: '1px solid #c8e6c9' }}>
            <span style={{ fontSize: '11px', color: '#2e7d32', fontWeight: '700' }}>STAGE 1</span>
            <div style={{ fontSize: '13.5px', fontWeight: '700', color: '#1b5e20', margin: '4px 0' }}>Fabric & Cutting</div>
            <span className="badge badge-success">100% COMPLETE</span>
          </div>

          <div style={{ padding: '14px', background: '#e8f5e9', borderRadius: '8px', border: '1px solid #c8e6c9' }}>
            <span style={{ fontSize: '11px', color: '#2e7d32', fontWeight: '700' }}>STAGE 2</span>
            <div style={{ fontSize: '13.5px', fontWeight: '700', color: '#1b5e20', margin: '4px 0' }}>Stitching & Assembly</div>
            <span className="badge badge-success">840 UNITS DONE</span>
          </div>

          <div style={{ padding: '14px', background: '#e6f6f4', borderRadius: '8px', border: '1px solid #c2ece7' }}>
            <span style={{ fontSize: '11px', color: '#168B80', fontWeight: '700' }}>STAGE 3</span>
            <div style={{ fontSize: '13.5px', fontWeight: '700', color: '#123B5D', margin: '4px 0' }}>Export Quality Check</div>
            <span className="badge badge-secondary">790 APPROVED</span>
          </div>

          <div style={{ padding: '14px', background: '#fef4e8', borderRadius: '8px', border: '1px solid #faebcc' }}>
            <span style={{ fontSize: '11px', color: '#ab711b', fontWeight: '700' }}>STAGE 4</span>
            <div style={{ fontSize: '13.5px', fontWeight: '700', color: '#8c580c', margin: '4px 0' }}>Carton Freight Dispatch</div>
            <span className="badge badge-accent">BATCH 1 IN TRANSIT</span>
          </div>
        </div>

        {/* In-Transit Shipment Tracking Card */}
        <div style={{ background: '#F8FAFC', padding: '16px', borderRadius: '8px', border: '1px solid #EEF2F5' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <strong style={{ fontSize: '13.5px', color: '#123B5D', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Truck size={16} color="#168B80" /> Active Consignment: {shipment.id}
            </strong>
            <span className="badge badge-success">DISPATCHED</span>
          </div>
          <div style={{ fontSize: '12.5px', color: '#243746', marginBottom: '6px' }}>
            Cargo: {shipment.cargoDescription}
          </div>
          <div style={{ fontSize: '12px', color: '#5e7386' }}>
            Transporter: <strong>{shipment.carrierName}</strong> &bull; Vehicle: <strong>{shipment.vehicleNumber}</strong> &bull; Driver: {shipment.driverName}
          </div>
        </div>
      </div>
    </div>
  );
};

export default BuyerOrdersPage;

