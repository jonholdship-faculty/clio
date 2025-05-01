import { geocode } from './geocode';
import { polygonAtPoint } from './landRegistry';
import { buildingOutline } from './overpass';

// Generate a demo polygon around a point
function generateDemoPolygon(lat, lon) {
  // Create a simple 4-point polygon around the given coordinates
  // This simulates a property boundary for demo purposes
  const size = 0.001; // roughly 100m at most latitudes
  
  return {
    type: "Feature",
    geometry: {
      type: "Polygon",
      coordinates: [[
        [lon - size, lat - size],
        [lon + size, lat - size],
        [lon + size, lat + size],
        [lon - size, lat + size],
        [lon - size, lat - size] // Close the polygon
      ]]
    },
    properties: {
      id: "demo-property",
      address: "Demo Property"
    }
  };
}

export async function fetchBoundary(address) {
  try {
    // Step 1: Geocode the address
    const { lat, lon } = await geocode(address);
    console.log(`Successfully geocoded address to: ${lat}, ${lon}`);
    
    // Step 2: Try to find land registry parcel
    let features = await polygonAtPoint(lat, lon);
    let source = "HMLR";
    
    // Step 3: Fall back to OSM building outline if no parcel exists
    if (!features.length) {
      console.log("No HMLR data found, trying OpenStreetMap fallback");
      const osmData = await buildingOutline(lat, lon);
      
      if (osmData.length) {
        // Convert OSM data to GeoJSON format
        features = [{
          type: "Feature",
          geometry: {
            type: "Polygon",
            coordinates: [osmData[0].geometry.map(node => [node.lon, node.lat])]
          },
          properties: {}
        }];
      }
      source = "OSM";
    }
    
    // Step 4: Fall back to generated demo data if all else fails
    if (!features.length) {
      console.log("No property boundary found, generating demo data");
      features = [generateDemoPolygon(lat, lon)];
      source = "Demo";
    }
    
    // Step 5: Return the result
    return { 
      source,
      geojson: features[0],
      center: { lat, lon } 
    };
  } catch (error) {
    console.error("Error fetching boundary:", error);
    
    // If geocoding failed, use default London coordinates and a demo polygon
    const lat = 51.5074;
    const lon = -0.1278;
    
    return {
      source: "Demo",
      geojson: generateDemoPolygon(lat, lon),
      center: { lat, lon }
    };
  }
} 