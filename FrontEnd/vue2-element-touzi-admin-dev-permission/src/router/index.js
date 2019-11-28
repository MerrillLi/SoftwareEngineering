import Vue from 'vue'
import Router from 'vue-router'
import {Layout, Content} from "../layout"; // 页面整体布局
import {topRouterMap} from "./topRouter";

process.env.NODE_ENV === "development" ? Vue.use(Router) : null;

function filterTopRouterMap(name) {
    let router = topRouterMap.find((item) => {
        return item.parentName === name;
    });
    return router.data; // arr
}

//手动跳转的页面白名单
const whiteList = [
    '/'
];

//默认不需要权限的页面
export const constantRouterMap = [
    {
        path: '',
        component: Layout,
        redirect: '/index/index',
        hidden: true
    },
    {path: '/login', name: 'login', component: () => import('@/page/login'), hidden: true},
    {path: '/404', component: () => import('@/page/errorPage/404'), hidden: true},
    {path: '/401', component: () => import('@/page/errorPage/401'), hidden: true},
    {
        path: '/index',
        name: 'index',
        component: Layout,
        meta: {
            title: '首页',
            icon: 'icondashboard',
        },
        noDropdown: true,
        children: [
            {
                path: 'index',
                meta: {
                    title: '首页',
                    icon: 'icondashboard',
                    routerType: 'leftmenu'
                },
                component: () => import('@/page/index/infoShow'),
            }
        ]
    }
]

//注册路由
export default new Router({
    mode: 'history', // 默认为'hash'模式
    base: '/permission/', // 添加跟目录,对应服务器部署子目录
    routes: constantRouterMap
})

//异步路由（需要权限的页面）
export const asyncRouterMap = [
    {
        path: '/userManager',
        name: 'userManage',
        component: Layout,
        meta: {
            title: '用户管理',
            icon: 'iconuser',
        },
        noDropdown: true,
        children: [
            {
                path: 'userList',
                meta: {
                    title: '用户管理',
                    icon: 'iconuser',
                    routerType: 'leftmenu'
                },
                component: () => import('@/page/Exercise/exercise'),
            }
        ]
    },
    {
        path: '/submit',
        name: 'infoManage',
        meta: {
            title: '信息管理',
            icon: 'iconinfo',
        },
        component: Layout,
        children: [
            {
                path: 'infoShow',
                name: 'infoShow',
                meta: {
                    title: '个人信息',
                    icon: 'iconinfo',
                    routerType: 'leftmenu',

                },
                component: () => import('@/page/submit/infoShow'),
            },
            {
                path: 'infoModify',
                name: 'infoModify',
                meta: {
                    title: '修改信息',
                    icon: 'iconinfo',
                    routerType: 'leftmenu'
                },
                component:() => import('@/page/submit/infoModify'),
            }
        ]
    },
    {
        path: '/fundManage',
        name: 'fundManage',
        meta: {
            title: '资金管理',
            icon: 'iconpay3',
        },
        noDropdown: true,
        component: Layout,
        children: [
            {
                path: 'fundList',
                name: 'fundList',
                meta: {
                    title: '资金流水',
                    routerType: 'leftmenu'
                },
                component: () => import('@/page/fundList/fundList'),
            }
        ]
    },

    {path: '*', redirect: '/404', hidden: true}
];
