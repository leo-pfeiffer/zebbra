import { defineNuxtConfig } from 'nuxt'

// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
    modules: ['@nuxtjs/tailwindcss'],
    app: {
        head: {
            link: [
                { rel: 'stylesheet', href: 'https://rsms.me/inter/inter.css' }
            ]
        }
    }
})
