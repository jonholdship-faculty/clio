# AI Reference and Useful Things

## Project Structure
- `/src`: Main source code
  - `/views`: Vue components that serve as page views
  - `/components`: Reusable Vue components
  - `/router`: Vue Router configuration
  - `/data`: Data files and mock data
  - `/assets`: Static assets like images and fonts

## Libraries and Dependencies
- **Vue.js 3**: Frontend framework (v3.5.13)
- **Vue Router**: For routing and navigation
- **PrimeVue**: UI component library for Vue
- **GOV.UK Vue**: GDS design system components for Vue
- **GOV.UK Frontend**: Styling and design system from Government Digital Service
- **Sass**: CSS preprocessor for styling

## Styling Integration
- Using both PrimeVue styling and GOV.UK Frontend styling
- GOV.UK Frontend requires importing `govuk-frontend/dist/govuk/all.scss`
- PrimeVue requires theme files that should be imported in main.js

## Common Issues
- PrimeVue theme import errors: Ensure all PrimeVue resources are properly imported
- Sass deprecation warnings from GOV.UK Frontend: These are expected with the current version

## GOV.UK Vue Integration Notes
- The library is a community resource implementing GDS design system components for Vue
- Components are prefixed with `gv-` (Example: `<gv-button>`)
- Follows accessibility standards from the GOV.UK Design System
- Main plugin is imported as `{ GovUkVue }` from 'govuk-vue'

## Setup Requirements
- For GOV.UK Vue, static assets should be copied from node_modules to the right location
- HTML body should include the classes `js-enabled` and `govuk-frontend-supported`
- For full GOV.UK branding, additional meta tags and link tags are needed in index.html

## Components Available

### GOV.UK Vue Components
- **Layout Components**:
  - `<gv-header>`: Service header with optional navigation
  - `<gv-footer>`: Page footer with links and copyright
  - `<gv-phase-banner>`: Shows alpha/beta phase of service
  - `<gv-width-container>`: Sets content width according to GOV.UK standards

- **Navigation Components**:
  - `<gv-back-link>`: Back navigation link
  - `<gv-breadcrumbs>`: Breadcrumb navigation
  - `<gv-skip-link>`: Accessibility skip link
  - `<gv-pagination>`: Page navigation

- **Form Components**:
  - `<gv-button>`: Standard, secondary, or warning buttons
  - `<gv-text-input>`: Text input field
  - `<gv-textarea>`: Multi-line text input
  - `<gv-checkboxes>`: Checkbox groups
  - `<gv-radios>`: Radio button groups
  - `<gv-select>`: Dropdown select
  - `<gv-date-input>`: Structured date input
  - `<gv-file-upload>`: File upload component
  - `<gv-error-summary>`: Form validation error summary

- **Content Components**:
  - `<gv-details>`: Expandable details section
  - `<gv-inset-text>`: Inset text block
  - `<gv-panel>`: Confirmation panel
  - `<gv-table>`: Structured data table
  - `<gv-tabs>`: Tabbed interface
  - `<gv-tag>`: Status tag indicator
  - `<gv-warning-text>`: Warning message
  - `<gv-summary-list>`: Key/value summary list

### PrimeVue Components
- DataTable, advanced inputs, charts (see PrimeVue documentation)

## CSS Utility Classes
GOV.UK Frontend provides utility classes for spacing, typography, and other common needs:

- **Spacing**:
  - `govuk-!-margin-{direction}-{size}`: Add margin 
  - `govuk-!-padding-{direction}-{size}`: Add padding
  - Directions: `top`, `right`, `bottom`, `left`
  - Sizes: `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`

- **Typography**:
  - `govuk-heading-xl`, `govuk-heading-l`, `govuk-heading-m`, `govuk-heading-s`: Heading sizes
  - `govuk-body`, `govuk-body-l`, `govuk-body-s`: Text sizes
  - `govuk-list`: Standard list

- **Layout**:
  - `govuk-grid-row`: Row container
  - `govuk-grid-column-{width}`: Column width (e.g., `govuk-grid-column-two-thirds`)

## Example Usage
See `/src/components/GovUkExample.vue` for examples of how to use GOV.UK Vue components.

## Data Structures
- Any specific data structures used in the application will be documented here as they are identified 