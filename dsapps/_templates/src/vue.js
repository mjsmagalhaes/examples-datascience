import { createApp } from "vue";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library, dom } from "@fortawesome/fontawesome-svg-core";
import { faSliders, faCoffee } from '@fortawesome/free-solid-svg-icons'
library.add(faCoffee, faSliders);
dom.watch()

import Example from './example.vue';

if (process.env.NODE_ENV === "development") {
    globalThis.__VUE_OPTIONS_API__ = true
    globalThis.__VUE_PROD_DEVTOOLS__ = true;
} else {
    // different values for production.
    globalThis.__VUE_OPTIONS_API__ = false;
    globalThis.__VUE_PROD_DEVTOOLS__ = false;
}

const app = createApp(Example);
app.component("font-awesome-icon", FontAwesomeIcon).mount("#app");