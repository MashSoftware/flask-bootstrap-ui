// initialize Leaflet
var map = L.map("mapid");

// add the OpenStreetMap tiles
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>',
}).addTo(map);

// add popup to each feature
function onEachFeature(feature, layer) {
  if (feature.properties && feature.properties.name) {
    layer.bindPopup(feature.properties.name);
  }
}

// add the GeoJSON feature layer
var geojsonLayer = L.geoJSON(geojson, { onEachFeature: onEachFeature }).addTo(
  map
);

// zoom map to GeoJSON feature layer
map.fitBounds(geojsonLayer.getBounds());
