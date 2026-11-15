import React from 'react';
import './Card.css';

const Card = ({ title, children, className = '' }) => (
  <div className={`card ${className}`}>
    {title && <h3 className="card__title">{title}</h3>}
    <div className="card__body">{children}</div>
  </div>
);

export default Card;

