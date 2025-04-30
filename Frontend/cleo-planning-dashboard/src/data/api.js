/**
 * API service for fetching planning data
 */

// Use the Vite proxy to avoid CORS issues in development
const API_BASE = '/api';

/**
 * Fetch search results for the search dropdown
 * @param {string} query - The search query
 * @returns {Promise<Array>} - Array of search results
 */
export async function fetchSearchResults(query) {
  try {
    // Use the proxy instead of direct URL
    const response = await fetch(`/api/list/${query}`);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    // This endpoint returns a simple array of address strings
    const addresses = await response.json();
    
    // Convert to the format expected by the dropdown
    return addresses.map((address, index) => ({
      address: address,
      application_ref: `Search-${index}`,
      decision_date: new Date().toISOString(),
      type: 'application',
      decision_type: '',
      reason: 'Address search result'
    }));
  } catch (error) {
    console.error('Error fetching search results:', error);
    throw error;
  }
}

/**
 * Fetch planning applications for a specific address
 * @param {string} address - The address to search for
 * @returns {Promise<Array>} - Array of application records
 */
export async function fetchAddressRecords(address) {
  try {
    const response = await fetch(`${API_BASE}/address/${address}`);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching address records:', error);
    throw error;
  }
}

/**
 * Map API data to the format expected by the frontend
 * @param {Array} apiData - Data from the API
 * @returns {Array} - Transformed data for the frontend
 */
export function mapApiDataToRecords(apiData) {
  return apiData.map((item, index) => {
    // Convert API data format to the format expected by the frontend
    return {
      id: index + 1,
      applicationNumber: item.application_ref,
      decisionDate: item.decision_date,
      address: item.address,
      type: mapApiType(item.type),
      status: mapDecisionType(item.decision_type),
      description: item.reason,
      details: item.reason
    };
  });
}

/**
 * Map API type values to frontend display values
 */
function mapApiType(type) {
  const typeMap = {
    'application': 'Planning Application',
    'appeal': 'Appeal',
    'enforcement': 'Enforcement'
  };
  
  return typeMap[type] || type;
}

/**
 * Map API decision type values to frontend status values
 */
function mapDecisionType(decisionType) {
  const statusMap = {
    'approval': 'Approved',
    'refusal': 'Rejected',
    'appeal_allowed': 'Approved',
    'appeal_dismissed': 'Rejected',
    'enforcement_notice': 'Active',
    'enforcement_resolved': 'Resolved'
  };
  
  return statusMap[decisionType] || decisionType;
} 