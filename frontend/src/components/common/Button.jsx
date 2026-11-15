import React from 'react';
import './Button.css';

const Button = ({ children, onClick, type = 'button', variant = 'primary', disabled }) => (
  <button
    type={type}
    className={`btn btn--${variant}`}
    onClick={onClick}
    disabled={disabled}
  >
    {children}
  </button>
);

export default Button;

