import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  ShoppingBag,
  Users,
  GitPullRequest,
  CheckCircle2,
  DollarSign,
  Package,
  Truck,
  Building2,
  Sparkles,
  BarChart3,
  Settings,
  Store,
  Mic,
  HelpCircle,
  Clock,
  Award,
  Wallet,
  FileText,
  Boxes,
  ShieldCheck,
  TrendingUp,
  FileCheck2,
  AlertTriangle
} from 'lucide-react';
import './Sidebar.css';

const roleMenus = {
  leader: [
    { section: 'CORE OPERATIONS', items: [
      { to: '/leader', label: 'Dashboard', icon: LayoutDashboard, end: true },
      { to: '/leader/orders', label: 'Bulk Orders', icon: ShoppingBag },
      { to: '/leader/allocation', label: 'AI Work Allocation', icon: GitPullRequest, highlight: true },
      { to: '/leader/production', label: 'Production Monitor', icon: Clock },
      { to: '/leader/quality', label: 'Quality Control (CV)', icon: CheckCircle2 }
    ]},
    { section: 'BUSINESS & SUPPLY', items: [
      { to: '/leader/pricing', label: 'Smart Pricing & Cost', icon: DollarSign },
      { to: '/leader/inventory', label: 'Inventory & Stock', icon: Package },
      { to: '/leader/suppliers', label: 'Suppliers & Quotes', icon: Building2 },
      { to: '/leader/logistics', label: 'Transport & Logistics', icon: Truck },
      { to: '/leader/retail', label: 'Retail Management', icon: Store }
    ]},
    { section: 'GOVERNANCE & AI', items: [
      { to: '/leader/members', label: 'Members & Capacity', icon: Users },
      { to: '/leader/finance', label: 'Payouts & Transparency', icon: Wallet, highlight: true },
      { to: '/leader/anomalies', label: 'Financial Anomalies', icon: AlertTriangle },
      { to: '/leader/ai', label: 'Agentic AI Insights', icon: Sparkles },
      { to: '/leader/reports', label: 'Reports & Analytics', icon: BarChart3 }
    ]}
  ],
  member: [
    { section: 'MY WORKSPACE', items: [
      { to: '/member', label: 'My Dashboard', icon: LayoutDashboard, end: true },
      { to: '/member/tasks', label: 'My Assigned Tasks', icon: ShoppingBag },
      { to: '/member/production', label: 'Submit Batch Production', icon: Clock },
      { to: '/member/quality', label: 'My Quality Feedback', icon: CheckCircle2 }
    ]},
    { section: 'MY FINANCIALS', items: [
      { to: '/member/earnings', label: 'My Approved Earnings', icon: DollarSign },
      { to: '/member/payments', label: 'Group Payout Voting', icon: Wallet, highlight: true }
    ]},
    { section: 'ASSISTANCE & VOICE', items: [
      { to: '/member/assistant', label: 'Voice & AI Saathi', icon: Mic, highlight: true },
      { to: '/member/help', label: 'Help & NRLM Schemes', icon: HelpCircle }
    ]}
  ],
  buyer: [
    { section: 'BUYER PORTAL', items: [
      { to: '/buyer', label: 'Buyer Dashboard', icon: LayoutDashboard, end: true },
      { to: '/buyer/create', label: 'Submit Bulk Order / PO', icon: FileText, highlight: true },
      { to: '/buyer/orders', label: 'Track Live Production', icon: Clock },
      { to: '/buyer/catalog', label: 'Browse SHG Catalog', icon: Store }
    ]}
  ],
  federation: [
    { section: 'FEDERATION OVERSIGHT', items: [
      { to: '/federation', label: 'Cluster Overview', icon: LayoutDashboard, end: true },
      { to: '/federation/shgs', label: 'SHG Registry & Capacity', icon: Building2 },
      { to: '/federation/production', label: 'Aggregated Orders', icon: Boxes },
      { to: '/federation/reports', label: 'Lakhpati Didi Metrics', icon: TrendingUp }
    ]}
  ]
};

const Sidebar = ({ role }) => {
  const sections = roleMenus[role] || roleMenus.leader;

  return (
    <aside className="portal-sidebar">
      <div className="sidebar-scroll">
        {sections.map((sec, sIdx) => (
          <div key={sIdx} className="sidebar-section">
            <span className="sidebar-section-title">{sec.section}</span>
            <ul className="sidebar-menu-list">
              {sec.items.map((item, iIdx) => {
                const IconComponent = item.icon;
                return (
                  <li key={iIdx} className="sidebar-menu-item">
                    <NavLink
                      to={item.to}
                      end={item.end}
                      className={({ isActive }) =>
                        `sidebar-link ${isActive ? 'active' : ''} ${item.highlight ? 'highlight' : ''}`
                      }
                    >
                      <IconComponent size={18} className="sidebar-link-icon" />
                      <span className="sidebar-link-text">{item.label}</span>
                    </NavLink>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </div>

      <div className="sidebar-footer-card">
        <div className="sidebar-footer-icon">
          <ShieldCheck size={20} className="text-secondary" />
        </div>
        <div className="sidebar-footer-content">
          <span className="footer-title">Verified Trust</span>
          <span className="footer-sub">Group Quorum Protected</span>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
