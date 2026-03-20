import { Result } from '@/request/Result'
import { get } from '@/request/index'
import { type Ref } from 'vue'

/**
 * 获取系统配置
 */
const getSystemConfig: (loading?: Ref<boolean>) => Promise<Result<any>> = (loading) => {
  return get('/system_manage/config', undefined, loading)
}

export default {
  getSystemConfig
}
