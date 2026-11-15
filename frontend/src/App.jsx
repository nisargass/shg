import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';

// Layouts
import PublicLayout from './layouts/PublicLayout';
import LeaderLayout from './layouts/LeaderLayout';
import MemberLayout from './layouts/MemberLayout';
import BuyerLayout from './layouts/BuyerLayout';
import FederationLayout from './layouts/FederationLayout';

// Public Pages
import LandingPage from './pages/landing/LandingPage';
import LoginPage from './pages/auth/LoginPage';
import MarketplacePage from './pages/marketplace/MarketplacePage';
import CartPage from './pages/marketplace/CartPage';

// Leader Portal Pages
import LeaderDashboard from './pages/leader/Dashboard';
import OrdersPage from './pages/leader/OrdersPage';
import AllocationPage from './pages/leader/AllocationPage';
import ProductionPage from './pages/leader/ProductionPage';
import QualityPage from './pages/leader/QualityPage';
import PricingPage from './pages/leader/PricingPage';
import InventoryPage from './pages/leader/InventoryPage';
import SuppliersPage from './pages/leader/SuppliersPage';
import LogisticsPage from './pages/leader/LogisticsPage';
import MembersPage from './pages/leader/MembersPage';
import FinancePage from './pages/leader/FinancePage';
import AnomaliesPage from './pages/leader/AnomaliesPage';
import RetailManagementPage from './pages/leader/RetailManagementPage';
import AgentInsightsPage from './pages/leader/AgentInsightsPage';
import ReportsPage from './pages/leader/ReportsPage';
import SettingsPage from './pages/leader/SettingsPage';

// Member Portal Pages
import MemberDashboard from './pages/member/Dashboard';
import MemberTasksPage from './pages/member/MemberTasksPage';
import MemberProductionPage from './pages/member/MemberProductionPage';
import MemberQualityPage from './pages/member/MemberQualityPage';
import MemberEarningsPage from './pages/member/MemberEarningsPage';
import MemberPaymentsPage from './pages/member/MemberPaymentsPage';
import VoiceAssistantPage from './pages/member/VoiceAssistantPage';
import MemberHelpPage from './pages/member/MemberHelpPage';

// Buyer Portal Pages
import BuyerDashboard from './pages/buyer/BuyerDashboard';
import BuyerCreateOrderPage from './pages/buyer/BuyerCreateOrderPage';
import BuyerOrdersPage from './pages/buyer/BuyerOrdersPage';
import BuyerCatalogPage from './pages/buyer/BuyerCatalogPage';

// Federation Portal Pages
import FederationDashboard from './pages/federation/FederationDashboard';
import FederationShgsPage from './pages/federation/FederationShgsPage';
import FederationProductionPage from './pages/federation/FederationProductionPage';
import FederationReportsPage from './pages/federation/FederationReportsPage';

const RequireAuth = ({ children, allowedRoles }) => {
  const { user } = useAuth();
  const isDemoMode = import.meta.env.DEV;
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return isDemoMode ? children : <Navigate to="/" replace />;
  }
  return children;
};

const AppRoutes = () => {
  return (
    <Routes>
      {/* Public Pages */}
      <Route element={<PublicLayout />}>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/about" element={<MemberHelpPage />} />
        <Route path="/marketplace" element={<MarketplacePage />} />
        <Route path="/marketplace/cart" element={<CartPage />} />
      </Route>

      {/* SHG Leader Portal */}
      <Route
        path="/leader"
        element={
          <RequireAuth allowedRoles={['SHG_LEADER']}>
            <LeaderLayout />
          </RequireAuth>
        }
      >
        <Route index element={<LeaderDashboard />} />
        <Route path="orders" element={<OrdersPage />} />
        <Route path="allocation" element={<AllocationPage />} />
        <Route path="production" element={<ProductionPage />} />
        <Route path="quality" element={<QualityPage />} />
        <Route path="pricing" element={<PricingPage />} />
        <Route path="inventory" element={<InventoryPage />} />
        <Route path="suppliers" element={<SuppliersPage />} />
        <Route path="logistics" element={<LogisticsPage />} />
        <Route path="members" element={<MembersPage />} />
        <Route path="finance" element={<FinancePage />} />
        <Route path="anomalies" element={<AnomaliesPage />} />
        <Route path="retail" element={<RetailManagementPage />} />
        <Route path="ai" element={<AgentInsightsPage />} />
        <Route path="reports" element={<ReportsPage />} />
        <Route path="settings" element={<SettingsPage />} />
      </Route>

      {/* SHG Member Portal */}
      <Route
        path="/member"
        element={
          <RequireAuth allowedRoles={['SHG_MEMBER']}>
            <MemberLayout />
          </RequireAuth>
        }
      >
        <Route index element={<MemberDashboard />} />
        <Route path="tasks" element={<MemberTasksPage />} />
        <Route path="production" element={<MemberProductionPage />} />
        <Route path="quality" element={<MemberQualityPage />} />
        <Route path="earnings" element={<MemberEarningsPage />} />
        <Route path="payments" element={<MemberPaymentsPage />} />
        <Route path="assistant" element={<VoiceAssistantPage />} />
        <Route path="help" element={<MemberHelpPage />} />
      </Route>

      {/* Wholesale Buyer Portal */}
      <Route
        path="/buyer"
        element={
          <RequireAuth allowedRoles={['BUYER']}>
            <BuyerLayout />
          </RequireAuth>
        }
      >
        <Route index element={<BuyerDashboard />} />
        <Route path="create" element={<BuyerCreateOrderPage />} />
        <Route path="orders" element={<BuyerOrdersPage />} />
        <Route path="catalog" element={<BuyerCatalogPage />} />
      </Route>

      {/* Federation Officer Portal */}
      <Route
        path="/federation"
        element={
          <RequireAuth allowedRoles={['FEDERATION_OFFICER']}>
            <FederationLayout />
          </RequireAuth>
        }
      >
        <Route index element={<FederationDashboard />} />
        <Route path="shgs" element={<FederationShgsPage />} />
        <Route path="production" element={<FederationProductionPage />} />
        <Route path="reports" element={<FederationReportsPage />} />
      </Route>

      {/* Catch-all redirect to Landing */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
};

export default App;
