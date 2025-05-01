import axios from 'axios';

const BASE = "https://inspire.landregistry.gov.uk/inspire/ows";

export async function polygonAtPoint(lat, lon) {
  const params = {
    service: "WFS",
    version: "2.0.0",
    request: "GetFeature",
    typeNames: "INSPIRE_POLYGON",
    outputFormat: "application/json",
    srsName: "EPSG:4326",
    CQL_FILTER: `INTERSECTS(geom,POINT(${lon} ${lat}))`
  };

  try {
    const url = `${BASE}`;
    const response = await axios.get(url, { params });
    return response.data.features || []; // Return empty array if no features
  } catch (error) {
    console.error("Land Registry API error:", error);
    return []; // Return empty array on error
  }
} 