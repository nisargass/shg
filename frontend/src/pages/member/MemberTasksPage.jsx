import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  ShoppingBag,
  Clock,
  CheckCircle2,
  Calendar,
  Camera,
  ArrowRight,
  TrendingUp,
  Brain
} from 'lucide-react';

const MemberTasksPage = () => {
  const [tasks] = useState([
    {
      taskId: 'TSK-104-01',
      orderId: 'ORD-2026-104',
      productName: 'Organic Cotton Tote Bags (Heavy 280 GSM)',
      roleTask: 'Main Body Stitching & Handle Assembly',
      assignedQty: 220,
      completedQty: 180,
      approvedQty: 180,
      feasibleQty: 230,
      deadline: '2026-11-20',
      daysLeft: 13,
      pieceRate: 32.0,
      status: 'IN_PROGRESS',
      completionLikelihood: 94
    }
  ]);

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">My Assigned Bulk Tasks</h1>
          <p className="page-subtitle">
            Track your piece-rate work orders, deadlines, and daily quotas
          </p>
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {tasks.map((task) => {
          const percent = Math.round((task.completedQty / task.assignedQty) * 100);
          return (
            <div key={task.taskId} className="card" style={{ padding: '24px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '14px', marginBottom: '14px' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span className="badge badge-primary">{task.taskId}</span>
                    <span className="badge badge-secondary">{task.orderId}</span>
                    <span className="badge badge-success">{task.status}</span>
                  </div>
                  <h3 style={{ fontSize: '18px', color: '#123B5D', marginTop: '6px' }}>
                    {task.productName}
                  </h3>
                  <div style={{ fontSize: '13px', color: '#5e7386' }}>
                    Process: <strong>{task.roleTask}</strong> &bull; Compensation: <strong>₹{task.pieceRate} / bag</strong>
                  </div>
                </div>

                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '24px', fontWeight: '800', color: '#168B80' }}>
                    {task.completedQty} / {task.assignedQty}
                  </div>
                  <div style={{ fontSize: '12px', color: '#5e7386' }}>Units Finished</div>
                </div>
              </div>

              {/* Progress bar */}
              <div style={{ marginBottom: '16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12.5px', marginBottom: '4px' }}>
                  <span>Actual Verified Progress</span>
                  <strong>{percent}% completed</strong>
                </div>
                <div className="progress-bar" style={{ height: '10px' }}>
                  <div className="progress-fill" style={{ width: `${percent}%` }}></div>
                </div>
              </div>

              {/* Metrics Box */}
              <div className="grid grid-cols-3" style={{ background: '#F8FAFC', padding: '14px', borderRadius: '8px', border: '1px solid #EEF2F5', fontSize: '12.5px', gap: '12px', marginBottom: '16px' }}>
                <div>
                  <span style={{ color: '#5e7386', display: 'block' }}>Delivery Deadline:</span>
                  <strong style={{ fontSize: '14px', color: '#123B5D' }}>{task.deadline}</strong> ({task.daysLeft} days)
                </div>
                <div>
                  <span style={{ color: '#5e7386', display: 'block' }}>AI Predicted Finish:</span>
                  <strong style={{ fontSize: '14px', color: '#168B80' }}>Nov 09, 2026</strong> (On-time)
                </div>
                <div>
                  <span style={{ color: '#5e7386', display: 'block' }}>Likelihood Score:</span>
                  <strong style={{ fontSize: '14px', color: '#168B80' }}>{task.completionLikelihood}% Feasible</strong>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '12px' }}>
                <Link to="/member/production" className="btn btn-secondary">
                  <Camera size={16} /> Submit Finished Units for Quality Check
                </Link>
                <Link to="/member/quality" className="btn btn-outline">
                  View Inspection Feedback
                </Link>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default MemberTasksPage;

