import React from 'react';
import { HelpCircle, FileText, Phone, Award, ShieldCheck, ExternalLink } from 'lucide-react';
import { DEMO_KNOWLEDGE_DOCS } from '../../mock/mockData';

const MemberHelpPage = () => {
  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Help, By-Laws & Government Schemes</h1>
          <p className="page-subtitle">
            Information on NRLM Lakhpati Didi benefits, standard operating procedures, and group contact numbers
          </p>
        </div>
      </div>

      <div className="grid grid-cols-12" style={{ gap: '24px' }}>
        <div style={{ gridColumn: 'span 8' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {DEMO_KNOWLEDGE_DOCS.map((doc) => (
              <div key={doc.id} className="card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                  <span className="badge badge-primary">{doc.category}</span>
                  <span style={{ fontSize: '11.5px', color: '#5e7386' }}>{doc.id}</span>
                </div>
                <h3 style={{ fontSize: '16px', color: '#123B5D', marginBottom: '6px' }}>{doc.title}</h3>
                <p style={{ fontSize: '13px', color: '#5e7386', marginBottom: '12px', lineHeight: '1.5' }}>
                  {doc.summary}
                </p>
                <div style={{ background: '#F8FAFC', padding: '12px', borderRadius: '6px', border: '1px solid #EEF2F5', fontSize: '12.5px', color: '#243746', fontStyle: 'italic' }}>
                  <strong>Key Extract:</strong> "{doc.excerpt}"
                </div>
              </div>
            ))}
          </div>
        </div>

        <div style={{ gridColumn: 'span 4' }}>
          <div className="card">
            <h3 style={{ fontSize: '15px', color: '#123B5D', marginBottom: '14px' }}>Emergency & Support Contacts</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '13px' }}>
              <div style={{ padding: '10px', background: '#F8FAFC', borderRadius: '6px', border: '1px solid #EEF2F5' }}>
                <strong>Savitribai Shinde (Leader)</strong>
                <div style={{ color: '#5e7386', fontSize: '12px' }}>Pragati Mahila Sangha</div>
                <div style={{ color: '#168B80', marginTop: '2px', fontWeight: '600' }}>+91 98452 11045</div>
              </div>
              <div style={{ padding: '10px', background: '#F8FAFC', borderRadius: '6px', border: '1px solid #EEF2F5' }}>
                <strong>Deepa Narayan, KAS</strong>
                <div style={{ color: '#5e7386', fontSize: '12px' }}>Cluster Development Officer, NRLM</div>
                <div style={{ color: '#168B80', marginTop: '2px', fontWeight: '600' }}>+91 94481 02941</div>
              </div>
              <div style={{ padding: '10px', background: '#F8FAFC', borderRadius: '6px', border: '1px solid #EEF2F5' }}>
                <strong>Sanjeevini Gramin Helpline</strong>
                <div style={{ color: '#5e7386', fontSize: '12px' }}>Toll Free (Kannada / Hindi / English)</div>
                <div style={{ color: '#168B80', marginTop: '2px', fontWeight: '600' }}>1800-425-9921</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MemberHelpPage;

