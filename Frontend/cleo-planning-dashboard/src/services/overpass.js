import axios from 'axios';

export async function buildingOutline(lat, lon) {
  const query = `[out:json][timeout:25];
                 is_in(${lat},${lon})->.a;
                 way(pivot.a)[building];
                 out geom;`;
  
  try {
    const response = await axios.post(
      "https://overpass-api.de/api/interpreter",
      query
    );
    
    return response.data.elements || []; // Return empty array if no elements
  } catch (error) {
    console.error("OpenStreetMap API error:", error);
    return []; // Return empty array on error
  }
} 