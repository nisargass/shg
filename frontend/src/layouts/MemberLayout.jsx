import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from '../components/common/Navbar';
import Sidebar from '../components/common/Sidebar';

const MemberLayout = () => {
  return (
    <div className="app-container">
      <Navbar />
      <div className="portal-layout">
        <Sidebar role="member" />
        <main className="portal-main">
          <div className="portal-content" style={{ maxWidth: '1080px' }}>
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default MemberLayout;
