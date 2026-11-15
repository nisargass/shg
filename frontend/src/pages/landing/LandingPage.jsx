import React from 'react';
import { Link } from 'react-router-dom';
import {
  Sparkles,
  ArrowRight,
  CheckCircle,
  AlertCircle,
  Users,
  ShoppingBag,
  TrendingUp,
  ShieldCheck,
  Brain,
  Truck,
  Eye,
  DollarSign,
  Layers,
  Award,
  ChevronRight,
  Store
} from 'lucide-react';
import { DEMO_RETAIL_PRODUCTS } from '../../mock/mockData';
import './LandingPage.css';

const LandingPage = () => {
  return (
    <div className="landing-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-container">
          <div className="hero-content">
            <div className="hero-pill">
              <Sparkles size={16} />
              <span>National Rural Livelihood Mission Compatible</span>
            </div>
            <h1 className="hero-title">
              Empowering Women. Simplifying Work. <span className="text-secondary">Building Stronger SHGs.</span>
            </h1>
            <p className="hero-subtitle">
              Transforming Self-Help Groups into reliable, profitable suppliers through Agentic AI. Intelligently coordinate bulk orders, predict member completion, enforce fair piece-rate earnings, and eliminate manual accounting mistrust.
            </p>
            <div className="hero-actions">
              <Link to="/leader" className="btn btn-primary btn-lg">
                Enter Leader Portal <ArrowRight size={18} />
              </Link>
              <Link to="/member" className="btn btn-secondary btn-lg">
                Member Portal (Voice)
              </Link>
              <Link to="/buyer" className="btn btn-outline btn-lg" style={{ color: '#FFFFFF', borderColor: 'rgba(255,255,255,0.4)' }}>
                Wholesale Buyer
              </Link>
            </div>

            <div className="hero-stats-banner">
              <div className="hero-stat-item">
                <span className="hero-stat-num">100%</span>
                <span className="hero-stat-desc">Fair Work & Payout Transparency</span>
              </div>
              <div className="hero-stat-item">
                <span className="hero-stat-num">96.4%</span>
                <span className="hero-stat-desc">On-Time Bulk Order Fulfilment</span>
              </div>
              <div className="hero-stat-item">
                <span className="hero-stat-num">10 Agents</span>
                <span className="hero-stat-desc">Autonomous Coordination Suite</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* The Core Problem */}
      <section className="landing-section bg-white">
        <div className="section-container">
          <div className="section-header">
            <span className="section-kicker">THE GROUND REALITY</span>
            <h2 className="section-title">Why Fulfilling Bulk Orders Breaks Down in Rural SHGs</h2>
            <p className="section-desc">
              When a Self-Help Group gets a bulk order for 1,500 tote bags or 500 jars of spice, manual processes create failure points.
            </p>
          </div>

          <div className="grid grid-cols-3">
            <div className="problem-card">
              <div className="problem-icon"><AlertCircle size={24} /></div>
              <h3>Verbal & Unequal Work Allocation</h3>
              <p>Work is assigned verbally without knowing individual daily capacity, leading to severe bottlenecks while other members sit idle.</p>
            </div>
            <div className="problem-card">
              <div className="problem-icon"><AlertCircle size={24} /></div>
              <h3>Late Quality Checks & Rejections</h3>
              <p>Defects are discovered only on submission day after 500 bags are stitched, causing missed buyer deadlines and financial loss.</p>
            </div>
            <div className="problem-card">
              <div className="problem-icon"><AlertCircle size={24} /></div>
              <h3>Underpricing & Erroneous Costing</h3>
              <p>Groups routinely forget transport, thread waste, and machine maintenance, unwittingly selling products below true production cost.</p>
            </div>
            <div className="problem-card">
              <div className="problem-icon"><AlertCircle size={24} /></div>
              <h3>Manual Accounting & Mistrust</h3>
              <p>Handwritten registers lead to disputed piece-rate counts and friction between members and group leaders during payout distribution.</p>
            </div>
            <div className="problem-card">
              <div className="problem-icon"><AlertCircle size={24} /></div>
              <h3>Inventory Double-Selling</h3>
              <p>Stock physically sitting in the workshop is mistakenly sold to local retail while simultaneously promised to a wholesale buyer.</p>
            </div>
            <div className="problem-card">
              <div className="problem-icon"><AlertCircle size={24} /></div>
              <h3>Disorganized Transport & High Freight</h3>
              <p>Without coordinated batch consolidation, small parcel dispatches eat up to 25% of the group's hard-earned margin.</p>
            </div>
          </div>
        </div>
      </section>

      {/* The Solution Architecture */}
      <section className="landing-section">
        <div className="section-container">
          <div className="section-header">
            <span className="section-kicker">THE SHG SAATHI WORKFLOW</span>
            <h2 className="section-title">An End-to-End Autonomous Pipeline for Bulk Fulfilment</h2>
            <p className="section-desc">
              From purchase order OCR ingestion to member-approved bank payouts, every step is coordinated with verifiable human-in-the-loop governance.
            </p>
          </div>

          <div className="workflow-diagram">
            <div className="workflow-step">
              <div className="step-number">1</div>
              <h4>Buyer PO Ingestion</h4>
              <p>FastAPI parses PDF purchase orders and extracts quantities, delivery dates, and technical specifications.</p>
            </div>
            <div className="workflow-arrow"><ChevronRight size={24} /></div>

            <div className="workflow-step">
              <div className="step-number">2</div>
              <h4>Cost & Margin Calculator</h4>
              <p>Smart Pricing Agent calculates material, labor, overheads, and prevents underpricing before contract confirmation.</p>
            </div>
            <div className="workflow-arrow"><ChevronRight size={24} /></div>

            <div className="workflow-step highlight">
              <div className="step-number">3</div>
              <h4>AI Work Allocation</h4>
              <p>Allocates tasks based on historical speed, skill rating, and predicts completion likelihood for each member.</p>
            </div>
            <div className="workflow-arrow"><ChevronRight size={24} /></div>

            <div className="workflow-step">
              <div className="step-number">4</div>
              <h4>Leader Review & Approval</h4>
              <p>AI recommendations require leader confirmation before tasks are assigned to member mobile dashboards.</p>
            </div>
          </div>

          <div className="workflow-diagram" style={{ marginTop: '20px' }}>
            <div className="workflow-step">
              <div className="step-number">5</div>
              <h4>Distributed Production</h4>
              <p>Members craft from home, update piece counts, and access voice assistance in Kannada, Hindi, or English.</p>
            </div>
            <div className="workflow-arrow"><ChevronRight size={24} /></div>

            <div className="workflow-step highlight">
              <div className="step-number">6</div>
              <h4>AI Quality Inspection</h4>
              <p>Computer Vision flags stitching and dimension flaws early. Inspector verifies and decides on rework.</p>
            </div>
            <div className="workflow-arrow"><ChevronRight size={24} /></div>

            <div className="workflow-step">
              <div className="step-number">7</div>
              <h4>Logistics & Consolidation</h4>
              <p>Consolidates cartons, reserves stock cleanly from retail, and routes to buyer with verified proof-of-dispatch.</p>
            </div>
            <div className="workflow-arrow"><ChevronRight size={24} /></div>

            <div className="workflow-step">
              <div className="step-number">8</div>
              <h4>Group Quorum Payout</h4>
              <p>Earnings ledger is published. Payouts require 60% affirmative member voting before bank dispatch.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Core Features Grid */}
      <section className="landing-section bg-white">
        <div className="section-container">
          <div className="section-header">
            <span className="section-kicker">ENTERPRISE CAPABILITIES</span>
            <h2 className="section-title">Built for Real SHG Production Realities</h2>
            <p className="section-desc">Designed with simple, accessible UI for women artisans alongside rigorous enterprise analytics.</p>
          </div>

          <div className="grid grid-cols-3">
            <div className="feature-card">
              <div className="feature-icon"><Brain size={22} /></div>
              <h4>Worker Completion Prediction</h4>
              <p>Distinguishes actual production progress from AI-predicted completion likelihood using historical speed, availability, and task complexity.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon"><Eye size={22} /></div>
              <h4>AI-Assisted Quality Control</h4>
              <p>Batch photo inspection detects seam misalignment, fabric defects, and measurement variance before delivery dispatch.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon"><DollarSign size={22} /></div>
              <h4>Smart Pricing & Costing Engine</h4>
              <p>Calculates unit production costs, suggests optimal selling prices, and issues prominent alerts if an order is underpriced.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon"><ShieldCheck size={22} /></div>
              <h4>Transparent Group-Approved Payouts</h4>
              <p>Fair piece-rate compensation breakdown. Zero secret deductions. Requires democratic 60% member quorum voting.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon"><Layers size={22} /></div>
              <h4>Unified Wholesale & Retail Inventory</h4>
              <p>Protects stock reserved for bulk buyer contracts from being double-sold on the public artisan marketplace.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon"><Sparkles size={22} /></div>
              <h4>Multilingual Voice Saathi</h4>
              <p>Simple voice-first interface in Kannada, Hindi, and English so members can ask: "How many bags have I completed?"</p>
            </div>
          </div>
        </div>
      </section>

      {/* Retail Marketplace Preview */}
      <section className="landing-section">
        <div className="section-container">
          <div className="section-header">
            <span className="section-kicker">SUPPORTING ECOSYSTEM</span>
            <h2 className="section-title">Direct Public Artisan Marketplace</h2>
            <p className="section-desc">
              Surplus capacity is listed on the public retail storefront, connecting verified rural artisan clusters directly to conscious consumers.
            </p>
          </div>

          <div className="grid grid-cols-4">
            {DEMO_RETAIL_PRODUCTS.map((prod) => (
              <div key={prod.id} className="landing-product-card card">
                <div className="product-image-box">
                  <img src={prod.imageUrl} alt={prod.name} />
                  <span className="product-category-tag">{prod.category}</span>
                </div>
                <div className="product-info-box">
                  <h4 className="product-name">{prod.name}</h4>
                  <p className="product-shg">By {prod.shgName}, {prod.location}</p>
                  <div className="product-price-row">
                    <span className="product-price">₹{prod.price}</span>
                    <span className="product-stock-tag">{prod.availableStock} in stock</span>
                  </div>
                  <Link to={`/marketplace`} className="btn btn-secondary btn-sm" style={{ width: '100%', marginTop: '10px' }}>
                    View in Marketplace
                  </Link>
                </div>
              </div>
            ))}
          </div>

          <div style={{ textAlign: 'center', marginTop: '30px' }}>
            <Link to="/marketplace" className="btn btn-outline btn-lg">
              <Store size={18} /> Browse Full Artisan Marketplace
            </Link>
          </div>
        </div>
      </section>

      {/* Impact & Alignment with NRLM */}
      <section className="landing-section bg-white">
        <div className="section-container">
          <div className="impact-box">
            <div className="impact-text">
              <span className="section-kicker" style={{ color: '#E6A23C' }}>GOVERNMENT & FEDERATION IMPACT</span>
              <h2>Powering the Lakhpati Didi Mission</h2>
              <p>
                Aligned with the Ministry of Rural Development's vision to elevate women SHG members to sustainable annual incomes exceeding ₹1,00,000. SHG Saathi provides Federation Officers with cluster-wide analytics, quality benchmarking, and institutional procurement dashboards.
              </p>
              <div style={{ display: 'flex', gap: '16px', marginTop: '20px' }}>
                <Link to="/federation" className="btn btn-primary">
                  View Federation Dashboard
                </Link>
                <Link to="/login" className="btn btn-outline">
                  Sign In to Your SHG
                </Link>
              </div>
            </div>
            <div className="impact-numbers">
              <div className="impact-metric">
                <span className="metric-val">₹48,200</span>
                <span className="metric-lbl">Avg. Extra Member Earnings per Bulk Cycle</span>
              </div>
              <div className="impact-metric">
                <span className="metric-val">0%</span>
                <span className="metric-lbl">Unverified Underpricing on the Platform</span>
              </div>
              <div className="impact-metric">
                <span className="metric-val">100%</span>
                <span className="metric-lbl">Auditable Member Payout Ledgers</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;

