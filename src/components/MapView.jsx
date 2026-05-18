

import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

function MapView() {
  return (
    <MapContainer center={[40.4168, -3.7038]} zoom={6} style={{ height: '100vh', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />
      <Marker position={[40.4168, -3.7038]}>
        <Popup>Madrid — punto inicial del mapa</Popup>
      </Marker>
    </MapContainer>
  );
}

export default MapView;


