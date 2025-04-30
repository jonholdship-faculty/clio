<template>
  <div class="govuk-width-container">
    <gv-header serviceName="Clio Planning Office" />
    
    <div class="govuk-main-wrapper govuk-main-wrapper--auto-spacing" id="main-content">
      <h1 class="govuk-heading-xl">GOV.UK Vue Components Example</h1>
      
      <div class="govuk-grid-row">
        <div class="govuk-grid-column-two-thirds">
          <gv-button>Primary Button</gv-button>
          <gv-button variant="secondary" class="govuk-!-margin-left-2">Secondary Button</gv-button>
          <gv-button variant="warning" class="govuk-!-margin-left-2">Warning Button</gv-button>
          
          <gv-details summary="More information" class="govuk-!-margin-top-6">
            <p class="govuk-body">This is additional information that's hidden by default.</p>
          </gv-details>
          
          <form class="govuk-!-margin-top-6">
            <gv-text-input
              id="full-name"
              label="Full name"
              hint="As shown on your passport or driving licence"
            />
            
            <gv-radios
              id="where-do-you-live"
              name="where-do-you-live"
              class="govuk-!-margin-top-6"
              label="Where do you live?"
              :items="[
                { value: 'england', text: 'England' },
                { value: 'scotland', text: 'Scotland' },
                { value: 'wales', text: 'Wales' },
                { value: 'northern-ireland', text: 'Northern Ireland' }
              ]"
            />
            
            <gv-checkboxes
              id="waste-types"
              name="waste-types"
              class="govuk-!-margin-top-6"
              label="Which types of waste do you transport?"
              hint="Select all that apply"
              :items="[
                { value: 'carcasses', text: 'Waste from animal carcasses' },
                { value: 'mines', text: 'Waste from mines or quarries' },
                { value: 'farm', text: 'Farm or agricultural waste' }
              ]"
            />
            
            <gv-button class="govuk-!-margin-top-6">Submit</gv-button>
          </form>
        </div>
      </div>
    </div>
    
    <gv-footer />
  </div>
</template>

<script setup>
// No imports needed as GOV.UK Vue components are registered globally
</script>

<style>
/* When in GOV.UK theme mode, these styles will help ensure consistent spacing */
.govuk-theme .govuk-width-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
}

.govuk-theme .govuk-main-wrapper {
  padding-top: 20px;
  padding-bottom: 60px;
}

.govuk-theme .govuk-heading-xl {
  margin-bottom: 30px;
}

.govuk-theme .govuk-button {
  margin-right: 10px;
}
</style> 