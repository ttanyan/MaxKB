export const DEFAULT_MENU_LIST = ['knowledge']

export const ALL_MANAGED_MENU_LIST = ['application', 'mindmap', 'knowledge', 'tool', 'model']

export const MENU_PATH_MAP: Record<string, string> = {
  application: '/application',
  mindmap: '/mindmap',
  knowledge: '/knowledge',
  tool: '/tool',
  model: '/model',
}

export function normalizeMenuList(menuList: string[] | undefined | null): string[] {
  const validMenuList = new Set(ALL_MANAGED_MENU_LIST)
  const uniqueMenuList = new Set<string>()
  ;(menuList || []).forEach((menuId) => {
    if (validMenuList.has(menuId)) {
      uniqueMenuList.add(menuId)
    }
  })
  return [...uniqueMenuList]
}

export function resolveMenuIdByPath(path: string): string | null {
  if (path.startsWith('/application')) return 'application'
  if (path.startsWith('/mindmap')) return 'mindmap'
  if (path.startsWith('/knowledge')) return 'knowledge'
  if (path.startsWith('/tool')) return 'tool'
  if (path.startsWith('/model')) return 'model'
  return null
}

export function getFirstAvailableMenuPath(menuList: string[]): string {
  const normalizedMenuList = normalizeMenuList(menuList)
  const preferredMenuList = [
    'knowledge',
    'application',
    'mindmap',
    'tool',
    'model',
  ]

  for (const menuId of preferredMenuList) {
    if (normalizedMenuList.includes(menuId)) {
      return MENU_PATH_MAP[menuId]
    }
  }

  return '/no-permission'
}
