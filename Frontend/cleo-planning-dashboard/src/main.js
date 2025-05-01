import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config'
import { GovUkVue } from 'govuk-vue'
import feather from 'feather-icons'

// Import our custom styles first
import './style.scss'

// Import GOV.UK styles directly from the node_modules
import '../node_modules/govuk-frontend/dist/govuk/govuk-frontend.min.css'

// Initialize Feather Icons - will be re-initialized by components as needed
// This provides fallback initialization and makes icons available for the directive
feather.replace()

// Create a directive for using feather icons
const app = createApp(App)

// Custom directive for feather icons
app.directive('feather', {
  mounted(el, binding) {
    const name = binding.value || binding.arg
    el.innerHTML = feather.icons[name].toSvg()
  },
  updated(el, binding) {
    const name = binding.value || binding.arg
    el.innerHTML = feather.icons[name].toSvg()
  }
})

app.use(PrimeVue, {
  ripple: true,
  inputStyle: 'outlined'
})
app.use(GovUkVue)
app.use(router)
app.mount('#app')
