import React, { useState } from 'react';
import {
  ShoppingBag,
  Plus,
  FileText,
  Upload,
  CheckCircle,
  Clock,
  AlertTriangle,
  Sparkles,
  Eye,
  Filter,
  Calendar,
  DollarSign
} from 'lucide-react';
import { DEMO_BULK_ORDERS } from '../../mock/mockData';
import { orderApi } from '../../api/services';

const OrdersPage = () => {
  const [orders, setOrders] = useState(DEMO_BULK_ORDERS);
  const [selectedOrder, setSelectedOrder] = useState(DEMO_BULK_ORDERS[0]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');

  // OCR state simulation
  const [ocrLoading, setOcrLoading] = useState(false);
  const [ocrVerified, setOcrVerified] = useState(false);
  const [ocrResult, setOcrResult] = useState({
    extractedBuyer: 'EcoFab Bangalore Retailers Ltd.',
    extractedQty: 1200,
    extractedPrice: 165.0,
    extractedDeadline: '2026-11-20',
    confidenceScore: 96.4,
    unverifiedFields: ['Packing Carton Dimension Specification']
  });

  // New order form state
  const [newOrderForm, setNewOrderForm] = useState({
    buyerName: '',
    productName: '',
    category: 'Garments & Textiles',
    totalQuantity: '',
    unitAgreedPrice: '',
    deadline: '',
    specifications: ''
  });

  const handleCreateOrder = async (e) => {
    e.preventDefault();
    const created = await orderApi.createOrder(newOrderForm);
    setOrders([created, ...orders]);
    setSelectedOrder(created);
    setShowCreateModal(false);
    setNewOrderForm({
      buyerName: '',
      productName: '',
      category: 'Garments & Textiles',
      totalQuantity: '',
      unitAgreedPrice: '',
      deadline: '',
      specifications: ''
    });
  };

  const simulateOcrScan = () => {
    setOcrLoading(true);
    setTimeout(() => {
      setOcrLoading(false);
      setOcrVerified(true);
    }, 1200);
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Bulk Order Management</h1>
          <p className="page-subtitle">
            Lifecycle monitoring from Purchase Order OCR verification to final shipment delivery
          </p>
        </div>
        <div className="page-actions">
          <button className="btn btn-primary" onClick={() => setShowCreateModal(true)}>
            <Plus size={16} /> Create Bulk Order
          </button>
        </div>
      </div>

      {/* Orders Grid / Master-Detail layout */}
      <div className="grid grid-cols-12" style={{ gap: '24px' }}>
        {/* Left Column: Orders List */}
        <div style={{ gridColumn: 'span 5' }}>
          <div className="card" style={{ padding: 0 }}>
            <div style={{ padding: '16px', borderBottom: '1px solid #EEF2F5', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <strong style={{ fontSize: '14px', color: '#123B5D' }}>All Active Inquiries & Contracts ({orders.length})</strong>
              <span className="badge badge-neutral">FastAPI Synced</span>
            </div>
            <div style={{ maxHeight: '680px', overflowY: 'auto' }}>
              {orders.map((ord) => {
                const isSelected = selectedOrder.id === ord.id;
                const percent = Math.round((ord.completedQuantity / ord.totalQuantity) * 100);
                return (
                  <div
                    key={ord.id}
                    onClick={() => {
                      setSelectedOrder(ord);
                      setOcrVerified(false);
                    }}
                    style={{
                      padding: '16px',
                      borderBottom: '1px solid #EEF2F5',
                      cursor: 'pointer',
                      background: isSelected ? '#f1f8f7' : '#FFFFFF',
                      borderLeft: isSelected ? '4px solid #168B80' : '4px solid transparent',
                      transition: 'all 0.15s ease'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                      <strong style={{ fontSize: '13px', color: '#123B5D' }}>{ord.id}</strong>
                      <span className={`badge ${ord.status === 'IN_PRODUCTION' ? 'badge-secondary' : 'badge-accent'}`}>
                        {ord.status.replace('_', ' ')}
                      </span>
                    </div>
                    <div style={{ fontSize: '13.5px', fontWeight: '600', color: '#243746', marginBottom: '4px' }}>
                      {ord.productName}
                    </div>
                    <div style={{ fontSize: '12px', color: '#5e7386', marginBottom: '8px' }}>
                      Buyer: <strong>{ord.buyerName}</strong>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
                      <span>Qty: <strong>{ord.totalQuantity}</strong></span>
                      <span>Total: <strong>₹{ord.totalOrderValue.toLocaleString()}</strong></span>
                    </div>
                    <div className="progress-bar" style={{ height: '6px' }}>
                      <div className="progress-fill" style={{ width: `${percent}%` }}></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Right Column: Detailed Order Inspector */}
        <div style={{ gridColumn: 'span 7' }}>
          <div className="card">
            {/* Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', paddingBottom: '16px', borderBottom: '1px solid #EEF2F5', flexWrap: 'wrap', gap: '10px' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span className="badge badge-primary">{selectedOrder.id}</span>
                  <span className="badge badge-secondary">{selectedOrder.category}</span>
                </div>
                <h2 style={{ fontSize: '20px', color: '#123B5D', marginTop: '6px' }}>
                  {selectedOrder.productName}
                </h2>
                <div style={{ fontSize: '13px', color: '#5e7386', marginTop: '2px' }}>
                  Buyer: <strong>{selectedOrder.buyerName}</strong> &bull; Order Date: {selectedOrder.orderDate}
                </div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '22px', fontWeight: '800', color: '#168B80' }}>
                  ₹{selectedOrder.totalOrderValue.toLocaleString()}
                </div>
                <div style={{ fontSize: '12px', color: '#5e7386' }}>
                  @ ₹{selectedOrder.unitAgreedPrice} per unit agreed
                </div>
              </div>
            </div>

            {/* Sub-Tabs */}
            <div style={{ display: 'flex', gap: '10px', margin: '16px 0', borderBottom: '1px solid #EEF2F5', paddingBottom: '8px' }}>
              <button
                className={`btn btn-sm ${activeTab === 'overview' ? 'btn-primary' : 'btn-outline'}`}
                onClick={() => setActiveTab('overview')}
              >
                Specifications & Target
              </button>
              <button
                className={`btn btn-sm ${activeTab === 'ocr' ? 'btn-primary' : 'btn-outline'}`}
                onClick={() => setActiveTab('ocr')}
              >
                <FileText size={14} /> OCR Document Extraction
              </button>
              <button
                className={`btn btn-sm ${activeTab === 'lifecycle' ? 'btn-primary' : 'btn-outline'}`}
                onClick={() => setActiveTab('lifecycle')}
              >
                Fulfillment Milestones
              </button>
            </div>

            {/* Tab 1: Specifications */}
            {activeTab === 'overview' && (
              <div>
                <div className="grid grid-cols-3" style={{ marginBottom: '20px' }}>
                  <div style={{ padding: '14px', background: '#f8fafc', borderRadius: '8px', border: '1px solid #EEF2F5' }}>
                    <span style={{ fontSize: '12px', color: '#5e7386' }}>Contract Target Qty</span>
                    <div style={{ fontSize: '18px', fontWeight: '700', color: '#123B5D' }}>{selectedOrder.totalQuantity} units</div>
                  </div>
                  <div style={{ padding: '14px', background: '#f8fafc', borderRadius: '8px', border: '1px solid #EEF2F5' }}>
                    <span style={{ fontSize: '12px', color: '#5e7386' }}>Verified Completed</span>
                    <div style={{ fontSize: '18px', fontWeight: '700', color: '#168B80' }}>{selectedOrder.completedQuantity} units</div>
                  </div>
                  <div style={{ padding: '14px', background: '#f8fafc', borderRadius: '8px', border: '1px solid #EEF2F5' }}>
                    <span style={{ fontSize: '12px', color: '#5e7386' }}>Deadline Feasibility</span>
                    <div style={{ fontSize: '18px', fontWeight: '700', color: selectedOrder.daysRemaining < 15 ? '#C83D43' : '#123B5D' }}>
                      {selectedOrder.deadline}
                    </div>
                  </div>
                </div>

                <div style={{ marginBottom: '16px' }}>
                  <strong style={{ fontSize: '13.5px', color: '#123B5D', display: 'block', marginBottom: '6px' }}>
                    Buyer Technical Specifications:
                  </strong>
                  <div style={{ padding: '14px', background: '#F8FAFC', borderRadius: '8px', border: '1px solid #DCE3E8', fontSize: '13px', lineHeight: '1.6' }}>
                    {selectedOrder.specifications}
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '12px', marginTop: '20px' }}>
                  <a href={`/leader/allocation?orderId=${selectedOrder.id}`} className="btn btn-secondary">
                    <Sparkles size={16} /> Open Work Allocation Matrix
                  </a>
                  <a href={`/leader/pricing?orderId=${selectedOrder.id}`} className="btn btn-outline">
                    <DollarSign size={16} /> Inspect Pricing & Costing
                  </a>
                </div>
              </div>
            )}

            {/* Tab 2: OCR Document Processing */}
            {activeTab === 'ocr' && (
              <div>
                <div className="alert-banner info" style={{ marginBottom: '16px' }}>
                  <FileText size={18} />
                  <div>
                    <strong>Purchase Order OCR & Verification Engine</strong>
                    <p style={{ margin: '2px 0 0', fontSize: '12.5px' }}>
                      FastAPI integrates with the AI Microservice OCR pipeline. Extracted metadata requires human leader sign-off.
                    </p>
                  </div>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '14px', border: '1px solid #DCE3E8', borderRadius: '8px', marginBottom: '16px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <FileText size={28} color="#168B80" />
                    <div>
                      <strong style={{ fontSize: '13.5px' }}>{selectedOrder.poDocumentName}</strong>
                      <div style={{ fontSize: '11.5px', color: '#5e7386' }}>Uploaded PDF &bull; 1.4 MB &bull; Signed Digital Stamp</div>
                    </div>
                  </div>
                  <button className="btn btn-outline btn-sm" onClick={simulateOcrScan} disabled={ocrLoading}>
                    {ocrLoading ? 'Scanning Document...' : 'Re-Run OCR Scanner'}
                  </button>
                </div>

                <div style={{ background: '#F8FAFC', border: '1px solid #DCE3E8', borderRadius: '8px', padding: '16px', marginBottom: '16px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px' }}>
                    <strong style={{ fontSize: '13px', color: '#123B5D' }}>Extracted Fields (Backend OCR)</strong>
                    <span className="badge badge-success" style={{ fontSize: '11px' }}>
                      Confidence: {ocrResult.confidenceScore}%
                    </span>
                  </div>

                  <div className="grid grid-cols-2" style={{ gap: '12px', fontSize: '13px' }}>
                    <div>
                      <span style={{ color: '#5e7386', fontSize: '11.5px' }}>Buyer Name:</span>
                      <div><strong>{ocrResult.extractedBuyer}</strong></div>
                    </div>
                    <div>
                      <span style={{ color: '#5e7386', fontSize: '11.5px' }}>Contracted Quantity:</span>
                      <div><strong>{ocrResult.extractedQty} units</strong></div>
                    </div>
                    <div>
                      <span style={{ color: '#5e7386', fontSize: '11.5px' }}>Unit Agreed Price:</span>
                      <div><strong>₹{ocrResult.extractedPrice}</strong></div>
                    </div>
                    <div>
                      <span style={{ color: '#5e7386', fontSize: '11.5px' }}>Extracted Delivery Date:</span>
                      <div><strong>{ocrResult.extractedDeadline}</strong></div>
                    </div>
                  </div>

                  <div style={{ marginTop: '14px', padding: '10px', background: '#fdfaf4', borderRadius: '6px', border: '1px solid #faebcc', fontSize: '12px' }}>
                    <span style={{ color: '#ab711b', fontWeight: '700' }}>Review Field: </span>
                    <span>{ocrResult.unverifiedFields[0]} needs human confirmation against master sample standard.</span>
                  </div>
                </div>

                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
                  {ocrVerified ? (
                    <span className="badge badge-success" style={{ padding: '8px 14px', fontSize: '13px' }}>
                      <CheckCircle size={16} /> Document Verified by Leader
                    </span>
                  ) : (
                    <button className="btn btn-secondary" onClick={() => setOcrVerified(true)}>
                      <CheckCircle size={16} /> Confirm & Verify Document Data
                    </button>
                  )}
                </div>
              </div>
            )}

            {/* Tab 3: Lifecycle */}
            {activeTab === 'lifecycle' && (
              <div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  <div style={{ display: 'flex', gap: '14px', alignItems: 'flex-start' }}>
                    <CheckCircle size={20} color="#168B80" style={{ flexShrink: 0, marginTop: '2px' }} />
                    <div>
                      <strong style={{ fontSize: '13px' }}>1. PO Document Upload & OCR</strong>
                      <p style={{ fontSize: '12px', color: '#5e7386', margin: 0 }}>Completed &bull; PO verified on {selectedOrder.orderDate}</p>
                    </div>
                  </div>
                  <div style={{ display: 'flex', gap: '14px', alignItems: 'flex-start' }}>
                    <CheckCircle size={20} color="#168B80" style={{ flexShrink: 0, marginTop: '2px' }} />
                    <div>
                      <strong style={{ fontSize: '13px' }}>2. Pricing & Costing Analysis</strong>
                      <p style={{ fontSize: '12px', color: '#5e7386', margin: 0 }}>Completed &bull; Profit margin protected at 8.12%</p>
                    </div>
                  </div>
                  <div style={{ display: 'flex', gap: '14px', alignItems: 'flex-start' }}>
                    <CheckCircle size={20} color={selectedOrder.allocationStatus === 'APPROVED' ? '#168B80' : '#E6A23C'} style={{ flexShrink: 0, marginTop: '2px' }} />
                    <div>
                      <strong style={{ fontSize: '13px' }}>3. AI Work Allocation & Leader Approval</strong>
                      <p style={{ fontSize: '12px', color: '#5e7386', margin: 0 }}>
                        {selectedOrder.allocationStatus === 'APPROVED' ? 'Approved & distributed to 7 members' : 'Proposal pending leader review'}
                      </p>
                    </div>
                  </div>
                  <div style={{ display: 'flex', gap: '14px', alignItems: 'flex-start' }}>
                    <Clock size={20} color="#E6A23C" style={{ flexShrink: 0, marginTop: '2px' }} />
                    <div>
                      <strong style={{ fontSize: '13px' }}>4. Distributed Member Production & Monitoring</strong>
                      <p style={{ fontSize: '12px', color: '#5e7386', margin: 0 }}>Active &bull; {selectedOrder.completedQuantity} of {selectedOrder.totalQuantity} units verified</p>
                    </div>
                  </div>
                  <div style={{ display: 'flex', gap: '14px', alignItems: 'flex-start' }}>
                    <Clock size={20} color="#899ba8" style={{ flexShrink: 0, marginTop: '2px' }} />
                    <div>
                      <strong style={{ fontSize: '13px' }}>5. AI Quality Control & Batch Packing</strong>
                      <p style={{ fontSize: '12px', color: '#5e7386', margin: 0 }}>In progress &bull; 790 units approved</p>
                    </div>
                  </div>
                  <div style={{ display: 'flex', gap: '14px', alignItems: 'flex-start' }}>
                    <Clock size={20} color="#899ba8" style={{ flexShrink: 0, marginTop: '2px' }} />
                    <div>
                      <strong style={{ fontSize: '13px' }}>6. Transparent Group Payout Approval</strong>
                      <p style={{ fontSize: '12px', color: '#5e7386', margin: 0 }}>Pending final milestone completion</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Modal: Create Bulk Order */}
      {showCreateModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3 style={{ fontSize: '17px', color: '#123B5D' }}>Create New Bulk Order Ingestion</h3>
              <button onClick={() => setShowCreateModal(false)} style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer' }}>&times;</button>
            </div>
            <form onSubmit={handleCreateOrder}>
              <div className="modal-body">
                <div className="form-group">
                  <label className="form-label">Buyer / Institution Name</label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="e.g. FabIndia Bangalore Regional Supply"
                    value={newOrderForm.buyerName}
                    onChange={(e) => setNewOrderForm({ ...newOrderForm, buyerName: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Product Name & Specifications</label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="e.g. Heavy Duty Canvas Shopping Tote Bags"
                    value={newOrderForm.productName}
                    onChange={(e) => setNewOrderForm({ ...newOrderForm, productName: e.target.value })}
                    required
                  />
                </div>
                <div className="grid grid-cols-2" style={{ gap: '14px' }}>
                  <div className="form-group">
                    <label className="form-label">Total Quantity (Units)</label>
                    <input
                      type="number"
                      className="form-control"
                      placeholder="e.g. 1000"
                      value={newOrderForm.totalQuantity}
                      onChange={(e) => setNewOrderForm({ ...newOrderForm, totalQuantity: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Agreed Unit Selling Price (₹)</label>
                    <input
                      type="number"
                      className="form-control"
                      placeholder="e.g. 175"
                      value={newOrderForm.unitAgreedPrice}
                      onChange={(e) => setNewOrderForm({ ...newOrderForm, unitAgreedPrice: e.target.value })}
                      required
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label className="form-label">Delivery Deadline</label>
                  <input
                    type="date"
                    className="form-control"
                    value={newOrderForm.deadline}
                    onChange={(e) => setNewOrderForm({ ...newOrderForm, deadline: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Detailed Craft / Product Specifications</label>
                  <textarea
                    className="form-control"
                    rows="3"
                    placeholder="Specify fabric GSM, handle cross-stitching, zipper type, FSSAI seal requirements..."
                    value={newOrderForm.specifications}
                    onChange={(e) => setNewOrderForm({ ...newOrderForm, specifications: e.target.value })}
                    required
                  ></textarea>
                </div>
                <div style={{ padding: '12px', border: '2px dashed #DCE3E8', borderRadius: '8px', textAlign: 'center', background: '#F8FAFC' }}>
                  <Upload size={22} color="#168B80" style={{ margin: '0 auto 6px' }} />
                  <div style={{ fontSize: '12px', fontWeight: '600' }}>Attach Buyer Purchase Order (PDF/Image)</div>
                  <div style={{ fontSize: '11px', color: '#5e7386' }}>FastAPI OCR will automatically extract spec metadata</div>
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-outline" onClick={() => setShowCreateModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary">Create Order & Generate Allocation</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default OrdersPage;

