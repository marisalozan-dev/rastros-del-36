import './styles/layout.css';
import Header from './components/Header';
import MapView from './components/MapView';
import Dashboard from './components/Dashboard';
import StoryPanel from './components/StoryPanel';
import Footer from './components/Footer';

function App() {
  return (
    <div className="app-root">
      <Header />
      <main className="app-main">
        <section className="map-section">
          <MapView />
        </section>
        <section className="board-section">
          <Dashboard />
          <StoryPanel />
        </section>
      </main>
      <Footer />
    </div>
  );
}

export default App;
