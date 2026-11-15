import React, { useState } from 'react';
import {
  Package,
  Layers,
  AlertTriangle,
  CheckCircle2,
  ShieldCheck,
  TrendingUp,
  RefreshCw,
  ShoppingBag,
  Store,
  ArrowRight
} from 'lucide-react';
import { DEMO_INVENTORY } from '../../mock/mockData';

const InventoryPage = () => {
  const [inventory, setInventory] = useState(DEMO_INVENTORY);
  const [filterCategory, setFilterCategory] = useState('ALL');

  const filteredItems = filterCategory === 'ALL'
    ? inventory
    : inventory.filter((item) => item.category.toLowerCase().includes(filterCategory.toLowerCase()));

  return (
    <div>
      <div className="page-header">
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h1 className="page-title">Unified Inventory & Stock Reservation</h1>
            <span className="demo-badge">Multi-Channel Protected</span>
          </div>
          <p className="page-subtitle">
            Shared stock coordination ensuring bulk buyer commitments are never double-sold to retail channels
          </p>
        </div>
        <div className="page-actions">
          <button className="btn btn-primary" onClick={() => alert('New raw material procurement order initialized with supplier.')}>
            <Package size={16} /> Procure Material
          </button>
        </div>
      </div>

      {/* Critical Stock Allocation Policy Alert */}
      <div className="alert-banner info" style={{ marginBottom: '24px' }}>
        <ShieldCheck size={20} />
        <div>
          <strong>Strict Double-Selling Prevention Active</strong>
          <p style={{ margin: '2px 0 0', fontSize: '13px' }}>
            Stock committed to confirmed bulk orders (e.g. 1,440m Canvas & 790 Finished Tote Bags) is cryptographically locked in the backend ledger and hidden from the public retail storefront.
          </p>
        </div>
      </div>

      {/* Category Filter Tabs */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '20px' }}>
        <button
          className={`btn btn-sm ${filterCategory === 'ALL' ? 'btn-primary' : 'btn-outline'}`}
          onClick={() => setFilterCategory('ALL')}
        >
          All Items ({inventory.length})
        </button>
        <button
          className={`btn btn-sm ${filterCategory === 'Raw Material' ? 'btn-primary' : 'btn-outline'}`}
          onClick={() => setFilterCategory('Raw Material')}
        >
          Raw Materials (Fabric, Webbing, Zippers)
        </button>
        <button
          className={`btn btn-sm ${filterCategory === 'Finished Goods' ? 'btn-primary' : 'btn-outline'}`}
          onClick={() => setFilterCategory('Finished Goods')}
        >
          Finished Products (Tote Bags, Table Runners)
        </button>
      </div>

      {/* Inventory Table */}
      <div className="card">
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>SKU & Item Name</th>
                <th>Category & Unit</th>
                <th>Physical Stock</th>
                <th style={{ color: '#123B5D' }}>Reserved (Bulk Order)</th>
                <th style={{ color: '#168B80' }}>Reserved (Retail)</th>
                <th style={{ color: '#22C55E' }}>Freely Available</th>
                <th>Reorder Level</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {filteredItems.map((item) => {
                const isLow = item.freeAvailableStock <= item.reorderLevel;
                return (
                  <tr key={item.sku}>
                    <td>
                      <strong>{item.name}</strong>
                      <div style={{ fontSize: '11.5px', color: '#5e7386' }}>SKU: {item.sku} &bull; Supplier: {item.supplier || 'In-House SHG'}</div>
                    </td>
                    <td>
                      <span className="badge badge-neutral">{item.category}</span>
                      <div style={{ fontSize: '11px', color: '#5e7386', marginTop: '2px' }}>{item.unit}</div>
                    </td>
                    <td>
                      <strong style={{ fontSize: '14px' }}>{item.physicalStock.toLocaleString()}</strong>
                    </td>
                    <td>
                      <span style={{ fontWeight: '700', color: '#123B5D' }}>
                        {item.reservedForBulkOrders.toLocaleString()}
                      </span>
                    </td>
                    <td>
                      <span style={{ fontWeight: '600', color: '#168B80' }}>
                        {item.reservedForRetailOrders.toLocaleString()}
                      </span>
                    </td>
                    <td>
                      <strong style={{ fontSize: '15px', color: isLow ? '#C83D43' : '#168B80' }}>
                        {item.freeAvailableStock.toLocaleString()}
                      </strong>
                    </td>
                    <td>{item.reorderLevel} {item.unit}</td>
                    <td>
                      {isLow ? (
                        <span className="badge badge-alert">LOW STOCK ALERT</span>
                      ) : (
                        <span className="badge badge-success">HEALTHY</span>
                      )}
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

export default InventoryPage;

