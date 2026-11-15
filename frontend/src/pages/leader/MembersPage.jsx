import React, { useState } from 'react';
import {
  Users,
  Award,
  Clock,
  Phone,
  MapPin,
  CheckCircle2,
  TrendingUp,
  Plus,
  ShieldCheck
} from 'lucide-react';
import { DEMO_MEMBERS } from '../../mock/mockData';

const MembersPage = () => {
  const [members] = useState(DEMO_MEMBERS);

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">SHG Member Roster & Capacity Profiles</h1>
          <p className="page-subtitle">
            Artisan skill matrices, working hours availability, speed ratings, and verified quality scores
          </p>
        </div>
        <div className="page-actions">
          <button className="btn btn-primary" onClick={() => alert('Member enrollment form initialized.')}>
            <Plus size={16} /> Register New Member
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2" style={{ gap: '20px' }}>
        {members.map((mem) => (
          <div key={mem.id} className="card" style={{ padding: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '14px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div style={{ width: '44px', height: '44px', borderRadius: '50%', background: '#e6f6f4', color: '#168B80', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: '800', fontSize: '18px' }}>
                  {mem.name.charAt(0)}
                </div>
                <div>
                  <h3 style={{ fontSize: '16px', color: '#123B5D' }}>{mem.name}</h3>
                  <div style={{ fontSize: '12px', color: '#5e7386' }}>
                    ID: {mem.id} &bull; Village: {mem.village}
                  </div>
                </div>
              </div>
              <span className="badge badge-secondary">{mem.skillLevel}</span>
            </div>

            <div style={{ marginBottom: '14px' }}>
              <span style={{ fontSize: '11px', color: '#5e7386', textTransform: 'uppercase', fontWeight: '600' }}>Craft Specializations:</span>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginTop: '6px' }}>
                {mem.skills.map((s, sIdx) => (
                  <span key={sIdx} className="badge badge-neutral" style={{ fontSize: '11.5px' }}>
                    {s}
                  </span>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-3" style={{ background: '#F8FAFC', padding: '12px', borderRadius: '8px', border: '1px solid #EEF2F5', fontSize: '12px', textAlign: 'center', gap: '8px', marginBottom: '14px' }}>
              <div>
                <span style={{ color: '#5e7386', display: 'block', fontSize: '11px' }}>Daily Hours:</span>
                <strong style={{ fontSize: '14px', color: '#123B5D' }}>{mem.availableHoursPerDay} hrs</strong>
              </div>
              <div>
                <span style={{ color: '#5e7386', display: 'block', fontSize: '11px' }}>Speed Rate:</span>
                <strong style={{ fontSize: '14px', color: '#168B80' }}>{mem.speedUnitsPerHour} / hr</strong>
              </div>
              <div>
                <span style={{ color: '#5e7386', display: 'block', fontSize: '11px' }}>On-Time Rate:</span>
                <strong style={{ fontSize: '14px', color: '#168B80' }}>{mem.historicalOnTimeRate}%</strong>
              </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '12px', color: '#5e7386' }}>
              <span>Bank A/C: <strong>{mem.accountNumber}</strong></span>
              <span>Phone: <strong>{mem.phone}</strong></span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MembersPage;

