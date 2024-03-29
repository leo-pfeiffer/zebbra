import { defineNuxtConfig } from 'nuxt'

// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
    runtimeConfig: {
        public: {
            backendUrlBase: process.env.BACKEND_URL_BASE,
        }
    },
    
    buildModules: ['@nuxtjs/tailwindcss', '@pinia/nuxt'],
    app: {
        head: {
            link: [
                { rel: 'stylesheet', href: 'https://rsms.me/inter/inter.css' },
                { rel: 'stylesheet', href: 'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.3/font/bootstrap-icons.css' }
            ]
        }
    },
})