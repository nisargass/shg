import React, { useState } from 'react';
import {
  CheckCircle2,
  AlertTriangle,
  Eye,
  Camera,
  ShieldCheck,
  Sparkles,
  FileText,
  User,
  Check,
  RotateCcw,
  X
} from 'lucide-react';
import { DEMO_QUALITY_BATCHES } from '../../mock/mockData';
import { qualityApi } from '../../api/services';

const QualityPage = () => {
  const [batches, setBatches] = useState(DEMO_QUALITY_BATCHES);
  const [selectedBatch, setSelectedBatch] = useState(DEMO_QUALITY_BATCHES[1]); // Choose the pending decision one
  const [decisionModalOpen, setDecisionModalOpen] = useState(false);
  const [decisionType, setDecisionType] = useState('APPROVE');
  const [approvedUnits, setApprovedUnits] = useState(selectedBatch.submittedQty);
  const [reworkUnits, setReworkUnits] = useState(0);
  const [remarks, setRemarks] = useState('');
  const [actionNotice, setActionNotice] = useState('');

  const handleOpenDecision = (type) => {
    setDecisionType(type);
    if (type === 'APPROVE') {
      setApprovedUnits(selectedBatch.submittedQty);
      setReworkUnits(0);
    } else if (type === 'REWORK') {
      setApprovedUnits(selectedBatch.submittedQty - 6);
      setReworkUnits(6);
      setRemarks('Zipper alignment exceeds 3mm tolerance. Please restitch before carton loading.');
    } else {
      setApprovedUnits(0);
      setReworkUnits(selectedBatch.submittedQty);
    }
    setDecisionModalOpen(true);
  };

  const handleRecordDecision = async (e) => {
    e.preventDefault();
    const result = await qualityApi.submitHumanDecision(selectedBatch.batchId, {
      status: decisionType === 'APPROVE' ? 'APPROVED' : decisionType === 'REWORK' ? 'REWORK_REQUESTED' : 'REJECTED',
      approvedQty: Number(approvedUnits),
      reworkQty: Number(reworkUnits),
      remarks
    });

    const updated = batches.map((b) => {
      if (b.batchId === selectedBatch.batchId) {
        return {
          ...b,
          humanReview: {
            status: decisionType === 'APPROVE' ? 'APPROVED' : 'REWORK_REQUESTED',
            reviewedBy: 'Savitribai Shinde (Leader)',
            approvedQty: Number(approvedUnits),
            reworkQty: Number(reworkUnits),
            reviewDate: new Date().toISOString().split('T')[0],
            leaderRemarks: remarks || 'Human review completed and logged.'
          }
        };
      }
      return b;
    });

    setBatches(updated);
    setSelectedBatch(updated.find((b) => b.batchId === selectedBatch.batchId));
    setDecisionModalOpen(false);
    setActionNotice(`Final human decision recorded for Batch ${selectedBatch.batchId}. Member notified.`);
    setTimeout(() => setActionNotice(''), 5000);
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">AI-Assisted Quality Inspection (Computer Vision)</h1>
          <p className="page-subtitle">
            Visual defect pre-screening with mandatory Human-In-The-Loop inspection approval
          </p>
        </div>
        <div className="page-actions">
          <span className="badge badge-secondary" style={{ padding: '6px 12px' }}>
            <Sparkles size={14} /> AI Pre-screener Active (YOLO / Vision Model)
          </span>
        </div>
      </div>

      {actionNotice && (
        <div className="alert-banner success" style={{ marginBottom: '20px' }}>
          <CheckCircle2 size={20} />
          <span>{actionNotice}</span>
        </div>
      )}

      {/* Human In The Loop Principle Banner */}
      <div className="alert-banner info" style={{ marginBottom: '24px' }}>
        <ShieldCheck size={20} />
        <div>
          <strong>Human Review Policy: AI Findings are Informative Only</strong>
          <p style={{ margin: '2px 0 0', fontSize: '13px' }}>
            AI vision detects pattern, seam tension and dimension flaws. The SHG Leader or designated master craftswoman must examine the physical piece or photographs and make the authoritative acceptance decision.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-12" style={{ gap: '24px' }}>
        {/* Left Column: Batches List */}
        <div style={{ gridColumn: 'span 4' }}>
          <div className="card" style={{ padding: 0 }}>
            <div style={{ padding: '16px', borderBottom: '1px solid #EEF2F5' }}>
              <h3 style={{ fontSize: '14px', color: '#123B5D' }}>Submitted Production Batches</h3>
            </div>
            <div style={{ maxHeight: '640px', overflowY: 'auto' }}>
              {batches.map((batch) => {
                const isSelected = selectedBatch.batchId === batch.batchId;
                const isDecided = batch.humanReview.status !== 'PENDING_DECISION';
                return (
                  <div
                    key={batch.batchId}
                    onClick={() => setSelectedBatch(batch)}
                    style={{
                      padding: '16px',
                      borderBottom: '1px solid #EEF2F5',
                      cursor: 'pointer',
                      background: isSelected ? '#f1f8f7' : '#FFFFFF',
                      borderLeft: isSelected ? '4px solid #168B80' : '4px solid transparent'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                      <strong style={{ fontSize: '13px', color: '#123B5D' }}>{batch.batchId}</strong>
                      <span className={`badge ${isDecided ? 'badge-success' : 'badge-alert'}`}>
                        {batch.humanReview.status.replace('_', ' ')}
                      </span>
                    </div>
                    <div style={{ fontSize: '13px', fontWeight: '600', color: '#243746' }}>
                      {batch.productName}
                    </div>
                    <div style={{ fontSize: '12px', color: '#5e7386', marginTop: '2px' }}>
                      Artisan: <strong>{batch.memberName}</strong> &bull; Qty: <strong>{batch.submittedQty}</strong>
                    </div>
                    <div style={{ fontSize: '11.5px', color: '#899ba8', marginTop: '4px' }}>
                      Submitted: {batch.submissionDate}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Right Column: AI Analysis & Human Decision Controls */}
        <div style={{ gridColumn: 'span 8' }}>
          <div className="card">
            {/* Batch Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', paddingBottom: '16px', borderBottom: '1px solid #EEF2F5' }}>
              <div>
                <span className="badge badge-primary">{selectedBatch.batchId}</span>
                <h2 style={{ fontSize: '19px', color: '#123B5D', marginTop: '6px' }}>
                  {selectedBatch.productName} (Submitted: {selectedBatch.submittedQty} units)
                </h2>
                <div style={{ fontSize: '13px', color: '#5e7386', marginTop: '2px' }}>
                  Submitted by Artisan: <strong>{selectedBatch.memberName}</strong> &bull; Order: {selectedBatch.orderId}
                </div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <span style={{ fontSize: '11px', color: '#5e7386', textTransform: 'uppercase', fontWeight: '600' }}>Inspection Status</span>
                <div>
                  <span className={`badge ${selectedBatch.humanReview.status === 'PENDING_DECISION' ? 'badge-alert' : 'badge-success'}`} style={{ fontSize: '13px', padding: '6px 12px' }}>
                    {selectedBatch.humanReview.status.replace('_', ' ')}
                  </span>
                </div>
              </div>
            </div>

            {/* Photo & Defect Bounding Boxes */}
            <div style={{ margin: '20px 0' }}>
              <div style={{ position: 'relative', borderRadius: '10px', overflow: 'hidden', border: '1px solid #DCE3E8', background: '#000', maxHeight: '340px' }}>
                <img
                  src={selectedBatch.photoUrl}
                  alt="Batch Inspection Item"
                  style={{ width: '100%', height: '100%', objectFit: 'cover', opacity: 0.92 }}
                />
                {/* Simulated Computer Vision Overlays */}
                <div style={{
                  position: 'absolute',
                  top: '25%',
                  left: '30%',
                  width: '140px',
                  height: '70px',
                  border: '2px solid #E6A23C',
                  backgroundColor: 'rgba(230, 162, 60, 0.2)',
                  borderRadius: '4px',
                  pointerEvents: 'none'
                }}>
                  <span style={{
                    position: 'absolute',
                    top: '-20px',
                    left: '0',
                    background: '#E6A23C',
                    color: '#000',
                    fontSize: '10.5px',
                    fontWeight: '700',
                    padding: '2px 6px',
                    borderRadius: '2px'
                  }}>
                    Zipper Alignment ({selectedBatch.aiInspection.overallConfidence}%)
                  </span>
                </div>
              </div>
            </div>

            {/* AI Vision Observations Breakdown */}
            <div style={{ background: '#F8FAFC', border: '1px solid #DCE3E8', borderRadius: '8px', padding: '18px', marginBottom: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Sparkles size={18} color="#168B80" />
                  <strong style={{ fontSize: '14px', color: '#123B5D' }}>AI Computer Vision Diagnostic</strong>
                </div>
                <span className="badge badge-secondary">
                  Confidence Score: {selectedBatch.aiInspection.overallConfidence}%
                </span>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '14px' }}>
                {selectedBatch.aiInspection.detectedIssues.map((issue, idx) => (
                  <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 12px', background: '#FFFFFF', borderRadius: '6px', border: '1px solid #EEF2F5', fontSize: '13px' }}>
                    <div>
                      <strong>{issue.type}</strong>: <span style={{ color: '#5e7386' }}>{issue.detail}</span>
                    </div>
                    <span className={`badge ${issue.severity === 'MEDIUM' ? 'badge-accent' : issue.severity === 'LOW' ? 'badge-neutral' : 'badge-success'}`}>
                      {issue.severity} RISK
                    </span>
                  </div>
                ))}
              </div>

              <div style={{ padding: '12px', background: '#e6f6f4', borderRadius: '6px', border: '1px solid #c2ece7', fontSize: '13px', color: '#123B5D' }}>
                <strong>AI Model Recommendation: </strong>
                {selectedBatch.aiInspection.aiRecommendation}
              </div>
            </div>

            {/* Human Decision Review Section */}
            <div style={{ borderTop: '1px solid #EEF2F5', paddingTop: '16px' }}>
              <h3 style={{ fontSize: '14px', color: '#123B5D', marginBottom: '8px' }}>
                Authoritative Human Decision Panel
              </h3>

              {selectedBatch.humanReview.reviewedBy ? (
                <div style={{ padding: '14px', background: '#e8f5e9', borderRadius: '8px', border: '1px solid #c8e6c9', fontSize: '13px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                    <strong>Reviewed By: {selectedBatch.humanReview.reviewedBy}</strong>
                    <span>Date: {selectedBatch.humanReview.reviewDate}</span>
                  </div>
                  <div>Approved: <strong>{selectedBatch.humanReview.approvedQty} units</strong> &bull; Rework: <strong>{selectedBatch.humanReview.reworkQty} units</strong></div>
                  <div style={{ marginTop: '6px', fontStyle: 'italic', color: '#2e7d32' }}>
                    "{selectedBatch.humanReview.leaderRemarks}"
                  </div>
                </div>
              ) : (
                <div style={{ display: 'flex', gap: '12px' }}>
                  <button className="btn btn-secondary" onClick={() => handleOpenDecision('APPROVE')}>
                    <Check size={16} /> Approve Full Batch (35 units)
                  </button>
                  <button className="btn btn-accent" onClick={() => handleOpenDecision('REWORK')}>
                    <RotateCcw size={16} /> Request Minor Rework (6 units)
                  </button>
                  <button className="btn btn-danger" onClick={() => handleOpenDecision('REJECT')}>
                    <X size={16} /> Reject Batch
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Modal: Human Decision Entry */}
      {decisionModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3 style={{ fontSize: '17px', color: '#123B5D' }}>Record Human Inspection Decision</h3>
              <button onClick={() => setDecisionModalOpen(false)} style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer' }}>&times;</button>
            </div>
            <form onSubmit={handleRecordDecision}>
              <div className="modal-body">
                <div className="alert-banner info" style={{ marginBottom: '16px' }}>
                  <ShieldCheck size={18} />
                  <span>Your decision directly updates member piece-rate earnings and carton packing availability.</span>
                </div>

                <div className="grid grid-cols-2" style={{ gap: '14px' }}>
                  <div className="form-group">
                    <label className="form-label">Approved Quantity</label>
                    <input
                      type="number"
                      className="form-control"
                      value={approvedUnits}
                      onChange={(e) => setApprovedUnits(e.target.value)}
                      max={selectedBatch.submittedQty}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Rework Quantity</label>
                    <input
                      type="number"
                      className="form-control"
                      value={reworkUnits}
                      onChange={(e) => setReworkUnits(e.target.value)}
                      max={selectedBatch.submittedQty}
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">Inspector / Leader Remarks for Artisan</label>
                  <textarea
                    className="form-control"
                    rows="3"
                    value={remarks}
                    onChange={(e) => setRemarks(e.target.value)}
                    placeholder="Provide constructive feedback (e.g., thread tension adjustment, zipper re-pinning)..."
                    required
                  ></textarea>
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-outline" onClick={() => setDecisionModalOpen(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary">Publish Decision to Member Ledger</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default QualityPage;

