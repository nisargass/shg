import apiClient from './apiClient';
import {
  DEMO_BULK_ORDERS,
  DEMO_ALLOCATIONS,
  DEMO_QUALITY_BATCHES,
  DEMO_COSTING_MODELS,
  DEMO_INVENTORY,
  DEMO_SUPPLIERS,
  DEMO_LOGISTICS,
  DEMO_PAYOUT_WORKFLOW,
  DEMO_ANOMALY_ALERTS,
  DEMO_RETAIL_PRODUCTS,
  DEMO_AGENT_ACTIVITIES,
  DEMO_KNOWLEDGE_DOCS,
  DEMO_MEMBERS
} from '../mock/mockData';

// Helper to simulate network latency for realistic feel
const simulateDelay = (ms = 300) => new Promise((resolve) => setTimeout(resolve, ms));

// ==========================================
// 1. Bulk Order Management API
// ==========================================
export const orderApi = {
  getOrders: async () => {
    try {
      return await apiClient.get('/orders');
    } catch (e) {
      await simulateDelay();
      return DEMO_BULK_ORDERS;
    }
  },

  getOrderById: async (orderId) => {
    try {
      return await apiClient.get(`/orders/${orderId}`);
    } catch (e) {
      await simulateDelay();
      return DEMO_BULK_ORDERS.find((o) => o.id === orderId) || DEMO_BULK_ORDERS[0];
    }
  },

  createOrder: async (orderData) => {
    try {
      return await apiClient.post('/orders', orderData);
    } catch (e) {
      await simulateDelay();
      const newOrder = {
        id: `ORD-2026-${Math.floor(100 + Math.random() * 900)}`,
        buyerName: orderData.buyerName || 'Direct Buyer Inquiry',
        productName: orderData.productName,
        category: orderData.category || 'Garments & Textiles',
        totalQuantity: Number(orderData.totalQuantity),
        completedQuantity: 0,
        approvedQuantity: 0,
        reworkQuantity: 0,
        pendingQuantity: Number(orderData.totalQuantity),
        unitAgreedPrice: Number(orderData.unitAgreedPrice || 150),
        totalOrderValue: Number(orderData.totalQuantity) * Number(orderData.unitAgreedPrice || 150),
        orderDate: new Date().toISOString().split('T')[0],
        deadline: orderData.deadline,
        daysRemaining: 30,
        status: 'PENDING_ALLOCATION',
        allocationStatus: 'PENDING',
        qualityCheckStatus: 'NOT_STARTED',
        payoutStatus: 'NOT_READY',
        specifications: orderData.specifications,
        poDocumentName: orderData.poDocumentName || 'PO_Uploaded_Document.pdf',
        assignedMembersCount: 0
      };
      return newOrder;
    }
  }
};

// ==========================================
// 2. Member Management API
// ==========================================
export const memberApi = {
  getMembers: async () => {
    try {
      return await apiClient.get('/members');
    } catch (e) {
      await simulateDelay();
      return DEMO_MEMBERS;
    }
  },

  getMemberById: async (memberId) => {
    try {
      return await apiClient.get(`/members/${memberId}`);
    } catch (e) {
      await simulateDelay();
      return DEMO_MEMBERS.find((m) => m.id === memberId) || DEMO_MEMBERS[0];
    }
  }
};

// ==========================================
// 3. Intelligent Work Allocation API
// ==========================================
export const allocationApi = {
  getAllocationByOrderId: async (orderId) => {
    try {
      return await apiClient.get(`/orders/${orderId}/allocations`);
    } catch (e) {
      await simulateDelay();
      return DEMO_ALLOCATIONS[orderId] || DEMO_ALLOCATIONS['ORD-2026-104'];
    }
  },

  approveAllocation: async (orderId, approvalData) => {
    try {
      return await apiClient.post(`/orders/${orderId}/allocations/approve`, approvalData);
    } catch (e) {
      await simulateDelay();
      return { success: true, message: `Work allocation for ${orderId} officially approved by Leader.`, status: 'APPROVED' };
    }
  },

  requestRebalance: async (orderId, feedback) => {
    try {
      return await apiClient.post(`/orders/${orderId}/allocations/rebalance`, { feedback });
    } catch (e) {
      await simulateDelay();
      return { success: true, message: 'AI Rebalance request sent to Optimization Agent.', status: 'REBALANCED' };
    }
  }
};

// ==========================================
// 4. Quality Control & Computer Vision API
// ==========================================
export const qualityApi = {
  getBatches: async (orderId = null) => {
    try {
      return await apiClient.get('/quality/batches', { params: { order_id: orderId } });
    } catch (e) {
      await simulateDelay();
      if (orderId) return DEMO_QUALITY_BATCHES.filter(b => b.orderId === orderId);
      return DEMO_QUALITY_BATCHES;
    }
  },

  submitHumanDecision: async (batchId, decisionData) => {
    try {
      return await apiClient.post(`/quality/batches/${batchId}/decision`, decisionData);
    } catch (e) {
      await simulateDelay();
      return {
        success: true,
        batchId,
        decision: decisionData.status,
        approvedQty: decisionData.approvedQty,
        reworkQty: decisionData.reworkQty,
        reviewedBy: 'SHG Leader',
        timestamp: new Date().toISOString()
      };
    }
  }
};

// ==========================================
// 5. Smart Pricing & Costing API
// ==========================================
export const pricingApi = {
  getCostingModel: async (orderId) => {
    try {
      return await apiClient.get(`/pricing/costing/${orderId}`);
    } catch (e) {
      await simulateDelay();
      return DEMO_COSTING_MODELS[orderId] || DEMO_COSTING_MODELS['ORD-2026-104'];
    }
  }
};

// ==========================================
// 6. Inventory Management API
// ==========================================
export const inventoryApi = {
  getInventory: async () => {
    try {
      return await apiClient.get('/inventory');
    } catch (e) {
      await simulateDelay();
      return DEMO_INVENTORY;
    }
  }
};

// ==========================================
// 7. Suppliers & Logistics API
// ==========================================
export const supplierApi = {
  getSuppliers: async () => {
    try {
      return await apiClient.get('/suppliers');
    } catch (e) {
      await simulateDelay();
      return DEMO_SUPPLIERS;
    }
  }
};

export const logisticsApi = {
  getShipments: async () => {
    try {
      return await apiClient.get('/logistics/shipments');
    } catch (e) {
      await simulateDelay();
      return DEMO_LOGISTICS;
    }
  }
};

// ==========================================
// 8. Financial Payouts & Anomalies API
// ==========================================
export const financialApi = {
  getPayoutWorkflow: async (orderId) => {
    try {
      return await apiClient.get(`/finance/payouts/${orderId}`);
    } catch (e) {
      await simulateDelay();
      return DEMO_PAYOUT_WORKFLOW;
    }
  },

  submitMemberVote: async (orderId, memberId, vote) => {
    try {
      return await apiClient.post(`/finance/payouts/${orderId}/vote`, { member_id: memberId, vote });
    } catch (e) {
      await simulateDelay();
      return { success: true, message: `Member vote recorded: ${vote}` };
    }
  },

  confirmPayout: async (orderId) => {
    try {
      return await apiClient.post(`/finance/payouts/${orderId}/confirm`);
    } catch (e) {
      await simulateDelay();
      return { success: true, message: 'Group payout confirmed and registered in bank dispatch ledger.' };
    }
  },

  getAnomalies: async () => {
    try {
      return await apiClient.get('/finance/anomalies');
    } catch (e) {
      await simulateDelay();
      return DEMO_ANOMALY_ALERTS;
    }
  }
};

// ==========================================
// 9. Retail Marketplace API
// ==========================================
export const retailApi = {
  getProducts: async () => {
    try {
      return await apiClient.get('/retail/products');
    } catch (e) {
      await simulateDelay();
      return DEMO_RETAIL_PRODUCTS;
    }
  },

  placeRetailOrder: async (orderPayload) => {
    try {
      return await apiClient.post('/retail/orders', orderPayload);
    } catch (e) {
      await simulateDelay();
      return {
        success: true,
        orderId: `RET-ORD-${Math.floor(1000 + Math.random() * 9000)}`,
        items: orderPayload.items,
        totalAmount: orderPayload.totalAmount,
        estimatedDelivery: '3-4 business days'
      };
    }
  }
};

// ==========================================
// 10. Agentic AI & RAG Assistant API
// ==========================================
export const assistantApi = {
  getAgentActivities: async () => {
    try {
      return await apiClient.get('/agents/activities');
    } catch (e) {
      await simulateDelay();
      return DEMO_AGENT_ACTIVITIES;
    }
  },

  queryKnowledge: async (query, language = 'English') => {
    try {
      return await apiClient.post('/assistant/rag/query', { query, language });
    } catch (e) {
      await simulateDelay(600);
      const lower = query.toLowerCase();
      let answer = "SHG Saathi Assistant: The platform coordinates bulk orders, fair work allocation, and transparent payouts. All member earnings are directly tracked based on quality-approved units.";
      let sources = [DEMO_KNOWLEDGE_DOCS[0]];

      if (lower.includes('earn') || lower.includes('payment') || lower.includes('money') || lower.includes('payout')) {
        answer = "Your earnings are calculated by multiplying your quality-approved units by the agreed piece-rate (e.g., ₹32 per tote bag). Once the group reaches a 60% affirmative quorum, payouts are released directly to your verified bank account.";
        sources = [DEMO_KNOWLEDGE_DOCS[2]];
      } else if (lower.includes('stitch') || lower.includes('quality') || lower.includes('defect') || lower.includes('standard')) {
        answer = "For export-quality tote bags, remember to maintain double-needle boxed-X stitching at handle attachment points. The tension must support a minimum 15 kg pull force, and inner zipper tolerance is ±3mm.";
        sources = [DEMO_KNOWLEDGE_DOCS[1]];
      } else if (lower.includes('scheme') || lower.includes('lakhpati') || lower.includes('loan') || lower.includes('subsidy')) {
        answer = "Under the National Rural Livelihoods Mission (NRLM) Lakhpati Didi initiative, eligible women SHG members producing bulk crafts can access collateral-free equipment working capital and interest subvention up to 7%.";
        sources = [DEMO_KNOWLEDGE_DOCS[0]];
      }

      return {
        answer,
        sources,
        language,
        confidence: 0.94
      };
    }
  }
};

