import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from '../components/common/Navbar';
import Sidebar from '../components/common/Sidebar';

const FederationLayout = () => {
  return (
    <div className="app-container">
      <Navbar />
      <div className="portal-layout">
        <Sidebar role="federation" />
        <main className="portal-main">
          <div className="portal-content">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default FederationLayout;
