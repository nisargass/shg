import React from 'react';
import { Boxes, Clock, CheckCircle2, TrendingUp } from 'lucide-react';
import { DEMO_BULK_ORDERS } from '../../mock/mockData';

const FederationProductionPage = () => {
  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Cluster-Wide Bulk Orders & Fulfillment Monitor</h1>
          <p className="page-subtitle">Aggregated production pipeline across Ramanagara Self-Help Groups</p>
        </div>
      </div>

      <div className="card">
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Order ID & Buyer</th>
                <th>Producing SHG</th>
                <th>Product Description</th>
                <th>Target Quantity</th>
                <th>Progress (Actual vs Target)</th>
                <th>Deadline</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {DEMO_BULK_ORDERS.map((ord) => {
                const percent = Math.round((ord.completedQuantity / ord.totalQuantity) * 100);
                return (
                  <tr key={ord.id}>
                    <td>
                      <strong>{ord.id}</strong>
                      <div style={{ fontSize: '11px', color: '#5e7386' }}>{ord.buyerName}</div>
                    </td>
                    <td>
                      <strong>Pragati Mahila Sangha</strong>
                      <div style={{ fontSize: '11px', color: '#5e7386' }}>Channapatna</div>
                    </td>
                    <td>{ord.productName}</td>
                    <td><strong>{ord.totalQuantity} units</strong></td>
                    <td style={{ minWidth: '150px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11.5px', marginBottom: '3px' }}>
                        <span>{ord.completedQuantity} / {ord.totalQuantity}</span>
                        <strong>{percent}%</strong>
                      </div>
                      <div className="progress-bar">
                        <div className="progress-fill" style={{ width: `${percent}%` }}></div>
                      </div>
                    </td>
                    <td>{ord.deadline}</td>
                    <td>
                      <span className="badge badge-secondary">{ord.status.replace('_', ' ')}</span>
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

export default FederationProductionPage;

