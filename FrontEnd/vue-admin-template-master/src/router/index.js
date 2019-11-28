import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    //redirect: '/profile',
    component:Layout,
    children: [{
      path: '/profile',
      name: '个人信息',
      component: () => import('@/views/profile/index'),
      meta: { title: '个人信息', icon: 'dashboard' }
    }]
  },

  {
    path: '/test',
    component: Layout,
    name: '测评练习',
    meta: {
      title: '测评练习',
      icon: 'form'
    },
    children:[
      {
        path: 'exercise',
        component: () => import('@/views/test/exercise/index'), // Parent router-view
        name: '练习',
        meta: { title: '练习' }
        },
      {
        path: 'exam',
        component: () => import('@/views/test/exam/index'),
        name:'考试',
        meta: { title: '考试' }
        },
    ]
  },

  {
    path: '/submit',
    component: Layout,
    children: [
      {
        path: 'index',
        name: '提交题目',
        component: () => import('@/views/submit/index'),
        meta: { title: '提交题目', icon: 'form' }
      }
    ]
  },

  {
    path: '/history',
    component: Layout,
    redirect: '/history/submit',
    name: '历史记录',
    meta: {
      title: '历史记录',
      icon: 'nested'
    },
    children: [
      {
        path: 'submit',
        component: () => import('@/views/history/submit/index'), // Parent router-view
        name: '出题记录',
        meta: { title: '出题记录' }
      },
      {
        path: 'exam',
        component: () => import('@/views/history/exam/index'),
        meta: { title: '考试记录' }
      },
      {
        path: 'exercise',
        component: () => import('@/views/history/exercise/index'),
        meta: { title: '练习记录' }
      }
    ]
  },


  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
