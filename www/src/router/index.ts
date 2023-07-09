// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/Home.vue'),
  },
  {
    path: '/privacy',
    name: 'Privacy Policy',
    component: () => import('@/layouts/Privacy.vue'),
  },
  {
    path: '/terms',
    name: 'Terms of Service',
    component: () => import('@/layouts/Terms.vue'),
  },
  {
    path: '/dashboard',
    component: () => import('@/layouts/dashboard/Dashboard.vue'),
    redirect: { name: 'Overview' },
    children: [
      {
        path: 'overview',
        name: 'Overview',
        component: () => import('@/views/Overview.vue'),
      },
      {
        path: 'data',
        name: 'Data Explorer',
        component: () => import('@/views/DataExplorer.vue'),
      },
      {
        path: 'ecpm',
        name: 'Network eCPM',
        component: () => import('@/views/NetworkECPM.vue'),
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/Settings.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

router.afterEach((to) => {
  document.title = to.name ? (to.name as string + " - Watchtower") : 'AdMob Watchtower';
})

export default router
