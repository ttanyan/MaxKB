import { Result } from '@/request/Result'
import { del, get, post, put } from '@/request'
import { type Ref } from 'vue'

const prefix = '/access_control_policy'

const getPolicyList = (params?: any, loading?: Ref<boolean>): Promise<Result<any>> => {
  return get(prefix, params, loading)
}

const getPolicyDetail = (id: string, loading?: Ref<boolean>): Promise<Result<any>> => {
  return get(`${prefix}/${id}`, undefined, loading)
}

const createPolicy = (data: any, loading?: Ref<boolean>): Promise<Result<any>> => {
  return post(prefix, data, undefined, loading)
}

const updatePolicy = (id: string, data: any, loading?: Ref<boolean>): Promise<Result<any>> => {
  return put(`${prefix}/${id}`, data, undefined, loading)
}

const deletePolicy = (id: string, loading?: Ref<boolean>): Promise<Result<any>> => {
  return del(`${prefix}/${id}`, undefined, undefined, loading)
}

const applyPolicy = (id: string, data: any, loading?: Ref<boolean>): Promise<Result<any>> => {
  return post(`${prefix}/${id}/apply`, data, undefined, loading)
}

const getApplicationRecordList = (params?: any, loading?: Ref<boolean>): Promise<Result<any>> => {
  return get(`${prefix}/application_record`, params, loading)
}

export default {
  getPolicyList,
  getPolicyDetail,
  createPolicy,
  updatePolicy,
  deletePolicy,
  applyPolicy,
  getApplicationRecordList,
}
