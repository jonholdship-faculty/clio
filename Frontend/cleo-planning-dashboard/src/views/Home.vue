<template>
  <div class="home-container">
    <div class="container">
      <div class="hero-section animate-slide-up">
        <h1 class="hero-title">Streamline Your Planning Records</h1>
        <p class="hero-description">
          Efficiently search and manage all planning applications, appeals, and enforcement actions from one central dashboard.
        </p>
        
        <div class="search-container">
          <div class="search-card">
            <h2>Find Planning Records</h2>
            <div class="search-form">
              <div class="search-input-container">
                <input 
                  v-model="searchQuery" 
                  placeholder="Enter an address (e.g. 12 High Street, London)" 
                  class="search-input"
                  @keyup.enter="searchAddress"
                  @input="handleSearchInput"
                />
                <div class="search-icon-wrapper">
                  <svg xmlns="http://www.w3.org/2000/svg" class="search-icon" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                  </svg>
                </div>
                <!-- Address Records Dropdown -->
                <div v-if="showDropdown && searchResults.length > 0" class="search-dropdown">
                  <div class="dropdown-header">
                    <span>Available records for "{{ searchQuery }}"</span>
                  </div>
                  <div class="dropdown-results">
                    <div 
                      v-for="record in searchResults" 
                      :key="record.id" 
                      class="dropdown-item"
                      @click="selectRecord(record)"
                    >
                      <div class="record-icon" :class="getTypeClass(record.type)">
                        <svg xmlns="http://www.w3.org/2000/svg" class="item-icon" viewBox="0 0 20 20" fill="currentColor">
                          <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd" />
                        </svg>
                      </div>
                      <div class="record-info">
                        <div class="record-title">{{ record.applicationNumber }}</div>
                        <div class="record-subtitle">{{ record.address }}</div>
                      </div>
                      <div class="record-badge" :class="getStatusClass(record.status)">
                        {{ record.status }}
                      </div>
                    </div>
                  </div>
                  <div class="dropdown-footer">
                    <button @click="searchAddress" class="view-all-btn">
                      View all results
                    </button>
                  </div>
                </div>
                
                <!-- No Results Message -->
                <div v-else-if="showDropdown && searchQuery && !loading && searchResults.length === 0" class="search-dropdown">
                  <div class="no-results">
                    <svg xmlns="http://www.w3.org/2000/svg" class="no-results-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>No records found for "{{ searchQuery }}"</span>
                  </div>
                </div>
                
                <!-- Loading State -->
                <div v-else-if="showDropdown && loading" class="search-dropdown">
                  <div class="loading-results">
                    <svg xmlns="http://www.w3.org/2000/svg" class="loading-icon spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    <span>Searching records...</span>
                  </div>
                </div>
              </div>
              <button @click="searchAddress" class="btn btn-primary search-button">
                <svg xmlns="http://www.w3.org/2000/svg" class="button-icon" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                </svg>
                Search Records
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { fetchAddressRecords, mapApiDataToRecords } from '../data/api';

const router = useRouter();
const searchQuery = ref('');
const searchResults = ref([]);
const showDropdown = ref(false);
const loading = ref(false);
const searchTimeout = ref(null);

// Handle input in the search box
const handleSearchInput = () => {
  clearTimeout(searchTimeout.value);
  
  if (searchQuery.value.trim().length < 2) {
    searchResults.value = [];
    showDropdown.value = searchQuery.value.trim().length > 0;
    return;
  }
  
  showDropdown.value = true;
  loading.value = true;
  
  // Debounce the API call to avoid excessive requests
  searchTimeout.value = setTimeout(async () => {
    try {
      // If we're using a real API, we'd call it here
      const apiData = await fetchAddressRecords(searchQuery.value.trim());
      const mappedData = mapApiDataToRecords(apiData);
      searchResults.value = mappedData;
    } catch (error) {
      console.error('Error fetching search results', error);
      searchResults.value = [];
    } finally {
      loading.value = false;
    }
  }, 300);
};

// Select a specific record from the dropdown
const selectRecord = (record) => {
  router.push({
    name: 'Dashboard',
    query: { 
      address: record.address,
      ref: record.applicationNumber
    }
  });
};

const searchAddress = () => {
  if (searchQuery.value.trim()) {
    router.push({
      name: 'Dashboard',
      query: { address: searchQuery.value.trim() }
    });
    showDropdown.value = false;
  }
};

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  const searchContainer = document.querySelector('.search-input-container');
  if (searchContainer && !searchContainer.contains(event.target)) {
    showDropdown.value = false;
  }
};

// Handle type and status classes for styling
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

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  clearTimeout(searchTimeout.value);
});
</script>

<style scoped>
.home-container {
  min-height: calc(100vh - 64px - 60px);
}

.hero-section {
  text-align: center;
  padding: var(--spacing-xl) 0;
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3rem;
  margin-bottom: var(--spacing-md);
  background: linear-gradient(90deg, 
    var(--primary) 0%, 
    #60a5fa 25%, 
    #7e22ce 50%, 
    #60a5fa 75%, 
    var(--primary) 100%);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-fill-color: transparent;
  animation: gradient-shift 8s ease infinite;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.05);
}

@keyframes gradient-shift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.hero-description {
  font-size: 1.2rem;
  color: var(--text-light);
  margin-bottom: var(--spacing-xl);
  line-height: 1.6;
}

.search-container {
  margin-top: var(--spacing-xl);
}

.search-card {
  background-color: white;
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl) var(--spacing-xl);
  box-shadow: var(--shadow-lg), 0 15px 40px -15px rgba(var(--primary-rgb), 0.2);
  max-width: 700px;
  margin: 0 auto;
  transition: transform var(--transition-normal), box-shadow var(--transition-normal);
  border: 1px solid rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: visible;
  backdrop-filter: blur(10px);
  animation: cardFloat 6s ease-in-out infinite;
}

@keyframes cardFloat {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}

.search-card::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 250px;
  height: 250px;
  background: radial-gradient(circle, rgba(var(--primary-rgb), 0.08) 0%, transparent 70%);
  border-radius: 50%;
  transform: translate(30%, -30%);
  z-index: 0;
}

.search-card::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(var(--accent-rgb), 0.06) 0%, transparent 70%);
  border-radius: 50%;
  transform: translate(-30%, 30%);
  z-index: 0;
}

.search-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-xl), 0 15px 35px -15px rgba(var(--primary-rgb), 0.2);
}

.search-card h2 {
  margin-bottom: var(--spacing-lg);
  color: var(--text);
  font-size: 1.6rem;
  position: relative;
  text-align: center;
}

.search-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  position: relative;
  z-index: 10;
}

.search-input-container {
  position: relative;
  margin-bottom: var(--spacing-lg);
}

.search-input {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-md) var(--spacing-md) var(--spacing-xl);
  font-size: 1.1rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-sm);
  height: 60px;
}

.search-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15), var(--shadow-md);
  outline: none;
}

.search-icon-wrapper {
  position: absolute;
  left: var(--spacing-sm);
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-light);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
}

.search-icon {
  width: 20px;
  height: 20px;
}

.button-icon {
  width: 20px;
  height: 20px;
}

.search-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-xl);
  font-weight: 600;
  font-size: 1.1rem;
  transition: all var(--transition-normal);
  height: 60px;
  background: linear-gradient(to right, var(--primary), #60a5fa);
  border-radius: var(--radius-lg);
  box-shadow: 0 4px 10px rgba(var(--primary-rgb), 0.3);
  letter-spacing: 0.5px;
}

.search-button:hover {
  background: linear-gradient(to right, var(--primary-dark), var(--primary));
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(var(--primary-rgb), 0.4);
}

/* GOV.UK specific styling for the search form */
:deep(body.govuk-theme) .search-card {
  background-color: #fff;
  border-radius: 0;
  box-shadow: none;
  border: 1px solid #b1b4b6;
  padding: 30px;
  margin-bottom: 30px;
}

:deep(body.govuk-theme) .search-card h2 {
  font-family: "GDS Transport", arial, sans-serif;
  font-weight: 700;
  font-size: 24px;
  color: #0b0c0c;
  margin-bottom: 20px;
}

:deep(body.govuk-theme) .search-card::before {
  display: none;
}

:deep(body.govuk-theme) .search-form {
  gap: 15px;
}

:deep(body.govuk-theme) .search-input-container {
  margin-bottom: 20px;
}

:deep(body.govuk-theme) .search-input {
  border: 2px solid #0b0c0c;
  border-radius: 0;
  box-shadow: none;
  padding: 5px 10px 5px 35px;
  height: 40px;
  font-family: "GDS Transport", arial, sans-serif;
  font-size: 16px;
}

:deep(body.govuk-theme) .search-input:focus {
  outline: 3px solid #ffdd00;
  outline-offset: 0;
  box-shadow: inset 0 0 0 2px #0b0c0c;
}

:deep(body.govuk-theme) .search-icon-wrapper {
  left: 10px;
  color: #0b0c0c;
}

:deep(body.govuk-theme) .search-button {
  background: #00703c;
  box-shadow: 0 2px 0 #002d18;
  border-radius: 0;
  padding: 8px 10px 7px;
  font-family: "GDS Transport", arial, sans-serif;
  font-size: 16px;
  font-weight: 400;
  min-height: 40px;
  height: auto;
  color: white;
  width: 100%;
  max-width: 200px;
  margin-left: 0;
  transition: background-color 0.2s ease;
}

:deep(body.govuk-theme) .search-button:hover {
  background-color: #005a30;
  transform: none;
}

:deep(body.govuk-theme) .search-button:focus {
  outline: 3px solid #ffdd00;
  outline-offset: 0;
  box-shadow: inset 0 0 0 2px #0b0c0c;
}

:deep(body.govuk-theme) .features-section {
  border-radius: 0;
  border-top: 1px solid #b1b4b6;
  padding: 45px 0;
}

:deep(body.govuk-theme) .section-header h2 {
  font-family: "GDS Transport", arial, sans-serif;
  font-weight: 700;
  font-size: 24px;
  color: #0b0c0c;
}

:deep(body.govuk-theme) .feature-card {
  border-radius: 0;
  border: 1px solid #b1b4b6;
}

:deep(body.govuk-theme) .feature-card:hover {
  transform: none;
  box-shadow: none;
}

:deep(body.govuk-theme) .feature-icon {
  background-color: #1d70b8;
  border-radius: 0;
}

.features-section {
  padding: var(--spacing-2xl) 0;
  background-color: white;
  border-radius: var(--radius-lg);
  margin-top: var(--spacing-2xl);
}

.section-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.section-header h2 {
  margin-bottom: var(--spacing-sm);
  color: var(--text);
}

.section-header p {
  color: var(--text-light);
}

.feature-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
  margin-top: var(--spacing-xl);
}

.feature-card {
  background-color: white;
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition-normal), box-shadow var(--transition-normal);
  border: 1px solid var(--border);
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-md);
}

.feature-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--primary-light);
  color: white;
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-md);
  padding: var(--spacing-sm);
}

.feature-icon svg {
  width: 24px;
  height: 24px;
}

.feature-card h3 {
  margin-bottom: var(--spacing-sm);
  color: var(--text);
}

.feature-card p {
  color: var(--text-light);
  line-height: 1.6;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-description {
    font-size: 1rem;
  }
  
  .search-form {
    flex-direction: column;
  }
  
  .search-input {
    margin-bottom: var(--spacing-sm);
  }
  
  .feature-cards {
    grid-template-columns: 1fr;
  }
}

/* Dropdown styles */
.search-dropdown {
  position: absolute;
  top: calc(100% + 5px);
  left: 0;
  right: 0;
  background-color: white;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-xl);
  margin-top: 2px;
  z-index: 100;
  max-height: 350px;
  overflow-y: auto;
  border: 1px solid var(--border);
}

.dropdown-header {
  padding: var(--spacing-sm) var(--spacing-md);
  border-bottom: 1px solid var(--border);
  font-size: 0.9rem;
  color: var(--text-light);
  background-color: var(--background);
}

.dropdown-results {
  max-height: 250px;
  overflow-y: auto;
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: var(--spacing-sm) var(--spacing-md);
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: background-color var(--transition-normal);
}

.dropdown-item:hover {
  background-color: rgba(var(--primary-rgb), 0.05);
}

.dropdown-item:last-child {
  border-bottom: none;
}

.record-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  margin-right: var(--spacing-md);
}

.item-icon {
  width: 20px;
  height: 20px;
  color: white;
}

.type-danger {
  background-color: #DC2626;
}

.type-warning {
  background-color: #D97706;
}

.type-success {
  background-color: #059669;
}

.record-info {
  flex: 1;
}

.record-title {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text);
  margin-bottom: 2px;
}

.record-subtitle {
  font-size: 0.8rem;
  color: var(--text-light);
}

.record-badge {
  font-size: 0.7rem;
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: 500;
  text-transform: uppercase;
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

.dropdown-footer {
  padding: var(--spacing-sm) var(--spacing-md);
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: center;
}

.view-all-btn {
  font-size: 0.9rem;
  color: var(--primary);
  font-weight: 500;
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--radius-md);
  transition: background-color var(--transition-normal);
}

.view-all-btn:hover {
  background-color: rgba(var(--primary-rgb), 0.05);
}

.no-results, .loading-results {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-md);
  color: var(--text-light);
  flex-direction: column;
  gap: var(--spacing-sm);
}

.no-results-icon, .loading-icon {
  width: 24px;
  height: 24px;
  color: var(--text-light);
}

.spin {
  animation: spin 1.5s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* GOV.UK styling adjustments for dropdown */
:deep(body.govuk-theme) .search-dropdown {
  border-radius: 0;
  border: 2px solid #0b0c0c;
  box-shadow: none;
}

:deep(body.govuk-theme) .dropdown-header {
  background-color: #f3f2f1;
  font-family: "GDS Transport", arial, sans-serif;
  padding: 10px 15px;
}

:deep(body.govuk-theme) .dropdown-item {
  padding: 15px;
}

:deep(body.govuk-theme) .dropdown-item:hover {
  background-color: #f3f2f1;
}

:deep(body.govuk-theme) .view-all-btn {
  font-family: "GDS Transport", arial, sans-serif;
  color: #1d70b8;
  text-decoration: underline;
}

:deep(body.govuk-theme) .view-all-btn:hover {
  color: #003078;
  background: none;
}
</style> 