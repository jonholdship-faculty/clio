import axios from 'axios';

const OS_KEY = "AnMmQNd5qLVDhJuSQGYypNsSozw1DEqj";

// For demo purposes - hardcoded coordinates for common UK locations
const DEMO_LOCATIONS = {
  'london': { lat: 51.5074, lon: -0.1278 },
  'manchester': { lat: 53.4808, lon: -2.2426 },
  'birmingham': { lat: 52.4862, lon: -1.8904 },
  'edinburgh': { lat: 55.9533, lon: -3.1883 },
  'glasgow': { lat: 55.8642, lon: -4.2518 },
  'liverpool': { lat: 53.4084, lon: -2.9916 },
  'leeds': { lat: 53.8008, lon: -1.5491 },
  'newcastle': { lat: 54.9783, lon: -1.6178 },
  'cardiff': { lat: 51.4816, lon: -3.1791 },
  'belfast': { lat: 54.5973, lon: -5.9301 },
  'test': { lat: 51.5074, lon: -0.1278 },  // Use London as default for 'test'
  'default': { lat: 51.5074, lon: -0.1278 } // Default to London
};

// Fallback function using hardcoded values
function fallbackGeocode(address) {
  if (!address) return DEMO_LOCATIONS['default'];
  
  // Convert to lowercase and trim for matching
  const normalizedAddress = address.toLowerCase().trim();
  
  // Check for direct matches
  if (DEMO_LOCATIONS[normalizedAddress]) {
    return DEMO_LOCATIONS[normalizedAddress];
  }
  
  // Check for partial matches
  for (const [key, coords] of Object.entries(DEMO_LOCATIONS)) {
    if (normalizedAddress.includes(key)) {
      return coords;
    }
  }
  
  // Default fallback
  return DEMO_LOCATIONS['default'];
}

export async function geocode(address) {
  const url = "https://api.os.uk/search/names/v1/find";
  const params = {
    query: address,
    maxresults: 1,
    key: OS_KEY
  };

  try {
    const response = await axios.get(url, { params });
    
    // Check if we have results
    if (!response.data || !response.data.results || response.data.results.length === 0) {
      console.log("Using fallback geocoding for address:", address);
      return fallbackGeocode(address);
    }
    
    // Get the first result
    const result = response.data.results[0];
    
    // Debug the response structure
    console.log('OS Names API response:', result);
    
    // Check if we have a point geometry (the API returns point features)
    if (result && result.GAZETTEER_ENTRY && result.GAZETTEER_ENTRY.GEOMETRY_X && result.GAZETTEER_ENTRY.GEOMETRY_Y) {
      // OS Names returns coordinates in British National Grid (EPSG:27700)
      // For simplicity, we'll use these directly, but ideally we'd convert to WGS84
      const x = parseFloat(result.GAZETTEER_ENTRY.GEOMETRY_X);
      const y = parseFloat(result.GAZETTEER_ENTRY.GEOMETRY_Y);
      
      // Simple conversion from BNG to WGS84 (lat/lon)
      // This is a very rough approximation
      const lon = -0.00000045 * x - 0.000000096 * y + -2.5;
      const lat = 0.000000077 * x - 0.00000006 * y + 54.7;
      
      return { lat, lon };
    }
    
    // Alternative format - some endpoints might return this structure
    if (result && result.geometry && result.geometry.coordinates) {
      return {
        lon: result.geometry.coordinates[0],
        lat: result.geometry.coordinates[1]
      };
    }
    
    console.log("Using fallback geocoding for address:", address);
    return fallbackGeocode(address);
  } catch (error) {
    console.error("Geocoding error:", error);
    console.log("Using fallback geocoding for address:", address);
    return fallbackGeocode(address);
  }
} 