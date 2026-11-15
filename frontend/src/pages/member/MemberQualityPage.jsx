import React from 'react';
import {
  CheckCircle2,
  AlertTriangle,
  Sparkles,
  Eye,
  Camera,
  ShieldCheck,
  RotateCcw
} from 'lucide-react';
import { DEMO_QUALITY_BATCHES } from '../../mock/mockData';

const MemberQualityPage = () => {
  // Filter batches submitted by Sunita Rathod (mem_01)
  const myBatch = DEMO_QUALITY_BATCHES[0];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">My Quality Inspection Feedback</h1>
          <p className="page-subtitle">
            Constructive AI pre-screening and Leader evaluation results for your submitted batches
          </p>
        </div>
      </div>

      <div className="card" style={{ maxWidth: '800px', margin: '0 auto', padding: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '12px', paddingBottom: '16px', borderBottom: '1px solid #EEF2F5' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span className="badge badge-primary">{myBatch.batchId}</span>
              <span className="badge badge-secondary">{myBatch.orderId}</span>
            </div>
            <h2 style={{ fontSize: '18px', color: '#123B5D', marginTop: '6px' }}>
              {myBatch.productName} ({myBatch.submittedQty} units submitted)
            </h2>
            <div style={{ fontSize: '12.5px', color: '#5e7386' }}>Submitted on {myBatch.submissionDate}</div>
          </div>

          <div>
            <span className="badge badge-success" style={{ fontSize: '13px', padding: '6px 12px' }}>
              <CheckCircle2 size={15} /> 48 Units Approved (2 Reworked & Accepted)
            </span>
          </div>
        </div>

        {/* Photo view */}
        <div style={{ margin: '20px 0', borderRadius: '8px', overflow: 'hidden', border: '1px solid #DCE3E8', maxHeight: '280px' }}>
          <img src={myBatch.photoUrl} alt="Inspection Sample" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </div>

        {/* AI & Leader Feedback Box */}
        <div style={{ background: '#F8FAFC', padding: '16px', borderRadius: '8px', border: '1px solid #EEF2F5', marginBottom: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#168B80', marginBottom: '8px' }}>
            <Sparkles size={18} />
            <strong style={{ fontSize: '13.5px' }}>AI Pre-Screening Findings (Confidence: {myBatch.aiInspection.overallConfidence}%)</strong>
          </div>
          <p style={{ fontSize: '13px', color: '#243746', margin: '0 0 10px' }}>
            {myBatch.aiInspection.aiRecommendation}
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            {myBatch.aiInspection.detectedIssues.map((issue, idx) => (
              <div key={idx} style={{ fontSize: '12.5px', color: '#5e7386', padding: '6px 10px', background: '#FFFFFF', borderRadius: '4px', border: '1px solid #EEF2F5' }}>
                <strong>{issue.type}:</strong> {issue.detail}
              </div>
            ))}
          </div>
        </div>

        {/* Human Leader Sign-off Note */}
        <div style={{ background: '#e8f5e9', border: '1px solid #c8e6c9', padding: '16px', borderRadius: '8px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
            <strong style={{ fontSize: '13.5px', color: '#2e7d32' }}>
              Leader Remarks: {myBatch.humanReview.reviewedBy}
            </strong>
            <span style={{ fontSize: '11.5px', color: '#5e7386' }}>{myBatch.humanReview.reviewDate}</span>
          </div>
          <p style={{ fontSize: '13px', color: '#1b5e20', margin: 0, fontStyle: 'italic' }}>
            "{myBatch.humanReview.leaderRemarks}"
          </p>
        </div>
      </div>
    </div>
  );
};

export default MemberQualityPage;

