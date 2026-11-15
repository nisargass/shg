import React, { useState } from 'react';
import {
  Building2,
  Phone,
  MapPin,
  Clock,
  Star,
  FileText,
  CheckCircle,
  Truck,
  Plus
} from 'lucide-react';
import { DEMO_SUPPLIERS } from '../../mock/mockData';

const SuppliersPage = () => {
  const [suppliers] = useState(DEMO_SUPPLIERS);

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Supplier & Procurement Management</h1>
          <p className="page-subtitle">
            Verified raw material vendors, bulk quotations, lead time tracking, and procurement contracts
          </p>
        </div>
        <div className="page-actions">
          <button className="btn btn-primary" onClick={() => alert('New Supplier Onboarding form initiated.')}>
            <Plus size={16} /> Register New Supplier
          </button>
        </div>
      </div>

      <div className="grid grid-cols-3" style={{ gap: '20px' }}>
        {suppliers.map((sup) => (
          <div key={sup.id} className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
              <div>
                <span className="badge badge-primary">{sup.id}</span>
                <h3 style={{ fontSize: '16px', color: '#123B5D', marginTop: '6px' }}>{sup.name}</h3>
                <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '12px', color: '#5e7386', marginTop: '2px' }}>
                  <MapPin size={13} /> {sup.city}
                </div>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '4px', background: '#fef4e8', padding: '3px 8px', borderRadius: '4px', color: '#ab711b', fontWeight: '700', fontSize: '12px' }}>
                <Star size={14} fill="#E6A23C" color="#E6A23C" /> {sup.rating}
              </div>
            </div>

            <div style={{ borderTop: '1px solid #EEF2F5', borderBottom: '1px solid #EEF2F5', padding: '12px 0', margin: '12px 0', fontSize: '13px' }}>
              <div style={{ marginBottom: '6px' }}>
                <span style={{ color: '#5e7386' }}>Contact:</span> <strong>{sup.contactPerson}</strong> ({sup.phone})
              </div>
              <div style={{ marginBottom: '6px' }}>
                <span style={{ color: '#5e7386' }}>Lead Time:</span> <strong>{sup.leadTimeDays} business days</strong>
              </div>
              <div>
                <span style={{ color: '#5e7386' }}>Recent Quote:</span> <strong style={{ color: '#168B80' }}>{sup.lastQuotePrice}</strong>
              </div>
            </div>

            <div style={{ marginBottom: '14px' }}>
              <span style={{ fontSize: '11px', color: '#5e7386', textTransform: 'uppercase', fontWeight: '600' }}>Supplied Materials:</span>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginTop: '6px' }}>
                {sup.materials.map((m, mIdx) => (
                  <span key={mIdx} className="badge badge-neutral" style={{ fontSize: '11px' }}>
                    {m}
                  </span>
                ))}
              </div>
            </div>

            <div style={{ fontSize: '11.5px', color: '#5e7386', background: '#F8FAFC', padding: '8px', borderRadius: '6px' }}>
              <strong>Payment Terms:</strong> {sup.paymentTerms}
            </div>

            <div style={{ display: 'flex', gap: '8px', marginTop: '14px' }}>
              <button className="btn btn-sm btn-outline" style={{ flex: 1 }} onClick={() => alert(`Requesting updated quotation from ${sup.name}...`)}>
                Request Quote
              </button>
              <button className="btn btn-sm btn-secondary" style={{ flex: 1 }} onClick={() => alert(`Creating Purchase Order for ${sup.name}...`)}>
                Create Material PO
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SuppliersPage;

