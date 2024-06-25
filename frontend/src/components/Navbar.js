import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Navbar, NavbarBrand, NavbarToggler, Collapse, Nav, NavItem, NavLink, Button } from 'reactstrap';
import '../Navbar.css';

const AppNavbar = () => {
  const navigate = useNavigate();
  const isAuthenticated = !!localStorage.getItem('token');
  const [isOpen, setIsOpen] = useState(false);

  const toggle = () => setIsOpen(!isOpen);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <Navbar color="light" light expand="md">
      <NavbarBrand tag={Link} to="/">Dashboard</NavbarBrand>
      <NavbarToggler onClick={toggle} />
      <Collapse isOpen={isOpen} navbar>
        <Nav className="ms-auto" navbar>
          {isAuthenticated && (
            <>
              <NavItem>
                <NavLink tag={Link} to="/emissionHistory">Emission History</NavLink>
              </NavItem>
              <NavItem>
                <NavLink tag={Link} to="/expenses">Expenses</NavLink>
              </NavItem>
              <NavItem>
                <Button color="link" onClick={handleLogout}>Logout</Button>
              </NavItem>
            </>
          )}
        </Nav>
      </Collapse>
    </Navbar>
  );
};

export default AppNavbar;
