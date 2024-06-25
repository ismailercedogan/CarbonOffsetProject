import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import fibabankaLogo from '../assets/fibabanka.png';  // Adjust the path as needed

const Navbar = () => {
  const navigate = useNavigate();
  const isAuthenticated = !!localStorage.getItem('token');

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">
          <img src={fibabankaLogo} alt="Fibabanka Logo" style={{ height: '60px', width: 'auto', marginRight: '20px',marginBottom:'10px' }} />
        </Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav">
            {isAuthenticated && (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/emissionHistory">Emission History</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/expenses">Expenses</Link>
                </li>
                <li className="nav-item">
                  <button className="btn btn-link nav-link" onClick={handleLogout}>Logout</button>
                </li>
              </>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
