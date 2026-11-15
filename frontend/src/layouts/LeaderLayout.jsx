import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from '../components/common/Navbar';
import Sidebar from '../components/common/Sidebar';

const LeaderLayout = () => {
  return (
    <div className="app-container">
      <Navbar />
      <div className="portal-layout">
        <Sidebar role="leader" />
        <main className="portal-main">
          <div className="portal-content">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default LeaderLayout;
