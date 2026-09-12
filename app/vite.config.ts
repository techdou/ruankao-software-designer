import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

// https://vite.dev/config/
// base './'：构建产物使用相对资源路径，配合 hash 路由可直接部署在
// GitHub Pages 项目子路径（/<repo>/）下，无需按仓库名硬编码 base。
export default defineConfig({
  base: './',
  plugins: [vue()],
})
