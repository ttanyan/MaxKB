import { hasPermission, set_next_route } from '@/utils/permission/index'
import { getChildRouteList } from '@/router/common'
import NProgress from 'nprogress'
import { getPermissionRoute } from '@/router/common'
import {
  createRouter,
  createWebHistory,
  type NavigationGuardNext,
  type RouteLocationNormalized,
  type RouteRecordName,
} from 'vue-router'
import useStore from '@/stores'
import { routes } from '@/router/routes'
import { getFirstAvailableMenuPath, resolveMenuIdByPath } from '@/utils/menu-setting'
NProgress.configure({ showSpinner: false, speed: 500, minimum: 0.3 })
const router = createRouter({
  history: createWebHistory(window.MaxKB?.prefix ? window.MaxKB?.prefix : import.meta.env.BASE_URL),
  routes: routes,
})

// 路由前置拦截器
router.beforeEach(
  async (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
    NProgress.start()
    if (to.name === '404') {
      next()
      return
    }
    const { user, login, menuSetting } = useStore()

    const notAuthRouteNameList = ['login', 'ForgotPassword', 'ResetPassword', 'Chat', 'UserLogin']
    if (!notAuthRouteNameList.includes(to.name ? to.name.toString() : '')) {
      if (to.query && to.query.token) {
        localStorage.setItem('token', to.query.token.toString())
      }
      const token = login.getToken()
      if (!token) {
        next({
          path: '/login',
        })
        return
      }
      if (!user.userInfo) {
        await user.profile()
      }
      await menuSetting.ensureLoaded()
    }
    set_next_route(to)
    const menuId = resolveMenuIdByPath(to.path)
    if (menuId && !user.is_admin() && !menuSetting.hasMenu(menuId)) {
      const availablePath = getFirstAvailableMenuPath(menuSetting.getMenuList())
      next(availablePath === '/no-permission' ? { name: 'noPermission' } : { path: availablePath })
      return
    }
    // 判断是否有菜单权限
    if (to.meta.permission ? hasPermission(to.meta.permission as any, 'OR') : true) {
      if(to.name=='noPermissionD'){
         const n = getPermissionRoute(routes, to)
         if(n.name=='noPermission'){
          next()
          return
         }else{
          next(n)
          return
         }
      }else{
        next()
      }
    } else {
      const n = getPermissionRoute(routes, to)
      next(n)
    }
  },
)
router.afterEach(() => {
  NProgress.done()
})
export const getChildRouteListByPathAndName = (path: any, name?: RouteRecordName | any) => {
  return getChildRouteList(routes, path, name)
}

export default router
