import ConditioNodeVue from './index.vue'
import { cloneDeep, set } from 'lodash'
import { AppNode, AppNodeModel } from '@/workflow/common/app-node'
class ConditioNode extends AppNode {
  constructor(props: any) {
    super(props, ConditioNodeVue)
  }
}
const get_up_index_height = (condition_list: Array<any>, index: number) => {
  return condition_list
    .filter((item, i) => i < index)
    .map((item) => item.height + 8)
    .reduce((x, y) => x + y, 0)
}
class ConditionModel extends AppNodeModel {
  refreshBranch() {
    // 更新节点连接边的path
    this.incoming.edges.forEach((edge: any) => {
      // 调用自定义的更新方案
      edge.updatePathByAnchor()
    })
    this.outgoing.edges.forEach((edge: any) => {
      edge.updatePathByAnchor()
    })
  }
  getDefaultAnchor() {
    const {
      id,
      x,
      y,
      width,
      height,
      properties: { branch_condition_list }
    } = this
    if (this.height === undefined) {
      this.height = 200
    }
    const showNode = this.properties.showNode === undefined ? true : this.properties.showNode
    const anchors: any = []
    anchors.push({
      x: x - width / 2 + 10,
      y: showNode ? y : y - 15,
      id: `${id}_left`,
      edgeAddable: false,
      type: 'left'
    })

    const conditionList = Array.isArray(branch_condition_list) ? branch_condition_list : []
    if (conditionList.length > 0) {
      for (let index = 0; index < conditionList.length; index++) {
        const element = conditionList[index]
        const h = get_up_index_height(conditionList, index)
        anchors.push({
          x: x + width / 2 - 10,
          y: showNode ? y - height / 2 + 75 + h + (element.height || 0) / 2 : y - 15,
          id: `${id}_${element.id}_right`,
          type: 'right'
        })
      }
    }

    return anchors
  }
}
export default {
  type: 'condition-node',
  model: ConditionModel,
  view: ConditioNode
}
