// import { createApp } from "vue";
import { createApp } from 'vue/dist/vue.esm-bundler';
import { createRouter, createWebHashHistory } from 'vue-router'

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library, dom } from "@fortawesome/fontawesome-svg-core";
import { faSliders, faCoffee } from '@fortawesome/free-solid-svg-icons'
library.add(faCoffee, faSliders);
dom.watch()

import Index from './index.vue'
import Example from './example.vue';

if (process.env.NODE_ENV === "development") {
    globalThis.__VUE_OPTIONS_API__ = false
    globalThis.__VUE_PROD_DEVTOOLS__ = true;
} else {
    // different values for production.
    globalThis.__VUE_OPTIONS_API__ = false;
    globalThis.__VUE_PROD_DEVTOOLS__ = false;
}

const router = createRouter({
    history: createWebHashHistory('/datacrawler/'),
    routes: [
        { path: '/', component: Index },
        { path: '/raids', component: Example }
    ]
})

const app = createApp({});
app.use(router)
app.component("font-awesome-icon", FontAwesomeIcon).mount("#vue");