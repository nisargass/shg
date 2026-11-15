import React, { useState } from 'react';
import {
  Store,
  ShoppingBag,
  TrendingUp,
  Package,
  Plus,
  Sparkles,
  ShieldCheck,
  Eye,
  CheckCircle2
} from 'lucide-react';
import { DEMO_RETAIL_PRODUCTS } from '../../mock/mockData';

const RetailManagementPage = () => {
  const [products] = useState(DEMO_RETAIL_PRODUCTS);

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Retail Marketplace & Storefront Management</h1>
          <p className="page-subtitle">
            Direct-to-consumer artisanal listings synchronized with shared inventory controls
          </p>
        </div>
        <div className="page-actions">
          <button className="btn btn-primary" onClick={() => alert('New retail product listing modal opened.')}>
            <Plus size={16} /> List New Artisan Product
          </button>
        </div>
      </div>

      {/* Cross-channel Protection Alert */}
      <div className="alert-banner info" style={{ marginBottom: '24px' }}>
        <ShieldCheck size={20} />
        <div>
          <strong>Shared Inventory Guard: Retail Stock is Strictly Surplus Only</strong>
          <p style={{ margin: '2px 0 0', fontSize: '13px' }}>
            Products listed here reflect only <strong>Free Available Stock</strong> after reserving quantities for accepted institutional bulk buyer orders.
          </p>
        </div>
      </div>

      {/* AI Demand Forecast Banner */}
      <div className="card" style={{ marginBottom: '24px', background: '#fdfaf4', border: '1px solid #faebcc' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Sparkles size={20} color="#E6A23C" />
          <div>
            <strong style={{ fontSize: '14px', color: '#ab711b' }}>AI Retail Demand Forecast (Deepavali Fairs)</strong>
            <p style={{ margin: '2px 0 0', fontSize: '12.5px', color: '#5e7386' }}>
              Projected 40% rise in demand for <strong>Kasuti Table Runners</strong> and <strong>Channapatna Wooden Desk Organizers</strong> over next 3 weeks. Recommended buffer: reserve 15 extra units in workshop bin.
            </p>
          </div>
        </div>
      </div>

      {/* Product Listings Table */}
      <div className="card">
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Product & Craft Name</th>
                <th>Category</th>
                <th>Retail Price</th>
                <th>Surplus Available Stock</th>
                <th>Customer Rating</th>
                <th>Storefront Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {products.map((p) => (
                <tr key={p.id}>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      <img
                        src={p.imageUrl}
                        alt={p.name}
                        style={{ width: '44px', height: '44px', borderRadius: '6px', objectFit: 'cover' }}
                      />
                      <div>
                        <strong>{p.name}</strong>
                        <div style={{ fontSize: '11px', color: '#5e7386' }}>ID: {p.id}</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <span className="badge badge-neutral">{p.category}</span>
                  </td>
                  <td>
                    <strong>₹{p.price.toFixed(2)}</strong>
                    <div style={{ fontSize: '11px', color: '#899ba8', textDecoration: 'line-through' }}>
                      ₹{p.originalPrice.toFixed(2)}
                    </div>
                  </td>
                  <td>
                    <strong style={{ fontSize: '14px', color: p.availableStock < 5 ? '#C83D43' : '#168B80' }}>
                      {p.availableStock} units
                    </strong>
                  </td>
                  <td>
                    <span style={{ fontSize: '12.5px', fontWeight: '700', color: '#ab711b' }}>
                      ★ {p.rating} ({p.reviewsCount})
                    </span>
                  </td>
                  <td>
                    <span className="badge badge-success">ACTIVE IN STORE</span>
                  </td>
                  <td>
                    <button className="btn btn-sm btn-outline" onClick={() => alert(`Editing listing for ${p.name}...`)}>
                      Edit Details
                    </button>
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

export default RetailManagementPage;

