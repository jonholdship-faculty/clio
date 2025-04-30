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
        <!-- Summary Section - One Large Card -->
        <div class="summary-sections animate-slide-up">
          <div class="summary-card full-width">
            <div class="summary-header">
              <svg xmlns="http://www.w3.org/2000/svg" class="summary-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <h2>Overview</h2>
            </div>
            <div class="summary-content">
              <p>This address has a complex planning history with multiple applications and enforcement actions. There are several noteworthy trends in the planning history including changes in application types over time and varying decision outcomes.</p>
              
              <div class="indicators-row">
                <div class="indicator primary-indicator">
                  <span class="indicator-number">3</span>
                  <span class="indicator-label">Applications</span>
                </div>
                
                <div class="indicator success-indicator">
                  <span class="indicator-number">33%</span>
                  <span class="indicator-label">Approval Rate</span>
                </div>
                
                <div class="indicator warning-indicator">
                  <span class="indicator-number">1</span>
                  <span class="indicator-label">Successful Appeals</span>
                </div>
                
                <div class="indicator danger-indicator">
                  <span class="indicator-number">1</span>
                  <span class="indicator-label">Active Enforcements</span>
                </div>
                
                <div class="indicator danger-indicator">
                  <span class="indicator-number">2</span>
                  <span class="indicator-label">Rejected</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Map Component -->
        <div class="map-section animate-fade-in">
          <div class="map-container">
            <div class="map-header">
              <h2>Location</h2>
              <div class="map-address">{{ address }}</div>
            </div>
            <div class="map-content">
              <div class="map-placeholder">
                <img :src="`https://maps.googleapis.com/maps/api/staticmap?center=${encodeURIComponent(address)}&zoom=15&size=600x400&key=AIzaSyBGCql0HlN4C_D7B2BcIIhtuFGjhB-IKgA&markers=${encodeURIComponent(address)}`" 
                  :alt="`Map showing ${address}`" 
                  class="static-map-image"
                />
                <div class="map-overlay">
                  <svg xmlns="http://www.w3.org/2000/svg" class="map-pin-icon" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                  </svg>
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
                  <th @click="sortBy('applicationNumber')" class="sortable-header">
                    Application Number
                    <span v-if="sortField === 'applicationNumber'" class="sort-indicator">
                      {{ sortOrder === 'asc' ? '↑' : '↓' }}
                    </span>
                  </th>
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
                  <th @click="sortBy('decisionDate')" class="sortable-header">
                    Decision Date
                    <span v-if="sortField === 'decisionDate'" class="sort-indicator">
                      {{ sortOrder === 'asc' ? '↑' : '↓' }}
                    </span>
                  </th>
                  <th>Address</th>
                  <th>Details</th>
                </tr>
              </thead>
              <tbody>
                <template v-for="record in filteredRecords" :key="record.id">
                  <tr class="record-row">
                    <td class="app-number">{{ record.applicationNumber }}</td>
                    <td>
                      <span :class="'status-badge ' + getStatusClass(record.status)">{{ record.status }}</span>
                    </td>
                    <td>
                      <span :class="'type-badge ' + getTypeClass(record.type)">{{ record.type }}</span>
                    </td>
                    <td>{{ formatDate(record.decisionDate) }}</td>
                    <td class="address-cell">{{ record.address }}</td>
                    <td class="actions-cell">
                      <button @click="showDetails(record)" class="btn-icon info-btn">
                        <svg xmlns="http://www.w3.org/2000/svg" class="details-icon" viewBox="0 0 20 20" fill="currentColor">
                          <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                          <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                        </svg>
                      </button>
                      <button @click="toggleRowExpansion(record.id)" class="btn-icon expand-btn">
                        <svg xmlns="http://www.w3.org/2000/svg" class="details-icon" viewBox="0 0 20 20" fill="currentColor">
                          <path v-if="isRowExpanded(record.id)" fill-rule="evenodd" d="M5 10a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1z" clip-rule="evenodd" />
                          <path v-else fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
                        </svg>
                      </button>
                    </td>
                  </tr>
                  <tr v-if="isRowExpanded(record.id)" class="expanded-row">
                    <td colspan="6" class="expanded-content">
                      <div class="expanded-grid">
                        <div class="expanded-section">
                          <h3 class="expanded-header">Application Details</h3>
                          <div class="expanded-detail">
                            <span class="detail-label">Application Ref:</span>
                            <span class="detail-value">{{ record.applicationNumber }}</span>
                          </div>
                          <div class="expanded-detail">
                            <span class="detail-label">Address:</span>
                            <span class="detail-value">{{ record.address }}</span>
                          </div>
                          <div class="expanded-detail">
                            <span class="detail-label">Status:</span>
                            <span class="detail-value">{{ record.status }}</span>
                          </div>
                          <div class="expanded-detail">
                            <span class="detail-label">Type:</span>
                            <span class="detail-value">{{ record.type }}</span>
                          </div>
                        </div>
                        <div class="expanded-section">
                          <h3 class="expanded-header">Timeline</h3>
                          <div class="expanded-detail">
                            <span class="detail-label">Submission Date:</span>
                            <span class="detail-value">{{ formatDate(new Date(record.decisionDate).setMonth(new Date(record.decisionDate).getMonth() - 2)) }}</span>
                          </div>
                          <div class="expanded-detail">
                            <span class="detail-label">Review Date:</span>
                            <span class="detail-value">{{ formatDate(new Date(record.decisionDate).setMonth(new Date(record.decisionDate).getMonth() - 1)) }}</span>
                          </div>
                          <div class="expanded-detail">
                            <span class="detail-label">Decision Date:</span>
                            <span class="detail-value">{{ formatDate(record.decisionDate) }}</span>
                          </div>
                        </div>
                        <div class="expanded-section full-width">
                          <h3 class="expanded-header">Description</h3>
                          <p class="expanded-description">{{ record.details }}</p>
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
              <h3>{{ selectedRecord?.description || '' }}</h3>
              <span class="modal-app-number">{{ selectedRecord?.applicationNumber }}</span>
            </div>
            <button @click="displayDialog = false" class="modal-close">
              <svg xmlns="http://www.w3.org/2000/svg" class="close-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
          
          <div v-if="selectedRecord" class="modal-body">
            <div class="detail-grid">
              <div class="detail-group">
                <div class="detail-label">Address</div>
                <div class="detail-value">{{ selectedRecord.address }}</div>
              </div>
              
              <div class="detail-group">
                <div class="detail-label">Decision Date</div>
                <div class="detail-value">{{ formatDate(selectedRecord.decisionDate) }}</div>
              </div>
              
              <div class="detail-group">
                <div class="detail-label">Type</div>
                <div class="detail-value">
                  <span :class="'type-badge ' + getTypeClass(selectedRecord.type)">
                    {{ selectedRecord.type }}
                  </span>
                </div>
              </div>
              
              <div class="detail-group">
                <div class="detail-label">Status</div>
                <div class="detail-value">
                  <span :class="'status-badge ' + getStatusClass(selectedRecord.status)">
                    {{ selectedRecord.status }}
                  </span>
                </div>
              </div>
              
              <div class="detail-group full-width">
                <div class="detail-label">Details</div>
                <div class="detail-value">{{ selectedRecord.details }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { fetchAddressRecords, mapApiDataToRecords } from '../data/api';
import { aiSummaries } from '../data/sampleData';

const router = useRouter();
const route = useRoute();

// State variables
const address = ref(route.query.address || 'test');
const records = ref([]);
const loading = ref(true);
const error = ref(null);
const tableFilter = ref('');
const sortField = ref('decisionDate');
const sortOrder = ref('desc');
const displayDialog = ref(false);
const selectedRecord = ref(null);
const expandedRows = ref([]); // Track which rows are expanded

// Toggle row expansion
const toggleRowExpansion = (recordId) => {
  const index = expandedRows.value.indexOf(recordId);
  if (index >= 0) {
    expandedRows.value.splice(index, 1);
  } else {
    expandedRows.value.push(recordId);
  }
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
  } catch (err) {
    error.value = 'Failed to load planning records. Please try again later.';
    loading.value = false;
    console.error('Error loading records:', err);
  }
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
  switch (type) {
    case 'Enforcement': return 'type-danger';
    case 'Appeal': return 'type-warning';
    case 'Planning Application': return 'type-success';
    default: return '';
  }
};

const getStatusClass = (status) => {
  switch (status) {
    case 'Approved': return 'status-success';
    case 'Rejected': return 'status-danger';
    case 'Pending': return 'status-warning';
    case 'Active': return 'status-info';
    case 'Withdrawn': return 'status-secondary';
    case 'Resolved': return 'status-success';
    case 'Approved with Conditions': return 'status-success';
    default: return 'status-info';
  }
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
}

.modal-content {
  background-color: white;
  border-radius: var(--radius-lg);
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-xl);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border);
}

.modal-title {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.modal-title h3 {
  margin: 0;
  color: var(--text);
  font-size: 1.25rem;
}

.modal-app-number {
  font-family: monospace;
  color: var(--text-light);
  font-size: 0.9rem;
}

.modal-close {
  background: none;
  border: none;
  color: var(--text-light);
  cursor: pointer;
  padding: var(--spacing-xs);
  border-radius: var(--radius-sm);
  transition: background-color var(--transition-normal);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close:hover {
  background-color: var(--border);
}

.close-icon {
  width: 24px;
  height: 24px;
}

.modal-body {
  padding: var(--spacing-lg);
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
}

.detail-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.full-width {
  width: 100%;
  max-width: 100%;
}

.detail-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-light);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 1rem;
  color: var(--text);
}

/* Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
  }
  
  .summary-sections {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
  
  .full-width {
    grid-column: span 1;
  }
}

.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  background-color: var(--card-bg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  margin: 2rem 0;
  text-align: center;
}

.loading-icon, .error-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 1rem;
  color: var(--primary);
}

.error-icon {
  color: var(--error);
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.actions-cell {
  display: flex;
  gap: var(--spacing-xs);
}

.info-btn {
  background-color: var(--info);
}

.info-btn:hover {
  background-color: var(--info-dark, #0369a1);
}

.expand-btn {
  background-color: var(--success);
}

.expand-btn:hover {
  background-color: var(--success-dark, #047857);
}

.expanded-row {
  background-color: rgba(var(--primary-rgb), 0.03);
}

.expanded-content {
  padding: var(--spacing-lg);
  border-top: 1px dashed var(--border);
  border-bottom: 1px dashed var(--border);
}

.expanded-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-lg);
}

.expanded-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.expanded-section.full-width {
  grid-column: 1 / -1;
}

.expanded-header {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: var(--spacing-xs);
  color: var(--primary);
  border-bottom: 1px solid var(--border);
  padding-bottom: var(--spacing-xs);
}

.expanded-detail {
  display: flex;
  gap: var(--spacing-sm);
  font-size: 0.9rem;
  line-height: 1.5;
}

.detail-label {
  font-weight: 600;
  color: var(--text-light);
  min-width: 130px;
}

.detail-value {
  color: var(--text);
}

.expanded-description {
  line-height: 1.6;
  margin: 0;
  color: var(--text);
}

:deep(body.govuk-theme) .expanded-row {
  background-color: #f3f2f1;
}

:deep(body.govuk-theme) .expanded-header {
  font-family: "GDS Transport", arial, sans-serif;
  font-weight: 700;
  color: #0b0c0c;
  border-bottom-color: #b1b4b6;
}

:deep(body.govuk-theme) .detail-label {
  font-family: "GDS Transport", arial, sans-serif;
  font-weight: 700;
  color: #505a5f;
}

:deep(body.govuk-theme) .detail-value {
  font-family: "GDS Transport", arial, sans-serif;
  color: #0b0c0c;
}

@media (max-width: 768px) {
  .expanded-grid {
    grid-template-columns: 1fr;
  }
}

/* Map Section */
.map-section {
  margin-bottom: var(--spacing-xl);
  width: 100%;
}

.map-container {
  background-color: white;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  width: 100%;
}

.map-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-md) var(--spacing-lg);
  background-color: var(--primary);
  color: white;
}

.map-header h2 {
  margin: 0;
  font-size: 1.1rem;
  color: white;
}

.map-address {
  font-size: 0.9rem;
  font-weight: 500;
  background-color: rgba(255, 255, 255, 0.2);
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--radius-md);
}

.map-content {
  width: 100%;
}

.map-placeholder {
  position: relative;
  width: 100%;
  height: 400px;
}

.static-map-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-top-left-radius: var(--radius-lg);
  border-top-right-radius: var(--radius-lg);
}

.map-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  border-top-left-radius: var(--radius-lg);
  border-top-right-radius: var(--radius-lg);
}

.map-pin-icon {
  width: 24px;
  height: 24px;
  color: var(--primary);
}

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
  font-weight: 700;
  font-size: 19px;
}

:deep(body.govuk-theme) .map-address {
  font-family: "GDS Transport", arial, sans-serif;
}

:deep(body.govuk-theme) .map-frame {
  border-radius: 0;
}
</style> 