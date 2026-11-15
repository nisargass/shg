import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import {
  ShoppingCart,
  Trash2,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  Store
} from 'lucide-react';
import { retailApi } from '../../api/services';

const CartPage = () => {
  const { cart, removeFromCart, clearCart } = useAuth();
  const navigate = useNavigate();
  const [checkingOut, setCheckingOut] = useState(false);
  const [orderConfirmed, setOrderConfirmed] = useState(null);

  const subtotal = cart.reduce((acc, item) => acc + item.price * item.quantity, 0);
  const shipping = subtotal > 500 || subtotal === 0 ? 0 : 50;
  const total = subtotal + shipping;

  const handleCheckout = async (e) => {
    e.preventDefault();
    setCheckingOut(true);
    const orderRes = await retailApi.placeRetailOrder({
      items: cart,
      totalAmount: total,
      shippingAddress: 'Direct Courier Delivery'
    });
    setCheckingOut(false);
    setOrderConfirmed(orderRes);
    clearCart();
  };

  return (
    <div style={{ maxWidth: '1080px', margin: '0 auto', padding: '30px 24px' }}>
      <div className="page-header">
        <div>
          <h1 className="page-title">Artisan Retail Shopping Cart</h1>
          <p className="page-subtitle">Supporting rural women entrepreneurs directly</p>
        </div>
      </div>

      {orderConfirmed ? (
        <div className="card" style={{ textAlign: 'center', padding: '40px 24px', maxWidth: '600px', margin: '0 auto' }}>
          <div style={{ width: '56px', height: '56px', borderRadius: '50%', background: '#e8f5e9', color: '#2e7d32', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 16px' }}>
            <CheckCircle2 size={32} />
          </div>
          <h2 style={{ fontSize: '22px', color: '#123B5D', marginBottom: '8px' }}>Thank You for Your Order!</h2>
          <p style={{ fontSize: '14px', color: '#5e7386', marginBottom: '16px' }}>
            Order <strong>{orderConfirmed.orderId}</strong> has been confirmed. The artisan group has received your order and will dispatch your package within {orderConfirmed.estimatedDelivery}.
          </p>
          <div style={{ background: '#F8FAFC', padding: '16px', borderRadius: '8px', border: '1px solid #EEF2F5', marginBottom: '24px', fontSize: '13px', textAlign: 'left' }}>
            <div>Total Paid: <strong>₹{orderConfirmed.totalAmount.toLocaleString()}</strong></div>
            <div style={{ color: '#168B80', marginTop: '4px' }}>&bull; 100% credited to Pragati Mahila Sangha collective fund.</div>
          </div>
          <Link to="/marketplace" className="btn btn-primary">
            Continue Sourcing from Artisans
          </Link>
        </div>
      ) : cart.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '50px 20px' }}>
          <ShoppingCart size={48} color="#899ba8" style={{ margin: '0 auto 14px' }} />
          <h3 style={{ fontSize: '18px', color: '#123B5D', marginBottom: '6px' }}>Your shopping cart is currently empty</h3>
          <p style={{ fontSize: '13px', color: '#5e7386', marginBottom: '20px' }}>
            Explore unique handmade tote bags, Kasuti embroidery, and pure spices.
          </p>
          <Link to="/marketplace" className="btn btn-secondary">
            <Store size={16} /> Browse Artisan Marketplace
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-12" style={{ gap: '24px' }}>
          {/* Cart items */}
          <div style={{ gridColumn: 'span 8' }}>
            <div className="card" style={{ padding: 0 }}>
              <div style={{ padding: '16px 20px', borderBottom: '1px solid #EEF2F5' }}>
                <strong style={{ fontSize: '14px', color: '#123B5D' }}>Cart Items ({cart.length})</strong>
              </div>
              <div>
                {cart.map((item) => (
                  <div key={item.id} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '16px 20px', borderBottom: '1px solid #EEF2F5', gap: '16px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                      <img src={item.imageUrl} alt={item.name} style={{ width: '60px', height: '60px', borderRadius: '8px', objectFit: 'cover' }} />
                      <div>
                        <strong style={{ fontSize: '14px', color: '#123B5D' }}>{item.name}</strong>
                        <div style={{ fontSize: '12px', color: '#5e7386' }}>By {item.shgName} &bull; Qty: {item.quantity}</div>
                        <div style={{ fontSize: '13.5px', fontWeight: '700', color: '#168B80', marginTop: '2px' }}>₹{item.price} each</div>
                      </div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontSize: '15px', fontWeight: '800', color: '#123B5D', marginBottom: '6px' }}>
                        ₹{(item.price * item.quantity).toFixed(2)}
                      </div>
                      <button className="btn btn-sm btn-outline" onClick={() => removeFromCart(item.id)} style={{ color: '#C83D43', borderColor: '#f5c6cb' }}>
                        <Trash2 size={13} /> Remove
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Order Summary */}
          <div style={{ gridColumn: 'span 4' }}>
            <div className="card">
              <h3 style={{ fontSize: '16px', color: '#123B5D', marginBottom: '16px' }}>Order Summary</h3>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '8px' }}>
                <span style={{ color: '#5e7386' }}>Items Subtotal:</span>
                <strong>₹{subtotal.toFixed(2)}</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '8px' }}>
                <span style={{ color: '#5e7386' }}>Rural Courier Delivery:</span>
                <strong>{shipping === 0 ? 'FREE' : `₹${shipping}`}</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '17px', fontWeight: '800', color: '#123B5D', borderTop: '1px solid #DCE3E8', paddingTop: '12px', marginTop: '12px' }}>
                <span>Order Total:</span>
                <span style={{ color: '#168B80' }}>₹{total.toFixed(2)}</span>
              </div>

              <div style={{ background: '#F8FAFC', padding: '12px', borderRadius: '8px', border: '1px solid #EEF2F5', margin: '18px 0', fontSize: '11.5px', color: '#5e7386' }}>
                <ShieldCheck size={14} color="#168B80" style={{ marginBottom: '2px' }} />
                <span>Protected by SHG collective escrow. 100% of proceeds go directly to artisan compensation.</span>
              </div>

              <button className="btn btn-secondary btn-lg" style={{ width: '100%' }} onClick={handleCheckout} disabled={checkingOut}>
                {checkingOut ? 'Placing Order...' : 'Proceed to Checkout'} <ArrowRight size={16} />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CartPage;

