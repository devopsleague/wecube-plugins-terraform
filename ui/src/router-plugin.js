import terraformIndex from '@/pages/terraform-index'
import conversionConfiguration from '@/pages/conversion-configuration'
import pluginDefinition from '@/pages/plugin-definition'
import templateData from '@/pages/template-data'
const router = [
  {
    path: '/terraformIndex',
    name: 'terraformIndex',
    component: terraformIndex,
    params: {},
    props: true,
    redirect: '/terraformIndex/templateData',
    children: [
      {
        path: 'templateData',
        name: 'templateData',
        title: '模板数据',
        meta: {},
        component: templateData
      },
      {
        path: 'conversionConfiguration',
        name: 'conversionConfiguration',
        title: '转换配置',
        meta: {},
        component: conversionConfiguration
      },
      {
        path: 'pluginDefinition',
        name: 'pluginDefinition',
        title: '插件定义',
        meta: {},
        component: pluginDefinition
      }
    ]
  }
]
export default router
