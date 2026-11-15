import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShoppingBag, Upload, CheckCircle2, ArrowRight, FileText } from 'lucide-react';
import { orderApi } from '../../api/services';

const BuyerCreateOrderPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    buyerName: 'EcoFab Bangalore Retailers Ltd.',
    productName: '',
    category: 'Garments & Textiles',
    totalQuantity: '',
    unitAgreedPrice: '',
    deadline: '',
    specifications: ''
  });
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    await orderApi.createOrder(formData);
    setSubmitting(false);
    setSubmitted(true);
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Submit Wholesale Bulk Order Request</h1>
          <p className="page-subtitle">
            Direct institutional contract submission to Pragati Mahila Sangha & verified cluster artisan networks
          </p>
        </div>
      </div>

      {submitted ? (
        <div className="alert-banner success" style={{ marginBottom: '24px' }}>
          <CheckCircle2 size={24} style={{ flexShrink: 0 }} />
          <div>
            <strong style={{ fontSize: '15px' }}>Purchase Order Request Received!</strong>
            <p style={{ margin: '4px 0 0', fontSize: '13px' }}>
              Your inquiry has been sent to the SHG Leader. The Pricing & Allocation Agents are analyzing cluster capacity and will submit a formal quotation within 24 hours.
            </p>
            <div style={{ marginTop: '12px' }}>
              <button className="btn btn-secondary btn-sm" onClick={() => navigate('/buyer')}>
                Return to Dashboard
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div className="card" style={{ maxWidth: '780px', margin: '0 auto', padding: '28px' }}>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">Procuring Company / Buyer Entity</label>
              <input
                type="text"
                className="form-control"
                value={formData.buyerName}
                onChange={(e) => setFormData({ ...formData, buyerName: e.target.value })}
                required
              />
            </div>

            <div className="grid grid-cols-2" style={{ gap: '16px' }}>
              <div className="form-group">
                <label className="form-label">Product Required</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="e.g. Pure Cotton Canvas Tote Bags"
                  value={formData.productName}
                  onChange={(e) => setFormData({ ...formData, productName: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label className="form-label">Category</label>
                <select
                  className="form-control"
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                >
                  <option value="Garments & Textiles">Garments & Textiles</option>
                  <option value="Handicrafts & Decor">Handicrafts & Decor</option>
                  <option value="Food Products">Food Products</option>
                  <option value="Handmade Accessories">Handmade Accessories</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-3" style={{ gap: '16px' }}>
              <div className="form-group">
                <label className="form-label">Total Quantity (Pieces / Jars)</label>
                <input
                  type="number"
                  className="form-control"
                  placeholder="e.g. 1500"
                  value={formData.totalQuantity}
                  onChange={(e) => setFormData({ ...formData, totalQuantity: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label className="form-label">Target Unit Price (₹)</label>
                <input
                  type="number"
                  className="form-control"
                  placeholder="e.g. 165"
                  value={formData.unitAgreedPrice}
                  onChange={(e) => setFormData({ ...formData, unitAgreedPrice: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label className="form-label">Required Delivery Cutoff Date</label>
                <input
                  type="date"
                  className="form-control"
                  value={formData.deadline}
                  onChange={(e) => setFormData({ ...formData, deadline: e.target.value })}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Technical & Quality Specifications (GSM, Dye, Branding, Packaging)</label>
              <textarea
                className="form-control"
                rows="4"
                placeholder="Include details regarding stitching tension, handles, logo print artwork, packaging cartons..."
                value={formData.specifications}
                onChange={(e) => setFormData({ ...formData, specifications: e.target.value })}
                required
              ></textarea>
            </div>

            <div style={{ padding: '16px', border: '2px dashed #DCE3E8', borderRadius: '8px', textAlign: 'center', background: '#F8FAFC', marginBottom: '24px' }}>
              <Upload size={24} color="#168B80" style={{ margin: '0 auto 6px' }} />
              <div style={{ fontSize: '13px', fontWeight: '700' }}>Attach Signed Purchase Order / RFQ (PDF)</div>
              <div style={{ fontSize: '11.5px', color: '#5e7386' }}>FastAPI OCR will automatically verify line items and delivery specs</div>
            </div>

            <button type="submit" className="btn btn-primary btn-lg" style={{ width: '100%' }} disabled={submitting}>
              {submitting ? 'Transmitting to SHG Cluster...' : 'Submit Institutional Order Request'} <ArrowRight size={18} />
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default BuyerCreateOrderPage;

