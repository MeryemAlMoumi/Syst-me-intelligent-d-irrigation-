import React from 'react';
import { NavLink } from 'react-router-dom';
import { FaThLarge, FaSeedling, FaExclamationTriangle } from 'react-icons/fa'; // Icônes
import { MdWaterDrop } from 'react-icons/md'; // Icône pour le logo
import './Sidebar.css';

const Sidebar = () => {
  return (
    <div className="sidebar">
      {/* En-tête avec le Logo */}
      <div className="sidebar-header">
        <div className="logo-container">
          <MdWaterDrop className="logo-icon" />
          <div>
            <h2>AgroSmart</h2>
            <p>Irrigation intelligente</p>
          </div>
        </div>
      </div>

      {/* Menu de navigation */}
      <nav className="sidebar-nav">
        <ul>
          <li>
            <NavLink 
              to="/" 
              className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}
            >
              <FaThLarge className="icon" />
              <span>Tableau de bord</span>
            </NavLink>
          </li>

          <li>
            <NavLink 
              to="/irrigation" 
              className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}
            >
              <FaSeedling className="icon" />
              <span>Gestion de l'irrigation</span>
            </NavLink>
          </li>

          <li>
            <NavLink 
              to="/alertes" 
              className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}
            >
              <FaExclamationTriangle className="icon" />
              <span>Fuites et anomalies</span>
            </NavLink>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;