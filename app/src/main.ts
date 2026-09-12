import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import { router } from './router'
import { useArchive } from './stores/archive'
import './styles/base.css'
import 'katex/dist/katex.min.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)

// 存档初始化完成后再挂载，避免首帧读不到进度
useArchive().init().finally(() => app.mount('#app'))
