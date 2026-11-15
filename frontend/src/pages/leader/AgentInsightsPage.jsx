import React from 'react';
import {
  Sparkles,
  Brain,
  Calendar,
  Users,
  Activity,
  CheckCircle,
  TrendingUp,
  ShieldAlert,
  ShoppingBag,
  Truck,
  Mic,
  ArrowRight,
  ShieldCheck
} from 'lucide-react';
import { DEMO_AGENT_ACTIVITIES } from '../../mock/mockData';

const AgentInsightsPage = () => {
  return (
    <div>
      <div className="page-header">
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h1 className="page-title">Agentic AI Activity Center & Orchestration</h1>
            <span className="demo-badge">10 Multi-Agent Ensemble</span>
          </div>
          <p className="page-subtitle">
            Autonomous coordination feed powered by LangGraph & FastAPI &bull; Human-In-The-Loop safety protocol
          </p>
        </div>
      </div>

      {/* Architecture Disclaimer */}
      <div className="alert-banner info" style={{ marginBottom: '24px' }}>
        <ShieldCheck size={20} />
        <div>
          <strong>Responsible Governance: Human Authority Precedes Autonomous Execution</strong>
          <p style={{ margin: '2px 0 0', fontSize: '13px' }}>
            AI agents perform computation, pattern detection, and draft recommendations. Official contract commitments, member assignments, and money payouts strictly require designated human leader approvals.
          </p>
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {DEMO_AGENT_ACTIVITIES.map((act) => {
          const isActionNeeded = act.requiresHumanAction;
          return (
            <div
              key={act.id}
              className="card"
              style={{
                padding: '20px',
                borderLeft: isActionNeeded ? '4px solid #E6A23C' : '4px solid #168B80'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '12px', marginBottom: '8px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <div style={{ width: '40px', height: '40px', borderRadius: '10px', background: isActionNeeded ? '#fef4e8' : '#e6f6f4', color: isActionNeeded ? '#E6A23C' : '#168B80', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Sparkles size={20} />
                  </div>
                  <div>
                    <h3 style={{ fontSize: '16px', color: '#123B5D' }}>{act.agentName}</h3>
                    <div style={{ fontSize: '12px', color: '#5e7386' }}>
                      Task: <strong>{act.task}</strong> &bull; {act.timestamp}
                    </div>
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span className="badge badge-neutral">Confidence: {act.confidence}</span>
                  <span className={`badge ${act.status === 'COMPLETED' ? 'badge-success' : act.status === 'ACTION_REQUIRED' ? 'badge-alert' : 'badge-accent'}`}>
                    {act.status.replace(/_/g, ' ')}
                  </span>
                </div>
              </div>

              <div style={{ background: '#F8FAFC', padding: '14px', borderRadius: '8px', border: '1px solid #EEF2F5', marginTop: '10px', fontSize: '13px', lineHeight: '1.5' }}>
                <strong style={{ color: '#123B5D' }}>Recommendation & Analysis:</strong>
                <p style={{ margin: '4px 0 0', color: '#243746' }}>{act.recommendation}</p>
              </div>

              {isActionNeeded && (
                <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '12px' }}>
                  <button className="btn btn-sm btn-accent" style={{ color: '#FFFFFF' }} onClick={() => alert(`Opening context workflow for ${act.task}`)}>
                    {act.actionLabel || 'Review & Decide'} <ArrowRight size={14} />
                  </button>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default AgentInsightsPage;

