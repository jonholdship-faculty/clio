<template>
  <div class="dashboard-container">
    <div class="container">
      <div class="dashboard-header animate-fade-in">
        <div class="address-header">
          <h1>Planning Records</h1>
          <div class="address-badge">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
            </svg>
            <span>{{ address }}</span>
          </div>
        </div>
        <button @click="goBack" class="btn btn-ghost back-button">
          <svg xmlns="http://www.w3.org/2000/svg" class="button-icon" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
          </svg>
          Back to Search
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-container animate-pulse">
        <svg xmlns="http://www.w3.org/2000/svg" class="loading-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <p>Loading planning data...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-container animate-fade-in">
        <svg xmlns="http://www.w3.org/2000/svg" class="error-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p>{{ error }}</p>
        <button @click="retryFetch" class="btn">Retry</button>
      </div>

      <!-- Content (only show when not loading) -->
      <template v-else>
        <!-- Summary and Map Section Row -->
        <div class="overview-map-row animate-slide-up">
          <!-- AI Overview Section - Take up 2/3 of width -->
          <div class="summary-card ai-overview">
            <div class="summary-header">
              <FeatherIcon name="cpu" class="summary-icon" color="white" size="md" />
              <h2>AI Overview</h2>
            </div>
            <div class="summary-content">
              <p>{{ aiSummaryText }}</p>
              
              <div class="indicators-row">
                <div class="indicator primary-indicator">
                  <span class="indicator-number">{{ recordStats.totalApplications }}</span>
                  <span class="indicator-label">Applications</span>
                </div>
                
                <div class="indicator success-indicator">
                  <span class="indicator-number">{{ recordStats.approvalRate }}%</span>
                  <span class="indicator-label">Approval Rate</span>
                </div>
                
                <div class="indicator warning-indicator">
                  <span class="indicator-number">{{ recordStats.successfulAppeals }}</span>
                  <span class="indicator-label">Successful Appeals</span>
                </div>
                
                <div class="indicator danger-indicator">
                  <span class="indicator-number">{{ recordStats.activeEnforcements }}</span>
                  <span class="indicator-label">Active Enforcements</span>
                </div>
                
                <div class="indicator danger-indicator">
                  <span class="indicator-number">{{ recordStats.rejected }}</span>
                  <span class="indicator-label">Rejected</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Map Component - Take up 1/3 of width -->
          <div class="map-section">
            <div class="map-container">
              <div class="map-header">
                <h2>Location</h2>
                <div class="map-address">{{ address }}</div>
                <div v-if="boundarySource" class="map-source">
                  <span>Source: {{ 
                    boundarySource === 'HMLR' ? 'HM Land Registry' : 
                    boundarySource === 'OSM' ? 'OpenStreetMap' :
                    'Demo Data'
                  }}</span>
                </div>
              </div>
              <div class="map-content">
                <div id="property-map" class="leaflet-map"></div>
                <div v-if="mapLoading" class="map-loading">
                  <svg xmlns="http://www.w3.org/2000/svg" class="loading-icon spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  <span>Loading property boundary...</span>
                </div>
                <div v-if="mapError" class="map-error">
                  <svg xmlns="http://www.w3.org/2000/svg" class="error-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>{{ mapError }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Records Table -->
        <div class="records-section card animate-fade-in">
          <div class="section-header">
            <h2>All Records</h2>
            <div class="table-actions">
              <button @click="toggleAllRows" class="expand-all-btn">
                <FeatherIcon 
                  :name="allExpanded ? 'minimize-2' : 'maximize-2'" 
                  size="sm" 
                  color="currentColor" 
                  strokeWidth="2"
                />
                <span>{{ allExpanded ? 'Collapse All' : 'Expand All' }}</span>
              </button>
              <div class="search-filter">
                <svg xmlns="http://www.w3.org/2000/svg" class="filter-icon" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                </svg>
                <input v-model="tableFilter" placeholder="Filter records..." class="filter-input" />
              </div>
            </div>
          </div>
          
          <div class="table-responsive">
            <table class="records-table">
              <thead>
                <tr>
                  <th @click="sortBy('decisionDate')" class="sortable-header">
                    Decision Date
                    <span v-if="sortField === 'decisionDate'" class="sort-indicator">
                      {{ sortOrder === 'asc' ? '↑' : '↓' }}
                    </span>
                  </th>
                  <th @click="sortBy('applicationNumber')" class="sortable-header">
                    Application Number
                    <span v-if="sortField === 'applicationNumber'" class="sort-indicator">
                      {{ sortOrder === 'asc' ? '↑' : '↓' }}
                    </span>
                  </th>
                  <th>Address</th>
                  <th @click="sortBy('status')" class="sortable-header">
                    Status
                    <span v-if="sortField === 'status'" class="sort-indicator">
                      {{ sortOrder === 'asc' ? '↑' : '↓' }}
                    </span>
                  </th>
                  <th @click="sortBy('type')" class="sortable-header">
                    Type
                    <span v-if="sortField === 'type'" class="sort-indicator">
                      {{ sortOrder === 'asc' ? '↑' : '↓' }}
                    </span>
                  </th>
                  <th>Details</th>
                </tr>
              </thead>
              <tbody>
                <template v-for="record in filteredRecords" :key="record.id">
                  <!-- Main data row -->
                  <tr class="record-row">
                    <td>{{ formatDate(record.decisionDate) }}</td>
                    <td class="app-number">{{ record.applicationNumber }}</td>
                    <td class="address-cell">{{ record.address }}</td>
                    <td>
                      <span :class="'status-badge ' + getStatusClass(record.status)">{{ record.status }}</span>
                    </td>
                    <td>
                      <span :class="'type-badge ' + getTypeClass(record.type)">{{ record.type }}</span>
                    </td>
                    <td class="actions-cell">
                      <button @click="showDetails(record)" class="btn-icon info-btn">
                        <svg xmlns="http://www.w3.org/2000/svg" class="details-icon" viewBox="0 0 20 20" fill="currentColor">
                          <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                          <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                        </svg>
                      </button>
                      <button @click="toggleRowExpansion(record.id)" class="btn-icon expand-btn">
                        <FeatherIcon 
                          :name="isRowExpanded(record.id) ? 'minus' : 'plus'" 
                          size="sm" 
                          color="white" 
                        />
                      </button>
                    </td>
                  </tr>
                  
                  <!-- AI Summary row (only visible when row is NOT expanded) -->
                  <tr v-if="!isRowExpanded(record.id)" class="summary-row">
                    <td colspan="6" class="summary-cell">
                      <div class="summary-container">
                        <p class="summary-text">
                          <FeatherIcon name="cpu" size="sm" class="ai-icon" />
                          <span class="ai-label">AI Summary:</span> {{ record.description }}
                        </p>
                      </div>
                    </td>
                  </tr>
                  
                  <!-- Timeline row (only visible when expanded) -->
                  <tr v-if="isRowExpanded(record.id)" class="expanded-row">
                    <td colspan="6" class="expanded-content">
                      <div class="expanded-grid">
                        <!-- Timeline Card -->
                        <div class="timeline-container">
                          <div class="timeline-header">
                            <FeatherIcon name="clock" size="sm" color="var(--primary)" />
                            <span>Application Timeline</span>
                          </div>
                          
                          <!-- Timeline items in a row format for better space utilization -->
                          <div class="timeline-items-container">
                            <!-- Submission -->
                            <div class="timeline-item">
                              <div class="vertical-timeline-marker">
                                <div class="vertical-marker-inner">
                                  <FeatherIcon name="edit-3" size="md" color="white" strokeWidth="2.5" />
                                </div>
                              </div>
                              <div class="vertical-timeline-content">
                                <div class="vertical-timeline-title">Application Submitted</div>
                                <div class="vertical-timeline-date">{{ formatDate(new Date(record.decisionDate).setMonth(new Date(record.decisionDate).getMonth() - 2)) }}</div>
                              </div>
                            </div>
                            
                            <!-- Review -->
                            <div class="timeline-item">
                              <div class="vertical-timeline-marker">
                                <div class="vertical-marker-inner">
                                  <FeatherIcon name="clipboard" size="md" color="white" strokeWidth="2.5" />
                                </div>
                              </div>
                              <div class="vertical-timeline-content">
                                <div class="vertical-timeline-title">Application Reviewed</div>
                                <div class="vertical-timeline-date">{{ formatDate(new Date(record.decisionDate).setMonth(new Date(record.decisionDate).getMonth() - 1)) }}</div>
                              </div>
                            </div>
                            
                            <!-- Decision -->
                            <div class="timeline-item">
                              <div class="vertical-timeline-marker" :class="'vertical-status-marker-' + getStatusClass(record.status)">
                                <div class="vertical-marker-inner">
                                  <FeatherIcon 
                                    :name="record.status === 'Approved' || record.status === 'Approved with Conditions' || record.status === 'Resolved' || record.status === 'Granted' ? 'check' : 
                                          record.status === 'Condition Discharged' ? 'check-circle' :
                                          record.status === 'Rejected' ? 'x' : 'alert-circle'" 
                                    size="md" 
                                    color="white" 
                                    strokeWidth="2.5" 
                                  />
                                </div>
                              </div>
                              <div class="vertical-timeline-content">
                                <div class="vertical-timeline-title">Decision: {{ record.status }}</div>
                                <div class="vertical-timeline-date">{{ formatDate(record.decisionDate) }}</div>
                              </div>
                            </div>
                          </div>
                        </div>
                        
                        <!-- AI Summary Card -->
                        <div class="ai-summary-container">
                          <div class="timeline-header">
                            <FeatherIcon name="cpu" size="sm" color="var(--primary)" />
                            <span>AI Summary</span>
                          </div>
                          <p class="ai-summary-text">{{ record.description }}</p>
                        </div>
                      </div>
                    </td>
                  </tr>
                </template>
                <tr v-if="filteredRecords.length === 0">
                  <td colspan="6" class="empty-state">
                    <div class="empty-container">
                      <svg xmlns="http://www.w3.org/2000/svg" class="empty-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <p>No records found matching your criteria</p>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>
    </div>

    <!-- Details Modal -->
    <transition name="modal">
      <div v-if="displayDialog" class="modal-overlay" @click="displayDialog = false">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <div class="modal-title">
              <h3>Planning Application Details</h3>
              <div class="modal-subtitle">
                <span class="modal-app-number">{{ selectedRecord?.applicationNumber }}</span>
                <span class="modal-separator">•</span>
                <span :class="'type-badge-small ' + getTypeClass(selectedRecord?.type)">{{ selectedRecord?.type }}</span>
              </div>
            </div>
            <button @click="displayDialog = false" class="modal-close">
              <FeatherIcon name="x" size="sm" color="var(--text-light)" />
            </button>
          </div>
          
          <div v-if="selectedRecord" class="modal-body">
            <div class="detail-grid">
              <!-- Left column - Application details and timeline -->
              <div class="detail-column">
                <div class="detail-section">
                  <h4 class="section-title">
                    <FeatherIcon name="map-pin" size="sm" color="var(--primary)" />
                    Location Information
                  </h4>
                  <div class="detail-group">
                    <div class="detail-label">Address</div>
                    <div class="detail-value address-value">{{ selectedRecord.address }}</div>
                  </div>
                  
                  <div class="detail-group">
                    <div class="detail-label">Reference</div>
                    <div class="detail-value mono">{{ selectedRecord.applicationNumber }}</div>
                  </div>
                  
                  <div class="detail-group">
                    <div class="detail-label">Type</div>
                    <div class="detail-value">
                      <span :class="'type-badge ' + getTypeClass(selectedRecord.type)">
                        {{ selectedRecord.type }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Timeline moved inside left column -->
                <div class="detail-section timeline-section">
                  <h4 class="section-title">
                    <FeatherIcon name="clock" size="sm" color="var(--primary)" />
                    Application Timeline
                  </h4>
                  <div class="modal-timeline">
                    <!-- Submission -->
                    <div class="vertical-timeline-item">
                      <div class="vertical-timeline-marker">
                        <div class="vertical-marker-inner">
                          <FeatherIcon name="edit-3" size="sm" color="white" />
                        </div>
                      </div>
                      <div class="vertical-timeline-content">
                        <div class="vertical-timeline-title">Application Submitted</div>
                        <div class="vertical-timeline-date">{{ formatDate(new Date(selectedRecord.decisionDate).setMonth(new Date(selectedRecord.decisionDate).getMonth() - 2)) }}</div>
                      </div>
                    </div>
                    
                    <!-- Review -->
                    <div class="vertical-timeline-item">
                      <div class="vertical-timeline-marker">
                        <div class="vertical-marker-inner">
                          <FeatherIcon name="clipboard" size="sm" color="white" />
                        </div>
                      </div>
                      <div class="vertical-timeline-content">
                        <div class="vertical-timeline-title">Application Reviewed</div>
                        <div class="vertical-timeline-date">{{ formatDate(new Date(selectedRecord.decisionDate).setMonth(new Date(selectedRecord.decisionDate).getMonth() - 1)) }}</div>
                      </div>
                    </div>
                    
                    <!-- Decision -->
                    <div class="vertical-timeline-item">
                      <div class="vertical-timeline-marker" :class="'vertical-status-marker-' + getStatusClass(selectedRecord.status)">
                        <div class="vertical-marker-inner">
                          <FeatherIcon 
                            :name="selectedRecord.status === 'Approved' || selectedRecord.status === 'Approved with Conditions' || selectedRecord.status === 'Resolved' || selectedRecord.status === 'Granted' ? 'check' : 
                                  selectedRecord.status === 'Condition Discharged' ? 'check-circle' :
                                  selectedRecord.status === 'Rejected' ? 'x' : 'alert-circle'" 
                            size="sm" 
                            color="white" 
                          />
                        </div>
                      </div>
                      <div class="vertical-timeline-content">
                        <div class="vertical-timeline-title">Decision: {{ selectedRecord.status }}</div>
                        <div class="vertical-timeline-date">{{ formatDate(selectedRecord.decisionDate) }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Right column - Status banner and AI Summary -->
              <div class="detail-column">
                <!-- Status banner moved here -->
                <div class="detail-section status-section">
                  <h4 class="section-title">
                    <FeatherIcon name="award" size="sm" color="var(--primary)" />
                    Decision Status
                  </h4>
                  <div class="status-banner" :class="'status-bg-' + getStatusClass(selectedRecord.status)">
                    <FeatherIcon 
                      :name="selectedRecord.status === 'Approved' || selectedRecord.status === 'Approved with Conditions' || selectedRecord.status === 'Resolved' || selectedRecord.status === 'Granted' ? 'check' : 
                            selectedRecord.status === 'Condition Discharged' ? 'check-circle' :
                            selectedRecord.status === 'Rejected' ? 'x' : 'alert-circle'" 
                      size="sm" 
                      :color="getStatusClass(selectedRecord.status) === 'status-success' ? '#059669' : 
                             getStatusClass(selectedRecord.status) === 'status-danger' ? '#DC2626' : 
                             getStatusClass(selectedRecord.status) === 'status-warning' ? '#D97706' : 
                             getStatusClass(selectedRecord.status) === 'status-info' ? '#2563EB' : '#4B5563'" 
                    />
                    <span class="status-text">{{ selectedRecord.status }}</span>
                  </div>
                </div>
                
                <!-- AI Summary remains in the right column -->
                <div class="detail-section description-section">
                  <h4 class="section-title">
                    <FeatherIcon name="cpu" size="sm" color="var(--primary)" />
                    AI Summary
                  </h4>
                  <p class="detail-description">{{ selectedRecord.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { fetchAddressRecords, mapApiDataToRecords } from "../data/api";
import { aiSummaries } from "../data/sampleData";
import FeatherIcon from "../components/FeatherIcon.vue";
import { fetchBoundary } from "../services/boundary";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

const router = useRouter();
const route = useRoute();

// State variables
const address = ref(route.query.address || "test");
const records = ref([]);
const loading = ref(true);
const error = ref(null);
const tableFilter = ref("");
const sortField = ref("decisionDate");
const sortOrder = ref("desc");
const displayDialog = ref(false);
const selectedRecord = ref(null);
const expandedRows = ref([]);
const allExpanded = ref(false);

// GeoJSON data for the site
const siteGeoJSON = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: {},
      geometry: {
        type: "LineString",
        coordinates: [
          [-1.5131759444203396, 52.43820266758567],
          [-1.5131759444203396, 52.437558897566674],
          [-1.5128938407395651, 52.43754976600931],
          [-1.512891344246981, 52.43748432312674],
          [-1.5126217230290138, 52.43748127926921],
          [-1.5126167300439306, 52.43754976600931],
          [-1.5120724946241353, 52.43754824408302],
          [-1.512069998131551, 52.43819962377779],
          [-1.5131734479277554, 52.43820418948934],
        ],
      },
    },
  ],
};

let geoJsonLayer = null;

// Map related state
const mapLoading = ref(false);
const mapError = ref(null);
const boundarySource = ref(null);
let map = null;
let boundaryLayer = null;

// Initialize and clean up the map
const initMap = async () => {
  if (map) return; // Map already initialized

  // Wait for the DOM to be ready
  await new Promise((resolve) => setTimeout(resolve, 100));

  const mapContainer = document.getElementById("property-map");
  if (!mapContainer) {
    console.error("Map container not found");
    return;
  }

  try {
    // Initialize the map with a default center and zoom level
    map = L.map("property-map").setView([52.438, -1.513], 16);

    // Add the OpenStreetMap tile layer
    L.tileLayer(
      "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      {
        attribution: "© OpenStreetMap contributors",
        maxZoom: 18,
      }
    ).addTo(map);

    // Add the GeoJSON layer for the boundary
    geoJsonLayer = L.geoJSON(siteGeoJSON, {
      style: {
        color: "#FF5500",
        weight: 3,
        opacity: 0.8,
      },
    }).addTo(map);

    // Fit the map to the GeoJSON bounds with padding
    map.fitBounds(geoJsonLayer.getBounds(), { padding: [50, 50] });
  } catch (error) {
    console.error("Error initializing map:", error);
    mapError.value = "Failed to initialize map.";
  } finally {
    mapLoading.value = false;
  }
};

const cleanupMap = () => {
  if (map) {
    map.remove();
    map = null;
  }
};

// Fetch and display the property boundary
const fetchPropertyBoundary = async () => {
  if (!address.value || !map) return;

  mapLoading.value = true;
  mapError.value = null;
  boundarySource.value = null;

  try {
    // Clear previous boundary if exists
    if (boundaryLayer) {
      map.removeLayer(boundaryLayer);
      boundaryLayer = null;
    }

    // Fetch the boundary
    const result = await fetchBoundary(address.value);
    boundarySource.value = result.source;

    // Add the boundary to the map
    boundaryLayer = L.geoJSON(result.geojson, {
      style: {
        color: "#FF5500",
        weight: 2,
        opacity: 0.8,
        fillColor: "#FF5500",
        fillOpacity: 0.2,
      },
    }).addTo(map);

    // Fit the map to the boundary
    map.fitBounds(boundaryLayer.getBounds(), { padding: [30, 30] });

    // Add a marker for the center
    L.marker([result.center.lat, result.center.lon]).addTo(map);
  } catch (err) {
    console.error("Error fetching property boundary:", err);
    mapError.value = `Failed to load property boundary: ${err.message}`;
  } finally {
    mapLoading.value = false;
  }
};

// Toggle row expansion
const toggleRowExpansion = (recordId) => {
  const index = expandedRows.value.indexOf(recordId);
  if (index === -1) {
    expandedRows.value.push(recordId);
  } else {
    expandedRows.value.splice(index, 1);
  }
  
  // Update allExpanded state based on whether all rows are now expanded
  allExpanded.value = expandedRows.value.length === records.value.length;
};

// Toggle all rows expansion
const toggleAllRows = () => {
  if (allExpanded.value) {
    // Collapse all rows
    expandedRows.value = [];
  } else {
    // Expand all rows
    expandedRows.value = records.value.map((record) => record.id);
  }
  allExpanded.value = !allExpanded.value;
};

// Check if a row is expanded
const isRowExpanded = (recordId) => {
  return expandedRows.value.includes(recordId);
};

// Get data from API on component mount
onMounted(async () => {
  try {
    loading.value = true;
    // Fetch data from API
    const apiData = await fetchAddressRecords(address.value);
    // Map API data to the format expected by the UI
    records.value = mapApiDataToRecords(apiData);
    loading.value = false;

    // Initialize the map after fetching records
    await initMap();
  } catch (err) {
    error.value = "Failed to load planning records. Please try again later.";
    loading.value = false;
    console.error("Error loading records:", err);
  }
});

onUnmounted(() => {
  cleanupMap();
});

// Filter, sort, and paginate data
const filteredRecords = computed(() => {
  if (!tableFilter.value) return records.value;
  
  const filter = tableFilter.value.toLowerCase();
  return records.value.filter(record => {
    return record.applicationNumber.toLowerCase().includes(filter) ||
           record.address.toLowerCase().includes(filter) ||
           record.type.toLowerCase().includes(filter) ||
           record.status.toLowerCase().includes(filter) ||
           record.description.toLowerCase().includes(filter);
  });
});

// Calculate statistics from records data
const recordStats = computed(() => {
  if (!records.value.length) {
    return {
      totalApplications: 0,
      approvalRate: 0,
      successfulAppeals: 0,
      activeEnforcements: 0,
      rejected: 0
    };
  }

  // Count applications by type
  const applications = records.value.filter(r => r.type === 'Planning Application').length;
  
  // Count approved applications
  const approved = records.value.filter(r => 
    (r.type === 'Planning Application' || r.type === 'Appeal') && 
    (r.status === 'Approved' || r.status === 'Approved with Conditions' || 
     r.status === 'Granted' || r.status === 'Condition Discharged' || 
     r.status === 'Resolved')
  ).length;
  
  // Calculate approval rate
  const totalDecided = records.value.filter(r => 
    (r.type === 'Planning Application' || r.type === 'Appeal') && 
    (r.status !== 'Pending')
  ).length;
  
  const approvalRate = totalDecided ? Math.round((approved / totalDecided) * 100) : 0;
  
  // Count successful appeals
  const successfulAppeals = records.value.filter(r => 
    r.type === 'Appeal' && 
    (r.status === 'Approved' || r.status === 'Approved with Conditions' || 
     r.status === 'Granted' || r.status === 'Condition Discharged')
  ).length;
  
  // Count active enforcements
  const activeEnforcements = records.value.filter(r => 
    r.type === 'Enforcement' && r.status === 'Active'
  ).length;
  
  // Count rejected applications
  const rejected = records.value.filter(r => 
    (r.type === 'Planning Application' || r.type === 'Appeal') && 
    r.status === 'Rejected'
  ).length;
  
  return {
    totalApplications: applications,
    approvalRate,
    successfulAppeals,
    activeEnforcements,
    rejected
  };
});

// Generate summary text based on records
const aiSummaryText = computed(() => {
  if (!records.value.length) {
    return "No planning data available for this address.";
  }
  
  const types = new Set(records.value.map(r => r.type));
  const hasMultipleTypes = types.size > 1;
  const hasEnforcements = records.value.some(r => r.type === 'Enforcement');
  const hasAppeals = records.value.some(r => r.type === 'Appeal');
  
  let summary = `This address has ${hasMultipleTypes ? 'a' : ''} ${hasMultipleTypes ? 'complex' : 'simple'} planning history`;
  
  if (hasMultipleTypes) {
    summary += " with multiple applications";
    if (hasEnforcements) summary += " and enforcement actions";
    summary += ".";
  } else {
    summary += ".";
  }
  
  if (records.value.length > 2) {
    summary += " There are several noteworthy trends in the planning history including ";
    
    if (hasMultipleTypes) {
      summary += "changes in application types over time";
      summary += " and varying decision outcomes.";
    } else {
      summary += "variations in decision outcomes over time.";
    }
  }
  
  return summary;
});

const sortedRecords = computed(() => {
  return [...filteredRecords.value].sort((a, b) => {
    let aValue = a[sortField.value];
    let bValue = b[sortField.value];
    
    // Special case for dates
    if (sortField.value === 'decisionDate') {
      aValue = new Date(aValue);
      bValue = new Date(bValue);
    }
    
    if (aValue < bValue) return sortOrder.value === 'asc' ? -1 : 1;
    if (aValue > bValue) return sortOrder.value === 'asc' ? 1 : -1;
    return 0;
  });
});

const showDetails = (record) => {
  selectedRecord.value = record;
  displayDialog.value = true;
};

const goBack = () => {
  router.push('/');
};

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

const getTypeClass = (type) => {
  if (!type) return 'type-default';
  
  // Normalize the type to uppercase for case-insensitive matching
  const normalizedType = type.toUpperCase();
  
  // Application types
  if (normalizedType.includes('ENFORCEMENT')) return 'type-danger';
  if (normalizedType.includes('APPEAL')) return 'type-warning';
  if (normalizedType.includes('PLANNING APPLICATION') || normalizedType.includes('FULL MAJOR')) return 'type-success';
  
  // Specialized application types
  if (normalizedType.includes('DISCHARGE OF CONDITION')) return 'type-purple';
  if (normalizedType.includes('NON-MATERIAL AMENDMENT') || normalizedType.includes('NMA')) return 'type-teal';
  if (normalizedType.includes('ADVERTISEMENT') || normalizedType.includes('ADV')) return 'type-indigo';
  
  // Default to blue if no specific type is matched
  return 'type-default';
};

const getStatusClass = (status) => {
  if (!status) return 'status-default';
  
  // Normalize the status to uppercase for case-insensitive matching
  const normalizedStatus = status.toUpperCase();
  
  // Success statuses (approved/granted)
  if (normalizedStatus.includes('APPROVED') || 
      normalizedStatus.includes('GRANTED') || 
      normalizedStatus.includes('RESOLVED') || 
      normalizedStatus.includes('CONDITION DISCHARGED')) {
    return 'status-success';
  }
  
  // Failure statuses (rejected)
  if (normalizedStatus.includes('REJECTED') || 
      normalizedStatus.includes('REFUSED') || 
      normalizedStatus.includes('DECLINED')) {
    return 'status-danger';
  }
  
  // Warning statuses (pending/in process)
  if (normalizedStatus.includes('PENDING') || 
      normalizedStatus.includes('OUTCOME PENDING') || 
      normalizedStatus.includes('AWAITING')) {
    return 'status-warning';
  }
  
  // Active/open statuses
  if (normalizedStatus.includes('ACTIVE') || 
      normalizedStatus.includes('OPEN') || 
      normalizedStatus.includes('IN PROGRESS')) {
    return 'status-info';
  }
  
  // Closed/withdrawn statuses
  if (normalizedStatus.includes('WITHDRAWN') || 
      normalizedStatus.includes('CLOSED') || 
      normalizedStatus.includes('SUPERSEDED')) {
    return 'status-secondary';
  }
  
  // Default to info if no specific status is matched
  return 'status-default';
};

const retryFetch = async () => {
  try {
    loading.value = true;
    error.value = null;
    // Fetch data from API
    const apiData = await fetchAddressRecords(address.value);
    // Map API data to the format expected by the UI
    records.value = mapApiDataToRecords(apiData);
    loading.value = false;
  } catch (err) {
    error.value = 'Failed to load planning records. Please try again later.';
    loading.value = false;
    console.error('Error retrying to load records:', err);
  }
};

// Sorting
const sortBy = (field) => {
  if (sortField.value === field) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortField.value = field;
    sortOrder.value = 'asc';
  }
};
</script>

<style scoped>
.dashboard-container {
  padding-bottom: var(--spacing-2xl);
  width: 100%;
}

.container {
  max-width: 100%;
  padding: 0 var(--spacing-2xl);
  width: 100%;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
}

.address-header {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.address-header h1 {
  color: var(--text);
  margin-bottom: var(--spacing-xs);
}

.address-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  background-color: var(--primary-light);
  color: white;
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--radius-xl);
  font-size: 0.9rem;
  font-weight: 500;
}

.address-badge .icon {
  width: 16px;
  height: 16px;
}

.back-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-weight: 500;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--border);
  background-color: white;
  box-shadow: var(--shadow-sm);
}

.back-button .button-icon {
  width: 20px;
  height: 20px;
}

:deep(body.govuk-theme) .back-button {
  font-family: "GDS Transport", arial, sans-serif;
  font-weight: 400;
  font-size: 16px;
  color: #005ea5;
  padding: 10px 15px;
  background: transparent;
  border: 0;
  box-shadow: none;
  position: relative;
  padding-left: 14px;
  text-decoration: underline;
}

:deep(body.govuk-theme) .back-button:before {
  content: "";
  display: block;
  position: absolute;
  top: 50%;
  left: 0;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 5px 6px 5px 0;
  border-color: transparent #005ea5 transparent transparent;
  margin-top: -5px;
}

:deep(body.govuk-theme) .back-button .button-icon {
  display: none;
}

/* Summary Cards */
.summary-sections {
  margin-bottom: var(--spacing-xl);
  width: 100%;
}

/* New Overview Map Row Layout */
.overview-map-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
  width: 100%;
  align-items: stretch; /* Ensures both cards stretch to same height */
}

.ai-overview {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.ai-overview .summary-content {
  flex: 1; /* Allow content to expand to fill space */
  display: flex;
  flex-direction: column;
}

.map-section {
  margin-bottom: 0; /* Override original margin */
  height: 100%;
  display: flex;
  flex-direction: column;
}

.summary-card {
  background-color: white;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition: transform var(--transition-normal), box-shadow var(--transition-normal);
  width: 100%;
}

.summary-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
}

.summary-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  background-color: var(--primary);
  color: white;
}

.summary-header h2 {
  margin: 0;
  font-size: 1.1rem;
  color: white;
}

.summary-icon {
  width: 24px;
  height: 24px;
}

.summary-content {
  padding: var(--spacing-lg);
}

.summary-content p {
  color: var(--text);
  margin-bottom: var(--spacing-lg);
  line-height: 1.6;
}

/* New Indicator Cards */
.indicators-row {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
  width: 100%;
}

.indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  background-color: white;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  flex: 1;
  text-align: center;
}

.indicator:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.primary-indicator {
  background-color: rgba(var(--primary-rgb), 0.1);
}

.success-indicator {
  background-color: rgba(16, 185, 129, 0.1);
}

.warning-indicator {
  background-color: rgba(245, 158, 11, 0.1);
}

.danger-indicator {
  background-color: rgba(239, 68, 68, 0.1);
}

.indicator-number {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: var(--spacing-sm);
  color: var(--primary);
}

.primary-indicator .indicator-number {
  color: var(--primary);
}

.success-indicator .indicator-number {
  color: var(--success);
}

.warning-indicator .indicator-number {
  color: var(--warning);
}

.danger-indicator .indicator-number {
  color: var(--danger);
}

.indicator-label {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text);
}

/* GOV.UK theme adjustments for indicators */
:deep(body.govuk-theme) .indicator {
  border-radius: 0;
  box-shadow: none;
  border: 1px solid #b1b4b6;
  border-left-width: 5px;
}

:deep(body.govuk-theme) .indicator:hover {
  transform: none;
  box-shadow: none;
}

:deep(body.govuk-theme) .primary-indicator {
  border-left-color: #1d70b8;
}

:deep(body.govuk-theme) .success-indicator {
  border-left-color: #00703c;
}

:deep(body.govuk-theme) .warning-indicator {
  border-left-color: #f47738;
}

:deep(body.govuk-theme) .danger-indicator {
  border-left-color: #d4351c;
}

:deep(body.govuk-theme) .indicator-number {
  border-radius: 0;
}

:deep(body.govuk-theme) .indicator-label {
  font-family: "GDS Transport", arial, sans-serif;
  font-weight: 700;
  font-size: 16px;
}

/* Specific GOV.UK styling for summary cards */
:deep(body.govuk-theme) .summary-sections {
  display: block;
}

:deep(body.govuk-theme) .summary-card {
  flex: 1;
  min-width: 0;
  border-radius: 0;
  box-shadow: none;
  border: 1px solid #b1b4b6;
}

:deep(body.govuk-theme) .summary-card:hover {
  transform: none;
  box-shadow: none;
}

:deep(body.govuk-theme) .summary-header {
  background-color: #1d70b8;
  color: #ffffff;
  padding: 15px;
  border-bottom: 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

:deep(body.govuk-theme) .summary-header h2 {
  color: #ffffff;
  font-size: 19px;
  font-weight: 700;
  margin: 0;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
}

:deep(body.govuk-theme) .summary-content {
  padding: 15px;
}

:deep(body.govuk-theme) .summary-content p {
  font-size: 16px;
  line-height: 1.5;
  margin-bottom: 20px;
}

:deep(body.govuk-theme) .summary-icon {
  color: white;
  width: 22px;
  height: 22px;
}

/* Records Section */
.records-section {
  padding: var(--spacing-lg);
  background-color: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  width: 100%;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border);
}

.section-header h2 {
  margin: 0;
  color: var(--text);
  font-size: 1.25rem;
}

.table-actions {
  display: flex;
  gap: var(--spacing-md);
}

.search-filter {
  position: relative;
}

.filter-icon {
  position: absolute;
  left: var(--spacing-sm);
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-light);
  width: 16px;
  height: 16px;
}

.filter-input {
  padding: var(--spacing-sm) var(--spacing-sm) var(--spacing-sm) var(--spacing-xl);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  width: 250px;
  font-size: 0.9rem;
}

.table-responsive {
  overflow-x: auto;
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-lg);
}

.records-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.95rem;
}

.records-table th {
  background-color: var(--background);
  padding: var(--spacing-md);
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
}

.sortable-header {
  cursor: pointer;
  position: relative;
  padding-right: var(--spacing-xl) !important;
}

.sort-indicator {
  position: absolute;
  right: var(--spacing-md);
  color: var(--primary);
}

.records-table td {
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
}

.app-number {
  font-family: monospace;
  font-weight: 600;
  color: var(--primary);
}

.address-cell {
  max-width: 250px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.record-row {
  transition: background-color var(--transition-fast);
}

.record-row:hover {
  background-color: rgba(59, 130, 246, 0.05);
}

.type-badge, .status-badge {
  display: inline-block;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: uppercase;
}

.type-danger {
  background-color: #FEE2E2;
  color: #DC2626;
}

.type-warning {
  background-color: #FEF3C7;
  color: #D97706;
}

.type-success {
  background-color: #D1FAE5;
  color: #059669;
}

.type-purple {
  background-color: #EDE9FE;
  color: #7C3AED;
}

.type-teal {
  background-color: #CCFBF1;
  color: #0D9488;
}

.type-indigo {
  background-color: #E0E7FF;
  color: #4F46E5;
}

.type-default {
  background-color: #E4E4E7;
  color: #3F3F46;
}

.status-success {
  background-color: #D1FAE5;
  color: #059669;
}

.status-danger {
  background-color: #FEE2E2;
  color: #DC2626;
}

.status-warning {
  background-color: #FEF3C7;
  color: #D97706;
}

.status-info {
  background-color: #DBEAFE;
  color: #2563EB;
}

.status-secondary {
  background-color: #F3F4F6;
  color: #4B5563;
}

.status-default {
  background-color: #E4E4E7;
  color: #3F3F46;
}

.btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: var(--primary-light);
  color: white;
  cursor: pointer;
  transition: background-color var(--transition-normal);
}

.btn-icon:hover {
  background-color: var(--primary);
}

.details-icon {
  width: 16px;
  height: 16px;
}

.empty-state {
  text-align: center;
  padding: var(--spacing-xl) !important;
}

.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
  color: var(--text-light);
}

.empty-icon {
  width: 48px;
  height: 48px;
  color: var(--text-light);
  opacity: 0.5;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: var(--spacing-md);
  backdrop-filter: blur(3px);
}

.modal-content {
  background-color: white;
  border-radius: var(--radius-lg);
  width: 100%;
  max-width: 1100px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-xl);
  animation: modal-in 0.3s ease-out;
}

@keyframes modal-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border);
  background-color: var(--background);
}

.modal-title {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.modal-title h3 {
  margin: 0;
  color: var(--primary);
  font-size: 1.3rem;
  font-weight: 600;
}

.modal-subtitle {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.modal-app-number {
  font-family: monospace;
  color: var(--text);
  font-size: 0.9rem;
  font-weight: 500;
}

.modal-separator {
  color: var(--text-light);
  font-size: 0.9rem;
}

.modal-close {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: var(--spacing-xs);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.modal-close:hover {
  background-color: var(--background-darker);
}

.modal-body {
  padding: var(--spacing-lg);
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
}

.detail-column {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.detail-section {
  background-color: var(--background);
  border-radius: var(--radius-md);
  padding: var(--spacing-md) var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid rgba(var(--primary-rgb), 0.1);
}

.section-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  color: var(--primary);
  margin: 0 0 var(--spacing-md) 0;
  padding-bottom: var(--spacing-sm);
  border-bottom: 1px solid var(--border);
  font-size: 1.1rem;
  font-weight: 600;
}

.detail-group {
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-sm);
  border-bottom: 1px solid var(--border-light);
}

.detail-group:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.detail-label {
  color: var(--text-light);
  font-size: 0.9rem;
  margin-bottom: var(--spacing-xs);
  font-weight: 500;
}

.detail-value {
  color: var(--text);
  font-size: 1rem;
}

.mono {
  font-family: monospace;
  font-weight: 600;
  color: var(--primary);
  font-size: 0.95rem;
}

.detail-description {
  line-height: 1.6;
  color: var(--text);
  background-color: white;
  padding: var(--spacing-md);
  border-radius: var(--radius-sm);
  border-left: 4px solid var(--primary-light);
  margin: 0;
}

.full-width {
  grid-column: 1 / -1;
}

/* Status banner redesign */
.status-banner {
  grid-column: 1 / -1;
  background-color: var(--background);
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--radius-lg);
  margin-bottom: var(--spacing-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.status-banner:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.status-text {
  font-size: 1.1rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Modal Timeline */
.modal-timeline {
  position: relative;
  padding: var(--spacing-md) var(--spacing-xs);
}

.vertical-timeline-item {
  position: relative;
  display: flex;
  margin-bottom: var(--spacing-md);
  padding-left: 45px;
}

.vertical-timeline-item:last-child {
  margin-bottom: 0;
}

.vertical-timeline-marker {
  position: absolute;
  left: 0;
  top: 0;
  z-index: 2;
}

.vertical-marker-inner {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--primary-light);
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  box-shadow: 0 0 0 4px white, 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.vertical-timeline-item:hover .vertical-marker-inner {
  transform: translateY(-3px);
  box-shadow: 0 0 0 4px white, 0 6px 10px rgba(0, 0, 0, 0.15);
}

.vertical-timeline-content {
  flex: 1;
  padding-right: var(--spacing-xs);
}

.vertical-timeline-title {
  font-weight: 600;
  font-size: 1.05rem;
  color: var(--text);
  margin-bottom: 3px;
}

.vertical-timeline-date {
  font-size: 0.85rem;
  color: var(--text-light);
  font-weight: 500;
  margin-bottom: 3px;
}

/* Status-specific marker colors */
.vertical-status-marker-status-success .vertical-marker-inner {
  background-color: #059669;
}

.vertical-status-marker-status-danger .vertical-marker-inner {
  background-color: #DC2626;
}

.vertical-status-marker-status-warning .vertical-marker-inner {
  background-color: #D97706;
}

.vertical-status-marker-status-info .vertical-marker-inner {
  background-color: #2563EB;
}

.vertical-status-marker-status-secondary .vertical-marker-inner {
  background-color: #4B5563;
}

/* Modal transitions */
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .detail-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }
  
  .overview-map-row {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }
  
  .map-section {
    margin-bottom: var(--spacing-md);
  }
  
  .timeline-track {
    left: 100px;
  }
  
  .timeline-point {
    grid-template-columns: 100px 50px 1fr;
  }
  
  .timeline-date {
    font-size: 0.8rem;
  }
  
  .marker-inner {
    width: 30px;
    height: 30px;
  }
}

/* Update status banner styling to fit in the column */
.status-section {
  margin-bottom: var(--spacing-md);
}

.status-banner {
  padding: var(--spacing-md);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  margin: 0;
}

/* Updated styles for expanded content */
.expanded-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
  padding: var(--spacing-md);
}

.timeline-container, .ai-summary-container {
  background-color: white;
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
}

.ai-summary-text {
  margin: 0;
  padding: var(--spacing-md);
  line-height: 1.6;
  color: var(--text);
  text-align: justify;
  background-color: var(--background-lighter);
  border-radius: var(--radius-sm);
  border-left: 4px solid var(--primary-light);
}

/* Timeline in expanded row */
.timeline-header {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: var(--spacing-md);
  color: var(--primary);
  border-bottom: 1px solid var(--border);
  padding-bottom: var(--spacing-xs);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.timeline-items-container {
  display: flex;
  justify-content: space-between;
  gap: var(--spacing-md);
}

/* Mobile view adjustments */
@media (max-width: 768px) {
  .expanded-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }
  
  .timeline-items-container {
    flex-direction: column;
  }
  
  .timeline-item {
    margin-bottom: var(--spacing-md);
  }
}

/* Map Section */
.map-section {
  margin-bottom: var(--spacing-xl);
}

.map-container {
  border-radius: var(--radius-lg);
  overflow: hidden;
  background-color: white;
  box-shadow: var(--shadow-md);
  display: flex;
  flex-direction: column;
  height: 100%;
  flex: 1;
}

.map-header {
  padding: var(--spacing-md) var(--spacing-lg);
  background-color: var(--primary);
  color: white;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.map-header h2 {
  color: white;
  margin: 0;
  font-size: 1.1rem;
}

.map-address {
  font-size: 0.9rem;
  opacity: 0.9;
}

.map-source {
  font-size: 0.8rem;
  opacity: 0.8;
  margin-top: 5px;
}

.map-content {
  flex: 1; /* Allow map to fill remaining space */
  position: relative;
  min-height: 335px;
}

.leaflet-map {
  height: 100%;
  width: 100%;
  z-index: 1;
}

.map-loading, .map-error {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-md);
  z-index: 2;
}

.loading-icon, .error-icon {
  width: 32px;
  height: 32px;
  color: var(--primary);
}

.spin {
  animation: spin 1.5s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* GOV.UK theme adjustments for map */
:deep(body.govuk-theme) .map-container {
  border-radius: 0;
  box-shadow: none;
  border: 1px solid #b1b4b6;
}

:deep(body.govuk-theme) .map-header {
  background-color: #1d70b8;
  padding: 15px;
}

:deep(body.govuk-theme) .map-header h2 {
  font-family: "GDS Transport", arial, sans-serif;
  font-size: 19px;
  font-weight: 700;
  margin: 0;
}

/* Fix any Leaflet specific style issues */
:deep(.leaflet-container) {
  font: inherit;
}

:deep(.leaflet-control-attribution) {
  font-size: 10px;
}

/* Updated styling for the expand all button */
.expand-all-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  background: linear-gradient(to right, var(--primary-light), var(--primary));
  color: white;
  font-weight: 600;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  transition: all var(--transition-normal);
  border: none;
  box-shadow: 0 3px 8px rgba(var(--primary-rgb), 0.25);
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.expand-all-btn:before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to right, var(--primary), var(--primary-dark));
  z-index: -1;
  transition: opacity 0.3s ease;
  opacity: 0;
}

.expand-all-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 12px rgba(var(--primary-rgb), 0.4);
}

.expand-all-btn:hover:before {
  opacity: 1;
}

.expand-all-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 5px rgba(var(--primary-rgb), 0.3);
}

/* GOV.UK theme adjustments for expand-all button */
:deep(body.govuk-theme) .expand-all-btn {
  background: #00703c;
  box-shadow: 0 2px 0 #002d18;
  border-radius: 0;
  font-family: "GDS Transport", arial, sans-serif;
  font-size: 16px;
  font-weight: 400;
  color: white;
}

:deep(body.govuk-theme) .expand-all-btn:before {
  display: none;
}

:deep(body.govuk-theme) .expand-all-btn:hover {
  background-color: #005a30;
  transform: none;
  box-shadow: 0 2px 0 #002d18;
}

:deep(body.govuk-theme) .expand-all-btn:active {
  top: 2px;
  box-shadow: none;
}

/* Fix Leaflet zoom controls */
:deep(.leaflet-control-container) {
  position: absolute;
  z-index: 1000;
}

:deep(.leaflet-control-zoom) {
  margin: var(--spacing-md);
  box-shadow: var(--shadow-md);
  border: none;
  border-radius: var(--radius-sm);
  overflow: hidden;
}

:deep(.leaflet-control-zoom-in),
:deep(.leaflet-control-zoom-out) {
  color: var(--text) !important;
  background-color: white !important;
  width: 30px;
  height: 30px;
  line-height: 30px;
  font-size: 18px;
  font-weight: 600;
  border: none !important;
}

:deep(.leaflet-control-zoom-in:hover),
:deep(.leaflet-control-zoom-out:hover) {
  background-color: var(--background) !important;
  color: var(--primary) !important;
}

/* Summary row in the table */
.summary-row {
  background-color: var(--background-lighter);
  border-bottom: 1px solid var(--border);
}

.summary-cell {
  padding: 0 !important;
}

.summary-container {
  padding: var(--spacing-sm) var(--spacing-md);
  position: relative;
}

.summary-text {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--text);
  text-align: justify;
  position: relative;
  /* Remove max-height and truncation */
  max-height: none;
  overflow: visible;
  display: block;
  -webkit-line-clamp: unset;
  -webkit-box-orient: unset;
}

.ai-icon {
  color: var(--primary);
  margin-right: var(--spacing-xs);
  vertical-align: text-bottom;
}

.ai-label {
  font-weight: 600;
  color: var(--primary);
  margin-right: var(--spacing-xs);
}

/* Timeline in expanded row */
.timeline-container {
  background-color: var(--background-lighter);
  border-radius: var(--radius-sm);
  padding: var(--spacing-md);
  margin: var(--spacing-sm) 0;
}

.timeline-header {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: var(--spacing-md);
  color: var(--primary);
  border-bottom: 1px solid var(--border);
  padding-bottom: var(--spacing-xs);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.timeline-items-container {
  display: flex;
  justify-content: space-between;
  gap: var(--spacing-md);
  padding-left: var(--spacing-xs);
}

.timeline-item {
  position: relative;
  flex: 1;
  padding-left: 45px;
  margin-bottom: var(--spacing-sm);
}

/* Set appropriate background colors */
:root {
  --background-lighter: #F9FAFB;
}

/* Mobile view adjustments */
@media (max-width: 768px) {
  .timeline-items-container {
    flex-direction: column;
  }
  
  .timeline-item {
    margin-bottom: var(--spacing-md);
  }
}
</style>
