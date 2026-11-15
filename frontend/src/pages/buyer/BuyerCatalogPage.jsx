import React from 'react';
import { Link } from 'react-router-dom';
import { Store, ShieldCheck, ArrowRight } from 'lucide-react';
import { DEMO_RETAIL_PRODUCTS } from '../../mock/mockData';

const BuyerCatalogPage = () => {
  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Wholesale Product Catalog & Cluster Capabilities</h1>
          <p className="page-subtitle">
            Verified production lines available for institutional and private-label bulk procurement
          </p>
        </div>
      </div>

      <div className="grid grid-cols-3" style={{ gap: '20px' }}>
        {DEMO_RETAIL_PRODUCTS.map((prod) => (
          <div key={prod.id} className="card" style={{ padding: 0, overflow: 'hidden' }}>
            <div style={{ height: '180px', overflow: 'hidden' }}>
              <img src={prod.imageUrl} alt={prod.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            </div>
            <div style={{ padding: '16px' }}>
              <span className="badge badge-primary" style={{ marginBottom: '6px' }}>{prod.category}</span>
              <h3 style={{ fontSize: '15px', color: '#123B5D', margin: '4px 0' }}>{prod.name}</h3>
              <p style={{ fontSize: '12px', color: '#5e7386', marginBottom: '12px' }}>
                Manufactured by {prod.shgName}, {prod.location}
              </p>
              <div style={{ background: '#F8FAFC', padding: '10px', borderRadius: '6px', fontSize: '12px', marginBottom: '12px' }}>
                <div>Bulk Capacity: <strong>1,000 - 5,000 units / month</strong></div>
                <div>Wholesale Estimate: <strong style={{ color: '#168B80' }}>₹{(prod.price * 0.75).toFixed(0)} / unit</strong></div>
              </div>
              <Link to="/buyer/create" className="btn btn-secondary btn-sm" style={{ width: '100%' }}>
                Request Bulk Contract Quote <ArrowRight size={14} />
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BuyerCatalogPage;

