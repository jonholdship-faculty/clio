<template>
  <div>
    <gv-skip-link href="#main-content">Skip to main content</gv-skip-link>
    
    <gv-header serviceName="Planning Records Service" />
    
    <div class="govuk-width-container">
      <gv-phase-banner phase="beta">
        This is a new service – your <a href="#" class="govuk-link">feedback</a> will help us to improve it.
      </gv-phase-banner>
      
      <gv-back-link @click="goBack">Back</gv-back-link>
      
      <main class="govuk-main-wrapper" id="main-content" role="main">
        <h1 class="govuk-heading-xl">GOV.UK Style Component</h1>
        
        <p class="govuk-body">This is an example GOV.UK style component showing various GDS design elements.</p>
        
        <gv-notification-banner title="Important">
          <p class="govuk-notification-banner__heading">
            Select the "GOV.UK" option from the styles dropdown to see the full GOV.UK styling.
          </p>
        </gv-notification-banner>
        
        <div class="govuk-grid-row">
          <div class="govuk-grid-column-two-thirds">
            <h2 class="govuk-heading-m">Submit your planning application</h2>
            
            <form class="govuk-form">
              <gv-text-input
                id="applicant-name"
                label="Full name"
                hint="As shown on your passport or driving licence"
              />
              
              <gv-date-input
                id="application-date"
                label="Application date"
                hint="For example, 27 3 2023"
                class="govuk-!-margin-top-6"
              />
              
              <gv-radios
                id="application-type"
                name="application-type"
                class="govuk-!-margin-top-6"
                label="What type of planning application is this?"
                :items="[
                  { value: 'householder', text: 'Householder application' },
                  { value: 'full', text: 'Full planning permission' },
                  { value: 'outline', text: 'Outline planning permission' },
                  { value: 'reserved', text: 'Reserved matters' }
                ]"
              />
              
              <gv-checkboxes
                id="contact-methods"
                name="contact-methods"
                class="govuk-!-margin-top-6"
                label="How would you like to be contacted?"
                hint="Select all that apply"
                :items="[
                  { value: 'email', text: 'Email' },
                  { value: 'phone', text: 'Phone' },
                  { value: 'post', text: 'Post' }
                ]"
              />
              
              <gv-button class="govuk-!-margin-top-6">Submit application</gv-button>
            </form>
            
            <gv-details summary="Help with planning applications" class="govuk-!-margin-top-6">
              <p class="govuk-body">
                Planning applications are submitted to your local planning authority (LPA), usually your council. 
                Applications can be made online through the Planning Portal.
              </p>
            </gv-details>
          </div>
          
          <div class="govuk-grid-column-one-third">
            <gv-inset-text>
              This column contains additional information and guidance about your planning application.
            </gv-inset-text>
            
            <gv-warning-text>
              Failure to provide accurate information may result in your application being rejected.
            </gv-warning-text>
            
            <h3 class="govuk-heading-s govuk-!-margin-top-6">Planning application fee</h3>
            <gv-table caption="Fee table" captionClass="govuk-visually-hidden">
              <template #head>
                <tr>
                  <th scope="col">Application type</th>
                  <th scope="col">Fee</th>
                </tr>
              </template>
              <template #body>
                <tr>
                  <td>Householder</td>
                  <td>£206</td>
                </tr>
                <tr>
                  <td>Full (new dwelling)</td>
                  <td>£462 per dwelling</td>
                </tr>
                <tr>
                  <td>Listed building consent</td>
                  <td>£0</td>
                </tr>
              </template>
            </gv-table>
          </div>
        </div>
        
        <div class="govuk-!-margin-top-9">
          <h2 class="govuk-heading-m">See your application status</h2>
          <gv-tabs>
            <gv-tab id="tab1" label="Current applications">
              <h3 class="govuk-heading-s">Current applications</h3>
              <p class="govuk-body">You have 2 applications in progress.</p>
              <gv-summary-list>
                <gv-summary-list-row key="Application reference" value="PA/2023/001" />
                <gv-summary-list-row key="Submitted" value="15 March 2023" />
                <gv-summary-list-row key="Status" value="Under review">
                  <template #actions>
                    <gv-link href="#">View</gv-link>
                  </template>
                </gv-summary-list-row>
              </gv-summary-list>
            </gv-tab>
            <gv-tab id="tab2" label="Past applications">
              <h3 class="govuk-heading-s">Past applications</h3>
              <p class="govuk-body">You have 3 completed applications.</p>
            </gv-tab>
            <gv-tab id="tab3" label="Saved drafts">
              <h3 class="govuk-heading-s">Saved drafts</h3>
              <p class="govuk-body">You have 1 draft application.</p>
            </gv-tab>
          </gv-tabs>
        </div>
      </main>
    </div>
    
    <gv-footer />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const goBack = () => {
  router.go(-1);
};
</script>

<style scoped>
/* GOV.UK specific spacing and margins */
.govuk-theme .govuk-width-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
}

.govuk-theme .govuk-phase-banner {
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #b1b4b6;
}

.govuk-theme .govuk-back-link {
  margin-bottom: 30px;
  display: inline-block;
}

.govuk-theme .govuk-main-wrapper {
  padding-top: 20px;
  padding-bottom: 60px;
}

.govuk-theme .govuk-notification-banner {
  margin-bottom: 30px;
}

.govuk-theme .govuk-grid-column-two-thirds,
.govuk-theme .govuk-grid-column-one-third {
  box-sizing: border-box;
  padding: 0 15px;
}

.govuk-theme .govuk-heading-xl {
  margin-top: 30px;
  margin-bottom: 30px;
}

.govuk-theme .govuk-heading-m {
  margin-top: 45px;
  margin-bottom: 20px;
}

.govuk-theme .govuk-button {
  margin-right: 10px;
}

.govuk-theme .govuk-table {
  width: 100%;
  margin-bottom: 30px;
}

.govuk-theme .govuk-summary-list {
  margin-bottom: 30px;
}

.govuk-theme .govuk-tabs {
  margin-bottom: 30px;
}

/* When not in GOV.UK theme, provide some basic spacing */
:not(.govuk-theme) .govuk-width-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style> 