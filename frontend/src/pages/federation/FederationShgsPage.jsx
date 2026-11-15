import React from 'react';
import { Building2, Users, MapPin, Award } from 'lucide-react';

const FederationShgsPage = () => {
  const shgs = [
    { name: 'Pragati Mahila Sangha', village: 'Channapatna', members: 8, lead: 'Savitribai Shinde', specialization: 'Heavy Cotton Bags & Textiles', activeContracts: 3 },
    { name: 'Sannidhi Farmers Mahila Group', village: 'Kailancha', members: 12, lead: 'Shobha Manjunath', specialization: 'Organic Spices & Food Processing', activeContracts: 2 },
    { name: 'Kala Chaitanya SHG', village: 'Ijoor', members: 10, lead: 'Anusuya Bai', specialization: 'GI Channapatna Lacquerware Toys', activeContracts: 2 },
    { name: 'Cauvery Mahila Sangha', village: 'Bidadi', members: 9, lead: 'Meenakshi K.', specialization: 'Natural Fibre Jute Crafts', activeContracts: 2 }
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Cluster SHG Directory & Capacity Register</h1>
          <p className="page-subtitle">Ramanagara District &bull; National Rural Livelihoods Mission</p>
        </div>
      </div>

      <div className="grid grid-cols-2" style={{ gap: '20px' }}>
        {shgs.map((s, idx) => (
          <div key={idx} className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
              <div>
                <h3 style={{ fontSize: '16px', color: '#123B5D' }}>{s.name}</h3>
                <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '12px', color: '#5e7386', marginTop: '2px' }}>
                  <MapPin size={13} /> {s.village} Village
                </div>
              </div>
              <span className="badge badge-secondary">{s.members} Artisans</span>
            </div>

            <div style={{ background: '#F8FAFC', padding: '12px', borderRadius: '8px', border: '1px solid #EEF2F5', fontSize: '12.5px', marginBottom: '12px' }}>
              <div>Leader: <strong>{s.lead}</strong></div>
              <div>Craft Specialization: <strong>{s.specialization}</strong></div>
              <div>Active Bulk Contracts: <strong>{s.activeContracts} Orders</strong></div>
            </div>

            <button className="btn btn-sm btn-outline" style={{ width: '100%' }} onClick={() => alert(`Opening comprehensive audit file for ${s.name}...`)}>
              View NRLM Audit Dossier
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FederationShgsPage;

