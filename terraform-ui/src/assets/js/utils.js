import { validate } from './validate'
const colorSet = ['#487e89', '#395b79', '#153863', '#153250']
// const colorSet = ['#61a0a8', '#2f4554', '#c23531', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074', '#546570', '#c4ccd3']
export function generateUuid () {
  return new Promise(resolve => {
    resolve(guid())
  })
}

export function randomColor () {
  let index = Math.floor(Math.random() * colorSet.length)
  return new Promise(resolve => {
    resolve(colorSet[index])
  })
}

function guid () {
  return 'xxxxxxxx_xxxx_4xxx_yxxx_xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    // eslint-disable-next-line one-var
    let r = (Math.random() * 16) | 0,
      v = c === 'x' ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}

/*
 * Func: 按要求截取字符串
 *
 * @param {String} value (待截取字符串)
 * @param {Int} maxLen (最大长度)
 */
export function interceptParams (value = '', maxLen = 20) {
  if (validate.isEmpty_reset(value)) {
    return ''
  }
  if (value.length > maxLen) {
    return value.substring(0, maxLen) + '...'
  }
  return value
}

export function isJSONStr (str) {
  if (typeof str === 'string') {
    try {
      var obj = JSON.parse(str)
      if (typeof obj === 'object' && obj) {
        return true
      } else {
        return false
      }
    } catch (e) {
      return false
    }
  }
}
