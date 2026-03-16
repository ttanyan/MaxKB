import { defineStore } from 'pinia'
import menuSettingApi from '@/api/system-settings/menu-setting'
import useUserStore from './user'
import { ALL_MANAGED_MENU_LIST, DEFAULT_MENU_LIST, normalizeMenuList } from '@/utils/menu-setting'

interface MenuSettingState {
  menuList: string[]
  loaded: boolean
}

const useMenuSettingStore = defineStore('menu-setting', {
  state: (): MenuSettingState => ({
    menuList: [],
    loaded: false,
  }),
  actions: {
    reset() {
      this.menuList = []
      this.loaded = false
    },
    setMenuList(menuList: string[]) {
      this.menuList = normalizeMenuList(menuList)
      this.loaded = true
    },
    getMenuList() {
      return this.menuList
    },
    hasMenu(menuId: string) {
      return this.menuList.includes(menuId)
    },
    getDefaultMenuList() {
      const user = useUserStore()
      return user.is_admin() ? [...ALL_MANAGED_MENU_LIST] : [...DEFAULT_MENU_LIST]
    },
    async ensureLoaded() {
      if (this.loaded) {
        return this.menuList
      }
      return this.fetchCurrentMenuSetting()
    },
    async fetchCurrentMenuSetting() {
      const user = useUserStore()
      try {
        const response = await menuSettingApi.getCurrentMenuSetting()
        this.setMenuList(response.data?.menu_list || this.getDefaultMenuList())
      } catch (error) {
        this.setMenuList(this.getDefaultMenuList())
      }
      return this.menuList
    },
  },
})

export default useMenuSettingStore
