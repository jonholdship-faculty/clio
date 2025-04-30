# Clio Planning Office Dashboard

A Vue.js application for planning offices to search and view records related to addresses.

## Features

- Search for records by address
- Dashboard view with AI-generated summaries for:
  - Enforcement records
  - Appeals
  - Planning applications
- Detailed records table with filtering and sorting
- Responsive design
- Multiple theme options (Default, Dark, Vibrant)

## Project Setup

```sh
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## How to Use

1. On the landing page, enter an address in the search field
2. Click "Search Records" to view the dashboard for that address
3. The dashboard displays AI-generated summaries at the top
4. All records are displayed in a table at the bottom
5. Click the info icon to view detailed information about each record
6. Use the Styles button in the top-right to switch between different visual themes

## Technologies Used

- Vue 3 with Composition API
- PrimeVue for UI components
- Vue Router for navigation
- PrimeFlex for layout
- Custom CSS with variables for theming
