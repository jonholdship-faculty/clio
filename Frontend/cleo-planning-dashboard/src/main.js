import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config'
import { GovUkVue } from 'govuk-vue'

// Import our custom styles first
import './style.scss'

// Import GOV.UK styles directly from the node_modules
import '../node_modules/govuk-frontend/dist/govuk/govuk-frontend.min.css'

const app = createApp(App)
app.use(PrimeVue, {
  ripple: true,
  inputStyle: 'outlined'
})
app.use(GovUkVue)
app.use(router)
app.mount('#app')
