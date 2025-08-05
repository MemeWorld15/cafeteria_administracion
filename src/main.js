import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
// Elimina la importación de Font Awesome:
// import '@fortawesome/fontawesome-free/css/all.min.css'

// Opcional: Si quieres usar Iconify globalmente, puedes importar el componente Icon
import { Icon } from '@iconify/vue';

const app = createApp(App);
app.use(router);

// Registra el componente Icon globalmente (opcional)
app.component('Icon', Icon);

app.mount('#app');