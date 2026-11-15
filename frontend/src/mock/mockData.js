// SHG Saathi - Realistic Demo Dataset
// All data clearly identified as simulation / demo for offline / pre-backend verification.

export const DEMO_USERS = {
  leader: {
    id: "usr_lead_01",
    name: "Savitribai Shinde",
    role: "SHG_LEADER",
    shgName: "Pragati Mahila Sangha",
    location: "Ramanagara District, Karnataka",
    phone: "+91 98452 11045",
    avatar: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&q=80&w=150"
  },
  member: {
    id: "mem_01",
    name: "Sunita Rathod",
    role: "SHG_MEMBER",
    shgName: "Pragati Mahila Sangha",
    skills: ["Heavy Fabric Stitching", "Bag Handle Attachment", "Zipper Fixing"],
    skillLevel: "Advanced",
    phone: "+91 97412 88390",
    experienceYears: 4,
    avatar: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=150"
  },
  buyer: {
    id: "usr_buy_01",
    name: "Arvind Deshmukh",
    company: "EcoFab Bangalore Retailers Ltd.",
    role: "BUYER",
    phone: "+91 98200 44521",
    email: "procurement@ecofab.in",
    avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=150"
  },
  federation: {
    id: "usr_fed_01",
    name: "Deepa Narayan, KAS",
    title: "Cluster Development Officer",
    role: "FEDERATION_OFFICER",
    federationName: "Sanjeevini KSRLPS (National Rural Livelihoods Mission)",
    district: "Ramanagara Cluster",
    phone: "+91 94481 02941",
    avatar: "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&q=80&w=150"
  },
  customer: {
    id: "usr_cust_01",
    name: "Pooja Hegde",
    role: "CUSTOMER",
    phone: "+91 99801 33490",
    email: "pooja.h@gmail.com"
  }
};

export const DEMO_MEMBERS = [
  {
    id: "mem_01",
    name: "Sunita Rathod",
    skills: ["Heavy Fabric Stitching", "Handle Fitting"],
    skillLevel: "Expert (Tier 1)",
    speedUnitsPerHour: 3.2,
    availableHoursPerDay: 5,
    assignedWorkload: 180,
    historicalOnTimeRate: 96,
    historicalQualityRate: 98,
    activeTasks: 1,
    village: "Channapatna",
    phone: "+91 97412 88390",
    accountNumber: "SBIN0040192 (A/C ...4821)"
  },
  {
    id: "mem_02",
    name: "Radhabai Hiremath",
    skills: ["Fabric Cutting", "Pattern Stenciling"],
    skillLevel: "Advanced",
    speedUnitsPerHour: 5.0,
    availableHoursPerDay: 6,
    assignedWorkload: 220,
    historicalOnTimeRate: 92,
    historicalQualityRate: 95,
    activeTasks: 1,
    village: "Ijoor",
    phone: "+91 98450 71123",
    accountNumber: "KARB0000122 (A/C ...9102)"
  },
  {
    id: "mem_03",
    name: "Lakshmi Devamma",
    skills: ["Precision Stitching", "Quality Inspection"],
    skillLevel: "Master Craftsman",
    speedUnitsPerHour: 2.8,
    availableHoursPerDay: 4.5,
    assignedWorkload: 150,
    historicalOnTimeRate: 98,
    historicalQualityRate: 99,
    activeTasks: 1,
    village: "Kailancha",
    phone: "+91 94812 55210",
    accountNumber: "CNRB0001882 (A/C ...3319)"
  },
  {
    id: "mem_04",
    name: "Meenakshi Kulkarni",
    skills: ["Zipper Attachment", "Lining Stitching"],
    skillLevel: "Intermediate",
    speedUnitsPerHour: 2.2,
    availableHoursPerDay: 4,
    assignedWorkload: 120,
    historicalOnTimeRate: 88,
    historicalQualityRate: 91,
    activeTasks: 1,
    village: "Bidadi",
    phone: "+91 99014 38291",
    accountNumber: "BARB0CHANN (A/C ...5501)"
  },
  {
    id: "mem_05",
    name: "Anusuya Bai",
    skills: ["Embroidery", "Screen Printing Finishing"],
    skillLevel: "Advanced",
    speedUnitsPerHour: 2.5,
    availableHoursPerDay: 5,
    assignedWorkload: 140,
    historicalOnTimeRate: 94,
    historicalQualityRate: 97,
    activeTasks: 1,
    village: "Channapatna",
    phone: "+91 96112 04821",
    accountNumber: "SBIN0040192 (A/C ...1190)"
  },
  {
    id: "mem_06",
    name: "Parvati Gowda",
    skills: ["Ironing & Packaging", "Label Tagging"],
    skillLevel: "Standard",
    speedUnitsPerHour: 7.5,
    availableHoursPerDay: 6,
    assignedWorkload: 250,
    historicalOnTimeRate: 95,
    historicalQualityRate: 98,
    activeTasks: 1,
    village: "Ijoor",
    phone: "+91 98801 77294",
    accountNumber: "PKGB0012093 (A/C ...7712)"
  },
  {
    id: "mem_07",
    name: "Kavitha Shrinivas",
    skills: ["Heavy Fabric Stitching"],
    skillLevel: "Intermediate",
    speedUnitsPerHour: 2.0,
    availableHoursPerDay: 3.5,
    assignedWorkload: 90,
    historicalOnTimeRate: 85,
    historicalQualityRate: 92,
    activeTasks: 1,
    village: "Ramanagara Town",
    phone: "+91 97312 90114",
    accountNumber: "KARB0000122 (A/C ...8841)"
  },
  {
    id: "mem_08",
    name: "Shobha Manjunath",
    skills: ["Food Processing", "Hygienic Jar Packaging"],
    skillLevel: "Certified FSSAI",
    speedUnitsPerHour: 10.0,
    availableHoursPerDay: 6,
    assignedWorkload: 0,
    historicalOnTimeRate: 97,
    historicalQualityRate: 99,
    activeTasks: 0,
    village: "Channapatna",
    phone: "+91 94498 12390",
    accountNumber: "CNRB0001882 (A/C ...4402)"
  }
];

export const DEMO_BULK_ORDERS = [
  {
    id: "ORD-2026-104",
    buyerName: "EcoFab Bangalore Retailers Ltd.",
    productName: "Organic Cotton Tote Bags (Heavy 280 GSM)",
    category: "Garments & Textiles",
    totalQuantity: 1200,
    completedQuantity: 840,
    approvedQuantity: 790,
    reworkQuantity: 35,
    pendingQuantity: 360,
    unitAgreedPrice: 165.0,
    totalOrderValue: 198000.0,
    orderDate: "2026-10-15",
    deadline: "2026-11-20",
    daysRemaining: 13,
    status: "IN_PRODUCTION",
    allocationStatus: "APPROVED",
    qualityCheckStatus: "PARTIALLY_INSPECTED",
    payoutStatus: "AWAITING_FINAL_COMPLETION",
    specifications: "100% natural unbleached cotton, double reinforced X-stitch cross handle, inner 6x6 zipper pocket, silk-screen eco logo on front.",
    poDocumentName: "PO_EcoFab_1200_Bags_Oct26.pdf",
    assignedMembersCount: 7
  },
  {
    id: "ORD-2026-108",
    buyerName: "Karnataka State Handloom & Handicrafts Corp",
    productName: "Kasuti Embroidered Jute Table Runners",
    category: "Handicrafts & Decor",
    totalQuantity: 500,
    completedQuantity: 120,
    approvedQuantity: 115,
    reworkQuantity: 5,
    pendingQuantity: 380,
    unitAgreedPrice: 380.0,
    totalOrderValue: 190000.0,
    orderDate: "2026-10-28",
    deadline: "2026-11-30",
    daysRemaining: 23,
    status: "IN_PRODUCTION",
    allocationStatus: "APPROVED",
    qualityCheckStatus: "IN_PROGRESS",
    payoutStatus: "PENDING_APPROVAL",
    specifications: "Golden natural jute 350 GSM with traditional Ilkal Kasuti border thread work, heat-pressed backing.",
    poDocumentName: "KSHDC_Govt_PO_9934.pdf",
    assignedMembersCount: 5
  },
  {
    id: "ORD-2026-112",
    buyerName: "Arogya Wellness Organics",
    productName: "Stone-Ground Curcumin Rich Turmeric 500g Jars",
    category: "Food Products",
    totalQuantity: 800,
    completedQuantity: 0,
    approvedQuantity: 0,
    reworkQuantity: 0,
    pendingQuantity: 800,
    unitAgreedPrice: 195.0,
    totalOrderValue: 156000.0,
    orderDate: "2026-11-04",
    deadline: "2026-12-05",
    daysRemaining: 28,
    status: "PENDING_ALLOCATION",
    allocationStatus: "RECOMMENDED",
    qualityCheckStatus: "NOT_STARTED",
    payoutStatus: "NOT_READY",
    specifications: "Certified organic Salem variety turmeric, cold-milled, food-grade airtight amber PET jars with foil induction seal.",
    poDocumentName: "Arogya_Turmeric_PO_800Jars.pdf",
    assignedMembersCount: 0
  }
];

export const DEMO_ALLOCATIONS = {
  "ORD-2026-104": [
    {
      memberId: "mem_01",
      memberName: "Sunita Rathod",
      roleTask: "Main Body Stitching & Handle Assembly",
      allocatedQty: 220,
      completedQty: 180,
      feasibleQty: 230,
      completionLikelihood: 94,
      predictionConfidence: "HIGH (92%)",
      skillMatchScore: 98,
      speedRate: "3.2 bags/hr",
      availableHoursDaily: 5,
      explanation: "Sunita has a 96% historical on-time delivery record and highest precision score for handle stress points. 220 units is well within her 25-day capacity envelope.",
      factors: ["High skill match (98%)", "Stable 5h/day availability", "Verified zero rework in last 3 batches"]
    },
    {
      memberId: "mem_02",
      memberName: "Radhabai Hiremath",
      roleTask: "Pattern Cutting & Fabric Prep",
      allocatedQty: 300,
      completedQty: 240,
      feasibleQty: 310,
      completionLikelihood: 92,
      predictionConfidence: "HIGH (90%)",
      skillMatchScore: 95,
      speedRate: "5.0 units/hr",
      availableHoursDaily: 6,
      explanation: "Radhabai specializes in speed pattern cutting with minimal raw cloth wastage. Current progress matches model projection.",
      factors: ["Expert fabric cutter", "6h/day availability", "Raw material delivered to home workshop"]
    },
    {
      memberId: "mem_03",
      memberName: "Lakshmi Devamma",
      roleTask: "Gusset Joining & Internal Pocket Stitching",
      allocatedQty: 180,
      completedQty: 140,
      feasibleQty: 185,
      completionLikelihood: 96,
      predictionConfidence: "VERY HIGH (95%)",
      skillMatchScore: 99,
      speedRate: "2.8 bags/hr",
      availableHoursDaily: 4.5,
      explanation: "Master stitcher with 99% historical acceptance. Perfect fit for complex zipper pocket integration.",
      factors: ["Highest quality rating", "Consistent delivery", "Nearby inspection depot"]
    },
    {
      memberId: "mem_04",
      memberName: "Meenakshi Kulkarni",
      roleTask: "Base Stitching & Overlock",
      allocatedQty: 160,
      completedQty: 110,
      feasibleQty: 155,
      completionLikelihood: 84,
      predictionConfidence: "MEDIUM (81%)",
      skillMatchScore: 88,
      speedRate: "2.2 bags/hr",
      availableHoursDaily: 4,
      explanation: "Slight delay due to festival break last week; model recommends providing pre-cut handles to maintain delivery date.",
      factors: ["Moderate speed", "Recent family event", "Requires check on day 10"]
    },
    {
      memberId: "mem_05",
      memberName: "Anusuya Bai",
      roleTask: "Screen Printing & Quality Finishing",
      allocatedQty: 180,
      completedQty: 90,
      feasibleQty: 190,
      completionLikelihood: 90,
      predictionConfidence: "HIGH (88%)",
      skillMatchScore: 94,
      speedRate: "2.5 bags/hr",
      availableHoursDaily: 5,
      explanation: "Anusuya operates the group's dual screen-printing bench. Excellent ink curing rate.",
      factors: ["Specialist skill", "Weather dependent ink curing", "Backup heating lamps provided"]
    },
    {
      memberId: "mem_06",
      memberName: "Parvati Gowda",
      roleTask: "Steam Ironing, Thread Trimming & Tagging",
      allocatedQty: 160,
      completedQty: 80,
      feasibleQty: 180,
      completionLikelihood: 95,
      predictionConfidence: "HIGH (92%)",
      skillMatchScore: 96,
      speedRate: "7.5 units/hr",
      availableHoursDaily: 6,
      explanation: "Parvati handles packaging and tagging directly before carton loading. Speed rate ensures no bottleneck at dispatch.",
      factors: ["High units per hour", "Quality checkpoint", "Final batch packer"]
    }
  ]
};

export const DEMO_QUALITY_BATCHES = [
  {
    batchId: "QCB-2026-081",
    orderId: "ORD-2026-104",
    productName: "Organic Cotton Tote Bags",
    memberId: "mem_01",
    memberName: "Sunita Rathod",
    submittedQty: 50,
    submissionDate: "2026-11-05",
    photoUrl: "https://images.unsplash.com/photo-1597484661643-2f5fef640dd1?auto=format&fit=crop&q=80&w=400",
    aiInspection: {
      defectStatus: "PASS_WITH_WARNING",
      overallConfidence: 94.2,
      detectedIssues: [
        { type: "Handle Cross Stitch", severity: "LOW", detail: "Minor thread tension variance on 2/50 units; passes strength test (>15kg)" },
        { type: "Dimension Uniformity", severity: "NONE", detail: "Within +/- 0.5 cm of buyer CAD specification" },
        { type: "Fabric Flaws", severity: "NONE", detail: "Clean unbleached weave without snagging" }
      ],
      aiRecommendation: "Approve 48 units, request minor trim rework on 2 units"
    },
    humanReview: {
      status: "APPROVED_WITH_MINOR_REWORK",
      reviewedBy: "Savitribai Shinde (Leader)",
      approvedQty: 48,
      reworkQty: 2,
      reviewDate: "2026-11-06",
      leaderRemarks: "Sunita fixed the two thread ends in our presence. Full 50 accepted into consolidation bin."
    }
  },
  {
    batchId: "QCB-2026-085",
    orderId: "ORD-2026-104",
    productName: "Organic Cotton Tote Bags",
    memberId: "mem_04",
    memberName: "Meenakshi Kulkarni",
    submittedQty: 35,
    submissionDate: "2026-11-07",
    photoUrl: "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&q=80&w=400",
    aiInspection: {
      defectStatus: "DEFECTS_DETECTED",
      overallConfidence: 89.5,
      detectedIssues: [
        { type: "Zipper Alignment", severity: "MEDIUM", detail: "Wavy stitching along inner zipper on 6 units (exceeds 3mm tolerance)" },
        { type: "Thread Trimming", severity: "LOW", detail: "Excess loose thread tails at base seam on 4 units" }
      ],
      aiRecommendation: "Recommend rework on 6 units for zipper restitching prior to carton packing."
    },
    humanReview: {
      status: "PENDING_DECISION",
      reviewedBy: null,
      approvedQty: 0,
      reworkQty: 0,
      reviewDate: null,
      leaderRemarks: ""
    }
  }
];

export const DEMO_COSTING_MODELS = {
  "ORD-2026-104": {
    productName: "Organic Cotton Tote Bag (Heavy 280 GSM)",
    orderQty: 1200,
    costComponents: [
      { name: "Raw Cotton Canvas Fabric (1.2m @ ₹72/m)", unitCost: 86.4, total: 103680 },
      { name: "Heavy Cotton Webbing Handles (1.4m @ ₹8/m)", unitCost: 11.2, total: 13440 },
      { name: "Inner Zippers & Metal Sliders", unitCost: 6.5, total: 7800 },
      { name: "High-Tensile Thread & Printing Ink", unitCost: 4.8, total: 5760 },
      { name: "Direct Member Labor Compensation (Piece-rate)", unitCost: 32.0, total: 38400 },
      { name: "Eco Packaging & Recycled Tagging", unitCost: 3.5, total: 4200 },
      { name: "Local Village-to-Cluster Hub Transport", unitCost: 3.2, total: 3840 },
      { name: "SHG Common Facility Overhead & Machine Maint.", unitCost: 4.0, total: 4800 }
    ],
    totalProductionCost: 151.6,
    totalProductionCostTotal: 181920,
    buyerAgreedPrice: 165.0,
    buyerTotalRevenue: 198000,
    suggestedMinSellingPrice: 162.0,
    recommendedOptimalPrice: 172.0,
    groupNetMargin: 13.4, // Rs per unit
    groupNetProfitTotal: 16080,
    marginPercentage: 8.12,
    aiPricingInsights: {
      underpricingAlert: false,
      marketBenchmark: "Bangalore wholesale rate for 280 GSM custom bags is ₹160 - ₹175 per unit.",
      advice: "Your agreed price of ₹165 leaves an 8.1% net surplus for the SHG group fund after paying members their fair ₹32/bag labor rate."
    }
  }
};

export const DEMO_INVENTORY = [
  {
    sku: "MAT-COT-280",
    name: "Heavy 280 GSM Unbleached Cotton Canvas",
    category: "Raw Material",
    unit: "Meters",
    physicalStock: 1850,
    reservedForBulkOrders: 1440,
    reservedForRetailOrders: 60,
    freeAvailableStock: 350,
    reorderLevel: 250,
    unitCost: 72.0,
    supplier: "Venkateshwara Weaving Mills, Davanagere",
    status: "HEALTHY"
  },
  {
    sku: "MAT-WEB-HDL",
    name: "Natural Cotton Herringbone Webbing (38mm)",
    category: "Raw Material",
    unit: "Meters",
    physicalStock: 1900,
    reservedForBulkOrders: 1680,
    reservedForRetailOrders: 80,
    freeAvailableStock: 140,
    reorderLevel: 200,
    unitCost: 8.0,
    supplier: "Sri Lakshmi Tapes & Ribbons, Bangalore",
    status: "REORDER_WARNING"
  },
  {
    sku: "MAT-ZIP-06",
    name: "6-inch YKK Brass Antique Metal Zippers",
    category: "Raw Material",
    unit: "Pieces",
    physicalStock: 1600,
    reservedForBulkOrders: 1200,
    reservedForRetailOrders: 100,
    freeAvailableStock: 300,
    reorderLevel: 250,
    unitCost: 6.5,
    supplier: "Karnataka Fasteners Hub",
    status: "HEALTHY"
  },
  {
    sku: "PRD-TOT-01",
    name: "Classic Eco Cotton Tote Bag (Finished)",
    category: "Finished Goods",
    unit: "Pieces",
    physicalStock: 840,
    reservedForBulkOrders: 790,
    reservedForRetailOrders: 25,
    freeAvailableStock: 25,
    reorderLevel: 20,
    unitCost: 151.6,
    retailSellingPrice: 220.0,
    status: "IN_CIRCULATION"
  },
  {
    sku: "PRD-RUN-02",
    name: "Kasuti Embroidered Table Runner (Finished)",
    category: "Finished Goods",
    unit: "Pieces",
    physicalStock: 120,
    reservedForBulkOrders: 115,
    reservedForRetailOrders: 3,
    freeAvailableStock: 2,
    reorderLevel: 5,
    unitCost: 310.0,
    retailSellingPrice: 480.0,
    status: "LOW_STOCK"
  }
];

export const DEMO_SUPPLIERS = [
  {
    id: "SUP-01",
    name: "Venkateshwara Weaving Mills",
    contactPerson: "R. Muralidharan",
    phone: "+91 94480 33190",
    city: "Davanagere, Karnataka",
    materials: ["Heavy Cotton Canvas 280 GSM", "Grey Cloth 220 GSM"],
    leadTimeDays: 4,
    rating: 4.8,
    lastQuotePrice: "₹72.00 / meter",
    paymentTerms: "Net 15 days via SHG Bank Transfer"
  },
  {
    id: "SUP-02",
    name: "Sri Lakshmi Tapes & Ribbons",
    contactPerson: "K. Venkatesh",
    phone: "+91 98860 12093",
    city: "Rajajinagar, Bangalore",
    materials: ["Cotton Webbing Handles", "Jute Twine Ribbons"],
    leadTimeDays: 2,
    rating: 4.6,
    lastQuotePrice: "₹8.00 / meter",
    paymentTerms: "Immediate upon delivery check"
  },
  {
    id: "SUP-03",
    name: "GreenEarth Packaging Solutions",
    contactPerson: "Ananya Hegde",
    phone: "+91 99002 81123",
    city: "Bidadi Industrial Area",
    materials: ["Recycled Kraft Cartons", "Eco Cotton Tags", "Cornstarch Bags"],
    leadTimeDays: 3,
    rating: 4.9,
    lastQuotePrice: "₹3.50 / tag & liner set",
    paymentTerms: "UPI / Bank Transfer"
  }
];

export const DEMO_LOGISTICS = [
  {
    id: "LOG-OUT-902",
    type: "OUTBOUND",
    orderId: "ORD-2026-104",
    recipient: "EcoFab Bangalore Retailers Ltd.",
    destination: "Warehouse 4, Peenya Industrial Area, Bangalore",
    cargoDescription: "Batch 1: 500 Completed Cotton Tote Bags (10 master cartons)",
    carrierName: "VRL Village Logistics & Rural Express",
    vehicleNumber: "KA-42-B-8912",
    driverName: "Manjunath Gowda (+91 98450 10293)",
    dispatchDate: "2026-11-06",
    expectedDelivery: "2026-11-08",
    status: "DISPATCHED_IN_TRANSIT",
    transportCost: 1850.0,
    proofOfPickup: "VRLExpr_Channa_B4902.pdf"
  },
  {
    id: "LOG-IN-401",
    type: "INBOUND",
    supplierName: "Venkateshwara Weaving Mills",
    origin: "Davanagere Textile Hub",
    destination: "Pragati SHG Common Center, Channapatna",
    cargoDescription: "500m Raw Canvas Roll consignment",
    carrierName: "Navata Road Transport",
    vehicleNumber: "KA-17-A-4431",
    driverName: "Suresh Patil (+91 97401 22841)",
    dispatchDate: "2026-11-03",
    expectedDelivery: "2026-11-05",
    status: "DELIVERED_RECEIVED",
    transportCost: 1400.0,
    proofOfPickup: "Navata_Waybill_9921.pdf"
  }
];

export const DEMO_PAYOUT_WORKFLOW = {
  orderId: "ORD-2026-104",
  productName: "Organic Cotton Tote Bags",
  batchMilestone: "Interim Milestone 1 (600 Approved Bags)",
  totalApprovedAmount: 19200.0, // 600 bags * Rs 32/bag
  quorumRequired: 5,
  votesReceived: 4,
  approvalStatus: "VOTING_IN_PROGRESS",
  leaderConfirmation: "PENDING_QUORUM",
  votingDeadline: "2026-11-10",
  membersPayoutList: [
    {
      memberId: "mem_01",
      memberName: "Sunita Rathod",
      approvedUnits: 180,
      pieceRate: 32.0,
      grossEarnings: 5760.0,
      toolSupportDeduction: 0.0,
      netPayable: 5760.0,
      voted: true,
      voteDecision: "APPROVED",
      voteTimestamp: "2026-11-06 14:30"
    },
    {
      memberId: "mem_02",
      memberName: "Radhabai Hiremath",
      approvedUnits: 150,
      pieceRate: 32.0,
      grossEarnings: 4800.0,
      toolSupportDeduction: 0.0,
      netPayable: 4800.0,
      voted: true,
      voteDecision: "APPROVED",
      voteTimestamp: "2026-11-06 15:10"
    },
    {
      memberId: "mem_03",
      memberName: "Lakshmi Devamma",
      approvedUnits: 140,
      pieceRate: 32.0,
      grossEarnings: 4480.0,
      toolSupportDeduction: 0.0,
      netPayable: 4480.0,
      voted: true,
      voteDecision: "APPROVED",
      voteTimestamp: "2026-11-06 17:05"
    },
    {
      memberId: "mem_04",
      memberName: "Meenakshi Kulkarni",
      approvedUnits: 130,
      pieceRate: 32.0,
      grossEarnings: 4160.0,
      toolSupportDeduction: 0.0,
      netPayable: 4160.0,
      voted: true,
      voteDecision: "APPROVED",
      voteTimestamp: "2026-11-07 10:20"
    },
    {
      memberId: "mem_05",
      memberName: "Anusuya Bai",
      approvedUnits: 0, // currently in progress for milestone 2
      pieceRate: 32.0,
      grossEarnings: 0.0,
      toolSupportDeduction: 0.0,
      netPayable: 0.0,
      voted: false,
      voteDecision: "PENDING",
      voteTimestamp: null
    }
  ]
};

export const DEMO_ANOMALY_ALERTS = [
  {
    id: "ANOM-2026-03",
    category: "DUPLICATE_INVOICE_WARNING",
    severity: "HIGH",
    title: "Possible Duplicate Yarn Invoice Detected",
    description: "Invoice #VWM-4091 from Venkateshwara Weaving Mills matches amount (₹14,400) and line items of Invoice #VWM-4078 submitted 10 days ago.",
    relatedTransaction: "PO-ORD-104-MAT-01",
    detectedDate: "2026-11-05",
    status: "UNDER_LEADER_INVESTIGATION",
    explanation: "AI Document Audit Flag: Check whether supplier billed the same 200m fabric roll consignment twice."
  },
  {
    id: "ANOM-2026-04",
    category: "QUANTITY_VARIATION",
    severity: "MEDIUM",
    title: "Material Consumption Discrepancy",
    description: "Cutting ledger logs 340m fabric used for 260 bags cut. Expected standard consumption is 312m (9.0% excess scrap).",
    relatedTransaction: "Cutting Batch #CB-04",
    detectedDate: "2026-11-06",
    status: "RESOLVED",
    explanation: "Leader Note: 28m fabric roll had a selvedge print defect from mill; scrap credit received from vendor."
  }
];

export const DEMO_RETAIL_PRODUCTS = [
  {
    id: "RET-PRD-101",
    name: "Handcrafted Pure Cotton Daily Market Bag",
    category: "Garments",
    price: 220.0,
    originalPrice: 280.0,
    rating: 4.9,
    reviewsCount: 38,
    shgName: "Pragati Mahila Sangha",
    location: "Channapatna",
    availableStock: 25,
    imageUrl: "https://images.unsplash.com/photo-1597484661643-2f5fef640dd1?auto=format&fit=crop&q=80&w=600",
    description: "Crafted by rural women artisans from Ramanagara using heavy duty unbleached cotton. Tested to hold up to 18kg with double-stitched reinforced straps.",
    features: ["100% Unbleached Cotton", "Washable & Reusable", "Inner zipper pocket", "Direct artisan benefit"]
  },
  {
    id: "RET-PRD-102",
    name: "Kasuti Hand-Embroidered Jute Table Runner",
    category: "Home decor",
    price: 480.0,
    originalPrice: 600.0,
    rating: 5.0,
    reviewsCount: 24,
    shgName: "Pragati Mahila Sangha",
    location: "Ijoor Cluster",
    availableStock: 2,
    imageUrl: "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&q=80&w=600",
    description: "Traditional Karnataka Kasuti needlework embroidery on pure golden natural jute. Elegant tribal motifs representing temple chariots.",
    features: ["Handcrafted Kasuti needlework", "Eco-friendly golden jute", "Heat resistant", "Size: 12x48 inches"]
  },
  {
    id: "RET-PRD-103",
    name: "Stone-Ground Curcumin Rich Turmeric Powder 500g",
    category: "Food products",
    price: 240.0,
    originalPrice: 290.0,
    rating: 4.8,
    reviewsCount: 52,
    shgName: "Sannidhi Farmers Mahila Group",
    location: "Kailancha",
    availableStock: 45,
    imageUrl: "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&q=80&w=600",
    description: "Farm-fresh Salem variety turmeric, organically grown without chemical pesticides and pulverized on low-speed stone chakki to retain natural volatile oils.",
    features: ["5.2% Certified Curcumin", "Low-temperature milled", "FSSAI verified", "No synthetic color"]
  },
  {
    id: "RET-PRD-104",
    name: "Channapatna Wooden Handcrafted Desk Organizer",
    category: "Handicrafts",
    price: 360.0,
    originalPrice: 450.0,
    rating: 4.7,
    reviewsCount: 19,
    shgName: "Kala Chaitanya SHG",
    location: "Channapatna Craft Town",
    availableStock: 18,
    imageUrl: "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&q=80&w=600",
    description: "Authentic GI-tagged Channapatna lacquerware crafted from sustainable ivory wood (Aale Mara) and dyed with non-toxic turmeric and vegetable colors.",
    features: ["GI Tagged Channapatna Toy Craft", "Natural organic vegetable dyes", "Smooth lacquer finish", "Eco friendly"]
  }
];

export const DEMO_AGENT_ACTIVITIES = [
  {
    id: "AGT-ACT-01",
    agentName: "Order Planning Agent",
    icon: "Calendar",
    timestamp: "10 mins ago",
    task: "Bulk Order Feasibility Analysis for ORD-2026-104",
    recommendation: "Dividing 1,200 units across 6 members with staggered 4-day milestones ensures on-time completion by Nov 18 (2 days before buyer deadline).",
    confidence: "95%",
    status: "COMPLETED",
    requiresHumanAction: false
  },
  {
    id: "AGT-ACT-02",
    agentName: "Work Allocation Agent",
    icon: "Users",
    timestamp: "45 mins ago",
    task: "Smart Fair Work Distribution for ORD-2026-112 (800 Turmeric Jars)",
    recommendation: "Allocate 400 jars to Shobha Manjunath (FSSAI lead) and 400 jars to Lakshmi Devamma based on past clean-room packaging scores.",
    confidence: "92%",
    status: "AWAITING_LEADER_APPROVAL",
    requiresHumanAction: true,
    actionLabel: "Review Allocation Proposal"
  },
  {
    id: "AGT-ACT-03",
    agentName: "Worker Completion Predictor",
    icon: "Activity",
    timestamp: "2 hours ago",
    task: "Progress Projection for Sunita Rathod (ORD-2026-104)",
    recommendation: "Sunita completed 180/220 units. Model predicts 100% completion of remaining 40 units in 2.5 work days (predicted date: Nov 09).",
    confidence: "94%",
    status: "INFORMATIVE",
    requiresHumanAction: false
  },
  {
    id: "AGT-ACT-04",
    agentName: "Quality Inspection Agent (CV)",
    icon: "CheckCircle",
    timestamp: "3 hours ago",
    task: "Batch QCB-2026-085 Image Analysis (35 units)",
    recommendation: "Flagged 6 units with inner zipper seam divergence (>3mm tolerance). Human re-inspection recommended.",
    confidence: "89.5%",
    status: "AWAITING_INSPECTOR_VERIFICATION",
    requiresHumanAction: true,
    actionLabel: "Examine Flagged Photos"
  },
  {
    id: "AGT-ACT-05",
    agentName: "Pricing Intelligence Agent",
    icon: "TrendingUp",
    timestamp: "Yesterday",
    task: "Wholesale Margin Benchmark Analysis",
    recommendation: "Current price ₹165/unit protects a net SHG reserve profit of ₹16,080. Recommended minimum bid for next reorder is ₹170.",
    confidence: "91%",
    status: "INFORMATIVE",
    requiresHumanAction: false
  },
  {
    id: "AGT-ACT-06",
    agentName: "Financial Transparency Agent",
    icon: "ShieldAlert",
    timestamp: "Yesterday",
    task: "Invoice Deduplication & Ledger Cross-check",
    recommendation: "Flagged potential duplicate invoice #VWM-4091 from raw cotton supplier. Hold payment until verified.",
    confidence: "97%",
    status: "ACTION_REQUIRED",
    requiresHumanAction: true,
    actionLabel: "Investigate Invoice"
  },
  {
    id: "AGT-ACT-07",
    agentName: "Retail Demand Agent",
    icon: "ShoppingBag",
    timestamp: "2 days ago",
    task: "Festival Season Demand Forecast",
    recommendation: "Expect 40% surge in Kasuti Table Runners for upcoming Deepavali fairs. Recommend reserving 50m extra jute stock.",
    confidence: "88%",
    status: "INFORMATIVE",
    requiresHumanAction: false
  },
  {
    id: "AGT-ACT-08",
    agentName: "Logistics Coordination Agent",
    icon: "Truck",
    timestamp: "2 days ago",
    task: "Consolidation Route Optimization",
    recommendation: "Consolidate dispatch of ORD-104 (Peenya) with nearby Channapatna woodcraft batch to save ₹450 on truck freight.",
    confidence: "93%",
    status: "COMPLETED",
    requiresHumanAction: false
  }
];

export const DEMO_KNOWLEDGE_DOCS = [
  {
    id: "DOC-01",
    title: "NRLM Lakhpati Didi Guidelines 2026",
    category: "Government Schemes",
    summary: "Ministry of Rural Development policy framework supporting women SHG members to earn sustained annual income exceeding ₹1,00,000 through collective bulk enterprise.",
    excerpt: "Priority access to collateral-free revolving funds up to ₹20,000 per member, subsidized credit guarantee schemes for collective equipment purchase, and institutional market linkages."
  },
  {
    id: "DOC-02",
    title: "Export Quality Standards for Garments & Tote Bags",
    category: "Technical SOP",
    summary: "Standard Operating Procedure for double-needle chain stitching, handle tension testing (>15kg weight load), and eco-friendly dye retention standards.",
    excerpt: "All bulk orders must undergo 100% seam integrity check and needle detector scan. Handles must feature reinforced boxed-cross (X) box stitching."
  },
  {
    id: "DOC-03",
    title: "SHG Group Payout By-laws & Quorum Rules",
    category: "Internal Governance",
    summary: "Transparent disbursement protocol requiring minimum 60% affirmative quorum among active members before bank transfer authorization.",
    excerpt: "No single leader or office-bearer may authorize member labor payments without written or digital quorum log verified during weekly meetings."
  }
];

export const DEMO_NOTIFICATIONS = [
  {
    id: "notif-01",
    title: "New Bulk Order Received",
    message: "Arogya Wellness Organics placed an inquiry for 800 Turmeric Jars (₹1,56,000).",
    time: "20 mins ago",
    type: "order",
    read: false
  },
  {
    id: "notif-02",
    title: "Quality Inspection Flagged",
    message: "Batch QCB-2026-085 (Meenakshi K.) has 6 units needing zipper seam rework.",
    time: "2 hours ago",
    type: "quality",
    read: false
  },
  {
    id: "notif-03",
    title: "Payout Approval Quorum Pending",
    message: "ORD-2026-104 Milestone 1 needs 1 more vote to reach required 5-member quorum.",
    time: "4 hours ago",
    type: "payout",
    read: false
  },
  {
    id: "notif-04",
    title: "Shipment Dispatched",
    message: "Batch of 500 Tote Bags picked up by VRL Logistics for EcoFab Bangalore.",
    time: "1 day ago",
    type: "logistics",
    read: true
  }
];

