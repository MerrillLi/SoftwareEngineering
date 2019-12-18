import store from './store'
import {Message} from 'element-ui'
import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css' // progress bar style
import {getToken} from '@/utils/auth' // get token from cookie
import getPageTitle from '@/utils/get-page-title'
import router from './router'
import permission from './store/permission'

NProgress.configure({showSpinner: false}); // NProgress Configuration

const whiteList = ['/login']; // no redirect whitelist


//
router.beforeEach(async (to, from, next) => {

  // start progress bar
  NProgress.start();

  // set page title
  document.title = getPageTitle(to.meta.title);

  // determine whether the user has logged in
  const hasToken = getToken();

  if (hasToken) {
    if (to.path === '/login') {
      // if is logged in, redirect to the home page
      next({path: '/'});
      NProgress.done()
    } else {
      const hasGetUserInfo = store.getters.name;

      //const role = Vue.prototype.$role;
      const role = localStorage.getItem('role');

      const asyncRouter = permission.actions.GenerateRoutes(role);

      // 动态添加可访问路由表
      if (router.options.routes.length <= 4) {
        for (let i = 0; i < asyncRouter.length; i++) {
          router.options.routes.push(asyncRouter[i])
        }

        router.options.routes.push(
          {path: '*', redirect: '/', hidden: true}
        );
        router.addRoutes(asyncRouter);
        next({...to, replace: true})
      }

      console.log(router);
      if (hasGetUserInfo) {

        next()
      } else {
        try {

          next();
          NProgress.done()
        } catch (error) {
          Message.error(error || 'Has Error');
          next(`/login?redirect=${to.path}`);
          NProgress.done()
        }
      }
    }
  } else {
    /* has no token*/

    if (whiteList.indexOf(to.path) !== -1) {
      // in the free login whitelist, go directly
      next()
    } else {
      // other pages that do not have permission to access are redirected to the login page.
      next(`/login?redirect=${to.path}`);
      NProgress.done()
    }
  }


});

router.afterEach(() => {
  // finish progress bar
  NProgress.done();
});
