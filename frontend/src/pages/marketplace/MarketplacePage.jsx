import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Store,
  Search,
  ShoppingCart,
  Star,
  ShieldCheck,
  Check,
  ArrowRight
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { DEMO_RETAIL_PRODUCTS } from '../../mock/mockData';

const MarketplacePage = () => {
  const { addToCart } = useAuth();
  const [products] = useState(DEMO_RETAIL_PRODUCTS);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [addedNotice, setAddedNotice] = useState('');

  const categories = ['ALL', 'Garments', 'Home decor', 'Food products', 'Handicrafts'];

  const filtered = products.filter((p) => {
    const matchesCat = selectedCategory === 'ALL' || p.category.toLowerCase() === selectedCategory.toLowerCase();
    const matchesSearch = p.name.toLowerCase().includes(searchTerm.toLowerCase()) || p.description.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCat && matchesSearch;
  });

  const handleAddToCart = (product) => {
    addToCart(product);
    setAddedNotice(`"${product.name}" added to cart!`);
    setTimeout(() => setAddedNotice(''), 3000);
  };

  return (
    <div style={{ maxWidth: '1440px', margin: '0 auto', padding: '30px 24px' }}>
      {/* Marketplace Header */}
      <div style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto 36px' }}>
        <span className="badge badge-secondary" style={{ marginBottom: '8px' }}>
          Direct Rural Artisan Storefront
        </span>
        <h1 style={{ fontSize: '36px', color: '#123B5D', fontWeight: '800' }}>
          Authentic Handcrafted Products by Women's SHGs
        </h1>
        <p style={{ fontSize: '15px', color: '#5e7386', marginTop: '8px' }}>
          100% direct artisan benefit &bull; Zero middleman markups &bull; Fair rural piece-rate compensation
        </p>
      </div>

      {addedNotice && (
        <div className="alert-banner success" style={{ maxWidth: '600px', margin: '0 auto 24px', textAlign: 'center' }}>
          <Check size={18} />
          <span>{addedNotice}</span>
          <Link to="/marketplace/cart" style={{ marginLeft: '12px', fontWeight: '700', textDecoration: 'underline' }}>
            View Cart & Checkout
          </Link>
        </div>
      )}

      {/* Filter and Search Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px', marginBottom: '30px' }}>
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          {categories.map((cat) => (
            <button
              key={cat}
              className={`btn btn-sm ${selectedCategory === cat ? 'btn-primary' : 'btn-outline'}`}
              onClick={() => setSelectedCategory(cat)}
            >
              {cat === 'ALL' ? 'All Products' : cat}
            </button>
          ))}
        </div>

        <div style={{ position: 'relative', width: '280px' }}>
          <input
            type="text"
            className="form-control"
            placeholder="Search handcrafted crafts..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{ paddingLeft: '36px' }}
          />
          <Search size={16} color="#899ba8" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
        </div>
      </div>

      {/* Product Grid */}
      <div className="grid grid-cols-4" style={{ gap: '24px' }}>
        {filtered.map((prod) => (
          <div key={prod.id} className="card" style={{ padding: 0, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
            <div style={{ height: '220px', overflow: 'hidden', position: 'relative' }}>
              <img src={prod.imageUrl} alt={prod.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              <span style={{ position: 'absolute', top: '10px', left: '10px', background: 'rgba(18,59,93,0.85)', color: '#fff', fontSize: '11px', fontWeight: '600', padding: '3px 8px', borderRadius: '4px' }}>
                {prod.category}
              </span>
            </div>

            <div style={{ padding: '16px', flex: 1, display: 'flex', flexDirection: 'column' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                <span style={{ fontSize: '11.5px', color: '#168B80', fontWeight: '600' }}>
                  {prod.shgName}
                </span>
                <span style={{ fontSize: '12px', color: '#ab711b', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '2px' }}>
                  <Star size={13} fill="#E6A23C" color="#E6A23C" /> {prod.rating}
                </span>
              </div>

              <h3 style={{ fontSize: '15px', color: '#123B5D', marginBottom: '6px', lineHeight: '1.3' }}>
                {prod.name}
              </h3>

              <p style={{ fontSize: '12px', color: '#5e7386', marginBottom: '14px', lineHeight: '1.4', flex: 1 }}>
                {prod.description}
              </p>

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid #EEF2F5', paddingTop: '12px', marginTop: 'auto' }}>
                <div>
                  <div style={{ fontSize: '18px', fontWeight: '800', color: '#123B5D' }}>
                    ₹{prod.price}
                  </div>
                  <span style={{ fontSize: '11px', color: '#899ba8', textDecoration: 'line-through' }}>
                    ₹{prod.originalPrice}
                  </span>
                </div>

                <button
                  className="btn btn-secondary btn-sm"
                  onClick={() => handleAddToCart(prod)}
                >
                  <ShoppingCart size={15} /> Add to Cart
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MarketplacePage;

