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
        <!-- AI Summary Sections -->
        <div class="summary-sections animate-slide-up">
          <div class="summary-card">
            <div class="summary-header">
              <svg xmlns="http://www.w3.org/2000/svg" class="summary-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <h2>Enforcement Summary</h2>
            </div>
            <div class="summary-content">
              <p>{{ aiSummaries.enforcement }}</p>
              <div class="summary-metrics">
                <div class="metric">
                  <span class="metric-value">2</span>
                  <span class="metric-label">Actions</span>
                </div>
                <div class="metric">
                  <span class="metric-value">1</span>
                  <span class="metric-label">Active</span>
                </div>
              </div>
            </div>
          </div>

          <div class="summary-card">
            <div class="summary-header">
              <svg xmlns="http://www.w3.org/2000/svg" class="summary-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
              </svg>
              <h2>Appeals Summary</h2>
            </div>
            <div class="summary-content">
              <p>{{ aiSummaries.appeals }}</p>
              <div class="summary-metrics">
                <div class="metric">
                  <span class="metric-value">3</span>
                  <span class="metric-label">Total</span>
                </div>
                <div class="metric">
                  <span class="metric-value">33%</span>
                  <span class="metric-label">Approved</span>
                </div>
              </div>
            </div>
          </div>

          <div class="summary-card">
            <div class="summary-header">
              <svg xmlns="http://www.w3.org/2000/svg" class="summary-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              <h2>Planning Application Summary</h2>
            </div>
            <div class="summary-content">
              <p>{{ aiSummaries.planningAppeals }}</p>
              <div class="summary-metrics">
                <div class="metric">
                  <span class="metric-value">45%</span>
                  <span class="metric-label">Avg. Rate</span>
                </div>
                <div class="metric">
                  <span class="metric-value">33%</span>
                  <span class="metric-label">This Address</span>
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
                  <th @click="sortBy('decisionDate')" class="sortable-header">
                    Decision Date
                    <span v-if="sortField === 'decisionDate'" class="sort-indicator">
                      {{ sortOrder === 'asc' ? '↑' : '↓' }}
                    </span>
                  </th>
                  <th>Address</th>
                  <th @click="sortBy('type')" class="sortable-header">
                    Type
                    <span v-if="sortField === 'type'" class="sort-indicator">
                      {{ sortOrder === 'asc' ? '↑' : '↓' }}
                    </span>
                  </th>
                  <th @click="sortBy('status')" class="sortable-header">
                    Status
                    <span v-if="sortField === 'status'" class="sort-indicator">
                      {{ sortOrder === 'asc' ? '↑' : '↓' }}
                    </span>
                  </th>
                  <th>Details</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="record in filteredPaginatedRecords" :key="record.id" class="record-row">
                  <td class="app-number">{{ record.applicationNumber }}</td>
                  <td>{{ formatDate(record.decisionDate) }}</td>
                  <td class="address-cell">{{ record.address }}</td>
                  <td>
                    <span :class="'type-badge ' + getTypeClass(record.type)">{{ record.type }}</span>
                  </td>
                  <td>
                    <span :class="'status-badge ' + getStatusClass(record.status)">{{ record.status }}</span>
                  </td>
                  <td>
                    <button @click="showDetails(record)" class="btn-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" class="details-icon" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                        <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                      </svg>
                    </button>
                  </td>
                </tr>
                <tr v-if="filteredPaginatedRecords.length === 0">
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
          
          <!-- Pagination -->
          <div class="pagination">
            <button 
              @click="prevPage" 
              :disabled="currentPage === 1" 
              class="pagination-button"
              :class="{ 'disabled': currentPage === 1 }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="pagination-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              Previous
            </button>
            
            <div class="pagination-info">
              <span>Page {{ currentPage }} of {{ totalPages }}</span>
              <span class="pagination-details">Showing {{ startItem }}-{{ endItem }} of {{ filteredRecords.length }} records</span>
            </div>
            
            <button 
              @click="nextPage" 
              :disabled="currentPage >= totalPages" 
              class="pagination-button"
              :class="{ 'disabled': currentPage >= totalPages }"
            >
              Next
              <svg xmlns="http://www.w3.org/2000/svg" class="pagination-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
              </svg>
            </button>
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
import { useRouter } from 'vue-router';
import { fetchAddressRecords, mapApiDataToRecords } from '../data/api';
import { aiSummaries } from '../data/sampleData';

const router = useRouter();

// State variables
const address = ref('test'); // Default address to search for
const records = ref([]);
const loading = ref(true);
const error = ref(null);
const tableFilter = ref('');
const sortField = ref('decisionDate');
const sortOrder = ref('desc');
const displayDialog = ref(false);
const selectedRecord = ref(null);
const currentPage = ref(1);
const itemsPerPage = 5;

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

const totalPages = computed(() => {
  return Math.ceil(filteredRecords.value.length / itemsPerPage);
});

const startItem = computed(() => {
  return (currentPage.value - 1) * itemsPerPage + 1;
});

const endItem = computed(() => {
  const end = currentPage.value * itemsPerPage;
  return end > filteredRecords.value.length ? filteredRecords.value.length : end;
});

const filteredPaginatedRecords = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return sortedRecords.value.slice(start, end);
});

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
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
</script>

<style scoped>
.dashboard-container {
  padding-bottom: var(--spacing-2xl);
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
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.summary-card {
  background-color: white;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition: transform var(--transition-normal), box-shadow var(--transition-normal);
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

/* Specific GOV.UK styling for summary cards */
:deep(body.govuk-theme) .summary-sections {
  display: flex;
  flex-direction: row;
  gap: 20px;
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
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  max-height: 4.5em;
  margin-bottom: 20px;
}

:deep(body.govuk-theme) .summary-icon {
  color: white;
  width: 22px;
  height: 22px;
}

.summary-metrics {
  display: flex;
  gap: var(--spacing-lg);
  margin-top: var(--spacing-md);
}

/* Default theme metrics styling */
.metric {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  align-items: center;
  background-color: rgba(var(--primary-rgb), 0.05);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-lg);
  min-width: 80px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  text-align: center;
}

.metric:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.metric-value {
  font-size: 1.8rem;
  font-weight: 700;
  background: linear-gradient(45deg, var(--primary), #1e40af);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-fill-color: transparent;
  order: 1;
  margin-bottom: 4px;
}

.metric-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  order: 2;
}

/* GOV.UK theme metrics styling */
:deep(body.govuk-theme) .summary-metrics {
  display: flex;
  gap: 20px;
  border-top: 1px solid #b1b4b6;
  padding-top: 15px;
  margin-top: 5px;
}

:deep(body.govuk-theme) .metric {
  background-color: transparent;
  padding: 0;
  border-radius: 0;
  box-shadow: none;
  align-items: flex-start;
  min-width: 0;
}

:deep(body.govuk-theme) .metric:hover {
  transform: none;
  box-shadow: none;
}

:deep(body.govuk-theme) .metric-value {
  font-size: 24px;
  font-weight: 700;
  color: #1d70b8;
  background: none;
  -webkit-text-fill-color: currentColor;
  font-family: "GDS Transport", arial, sans-serif;
  margin-bottom: 4px;
  order: 1;
}

:deep(body.govuk-theme) .metric-label {
  font-size: 16px;
  font-weight: normal;
  color: #0b0c0c;
  text-transform: none;
  letter-spacing: normal;
  font-family: "GDS Transport", arial, sans-serif;
  order: 2;
}

/* Records Section */
.records-section {
  padding: var(--spacing-lg);
  background-color: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
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

/* Pagination */
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border);
}

.pagination-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  background-color: white;
  border: 1px solid var(--border);
  color: var(--text);
  cursor: pointer;
  transition: all var(--transition-normal);
}

.pagination-button:hover:not(.disabled) {
  border-color: var(--primary);
  color: var(--primary);
}

.pagination-button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-icon {
  width: 16px;
  height: 16px;
}

.pagination-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
}

.pagination-details {
  font-size: 0.8rem;
  color: var(--text-light);
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
  max-width: 700px;
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
  grid-column: span 2;
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
  
  .pagination {
    flex-direction: column;
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
</style> 