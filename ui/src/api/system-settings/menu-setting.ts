import { Result } from '@/request/Result'
import { get, put } from '@/request/index'
import { type Ref } from 'vue'

const prefix = '/menu_setting'

const getMenuSetting = (loading?: Ref<boolean>): Promise<Result<any>> => {
  return get(prefix, undefined, loading)
}

const getCurrentMenuSetting = (loading?: Ref<boolean>): Promise<Result<any>> => {
  return get(`${prefix}/current`, undefined, loading)
}

const putMenuSetting = (data: any, loading?: Ref<boolean>): Promise<Result<any>> => {
  return put(prefix, data, undefined, loading)
}

export default {
  getMenuSetting,
  getCurrentMenuSetting,
  putMenuSetting,
}
