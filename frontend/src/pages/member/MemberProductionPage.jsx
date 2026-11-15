import React, { useState } from 'react';
import {
  Camera,
  CheckCircle2,
  Plus,
  Minus,
  Upload,
  ArrowRight,
  ShieldCheck,
  Sparkles
} from 'lucide-react';

const MemberProductionPage = () => {
  const [unitsToSubmit, setUnitsToSubmit] = useState(15);
  const [photoPreview, setPhotoPreview] = useState('https://images.unsplash.com/photo-1597484661643-2f5fef640dd1?auto=format&fit=crop&q=80&w=400');
  const [submitting, setSubmitting] = useState(false);
  const [submittedSuccess, setSubmittedSuccess] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitting(true);
    setTimeout(() => {
      setSubmitting(false);
      setSubmittedSuccess(true);
    }, 1000);
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Submit Completed Batch</h1>
          <p className="page-subtitle">
            Record the pieces you stitched today and upload photos for AI pre-inspection
          </p>
        </div>
      </div>

      {submittedSuccess && (
        <div className="alert-banner success" style={{ marginBottom: '24px' }}>
          <CheckCircle2 size={24} style={{ flexShrink: 0 }} />
          <div>
            <strong style={{ fontSize: '15px' }}>Batch Successfully Submitted!</strong>
            <p style={{ margin: '4px 0 0', fontSize: '13px' }}>
              Your {unitsToSubmit} units have been queued for Computer Vision pre-check and Leader verification. Your earnings ledger will credit ₹{(unitsToSubmit * 32).toLocaleString()} once approved.
            </p>
          </div>
        </div>
      )}

      <div className="card" style={{ maxWidth: '640px', margin: '0 auto', padding: '28px' }}>
        <form onSubmit={handleSubmit}>
          {/* Active Order Context */}
          <div style={{ background: '#F8FAFC', padding: '16px', borderRadius: '10px', border: '1px solid #EEF2F5', marginBottom: '24px' }}>
            <span className="badge badge-primary">ORD-2026-104</span>
            <h3 style={{ fontSize: '16px', color: '#123B5D', marginTop: '4px' }}>
              Organic Cotton Tote Bags (Heavy 280 GSM)
            </h3>
            <div style={{ fontSize: '13px', color: '#168B80', marginTop: '2px', fontWeight: '600' }}>
              Piece-rate compensation: ₹32.00 per approved bag
            </div>
          </div>

          {/* Large Accessible Counter */}
          <div style={{ marginBottom: '28px', textAlign: 'center' }}>
            <label className="form-label" style={{ fontSize: '15px', marginBottom: '12px' }}>
              How many finished bags did you complete today?
            </label>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '20px' }}>
              <button
                type="button"
                className="btn btn-outline"
                style={{ width: '56px', height: '56px', borderRadius: '50%', fontSize: '24px' }}
                onClick={() => setUnitsToSubmit(Math.max(1, unitsToSubmit - 5))}
              >
                <Minus size={24} />
              </button>

              <div style={{
                width: '120px',
                height: '70px',
                borderRadius: '12px',
                background: '#e6f6f4',
                border: '2px solid #168B80',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '36px',
                fontWeight: '800',
                color: '#123B5D'
              }}>
                {unitsToSubmit}
              </div>

              <button
                type="button"
                className="btn btn-outline"
                style={{ width: '56px', height: '56px', borderRadius: '50%', fontSize: '24px' }}
                onClick={() => setUnitsToSubmit(unitsToSubmit + 5)}
              >
                <Plus size={24} />
              </button>
            </div>
            <div style={{ marginTop: '10px', fontSize: '13px', color: '#5e7386' }}>
              Estimated batch earnings: <strong>₹{(unitsToSubmit * 32).toLocaleString()}</strong>
            </div>
          </div>

          {/* Photo Capture / Upload */}
          <div style={{ marginBottom: '28px' }}>
            <label className="form-label" style={{ fontSize: '14px', marginBottom: '8px' }}>
              Take or Attach Product Photograph (for Quality Inspection)
            </label>
            <div style={{ border: '2px dashed #168B80', borderRadius: '12px', padding: '20px', textAlign: 'center', background: '#fdfaf4' }}>
              {photoPreview ? (
                <div>
                  <img
                    src={photoPreview}
                    alt="Batch sample"
                    style={{ width: '100%', maxHeight: '200px', objectFit: 'cover', borderRadius: '8px', marginBottom: '12px' }}
                  />
                  <div style={{ display: 'flex', justifyContent: 'center', gap: '10px' }}>
                    <button type="button" className="btn btn-sm btn-outline" onClick={() => alert('Camera activated on mobile device.')}>
                      <Camera size={16} /> Retake Photo
                    </button>
                  </div>
                </div>
              ) : (
                <div>
                  <Camera size={36} color="#168B80" style={{ margin: '0 auto 8px' }} />
                  <div style={{ fontSize: '13.5px', fontWeight: '700', color: '#123B5D' }}>
                    Tap to open camera or upload image
                  </div>
                  <div style={{ fontSize: '12px', color: '#5e7386', marginTop: '2px' }}>
                    Ensure handle stitching and zipper seams are clearly visible
                  </div>
                </div>
              )}
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-secondary btn-lg"
            style={{ width: '100%', padding: '14px', fontSize: '16px' }}
            disabled={submitting}
          >
            {submitting ? 'Submitting & Scanning...' : `Submit ${unitsToSubmit} Bags for Verification`}
            <ArrowRight size={18} />
          </button>
        </form>
      </div>
    </div>
  );
};

export default MemberProductionPage;

