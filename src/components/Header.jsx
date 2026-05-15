// src/components/Header.jsx
import './Header.css';

function Header() {
  return (
    <header className="header-container">
      <div className="header-content">
        <h1 className="header-title">Rastros del 36</h1>
        <p className="header-subtitle">
          Cartografía de la Guerra Civil y el exilio republicano.  
          Un archivo vivo de memoria, territorio y datos.
        </p>

        <div className="header-buttons">
          <a href="#map" className="btn primary">Explorar mapa</a>
          <a href="#dashboard" className="btn secondary">Ver análisis</a>
        </div>
      </div>
    </header>
  );
}

export default Header;

