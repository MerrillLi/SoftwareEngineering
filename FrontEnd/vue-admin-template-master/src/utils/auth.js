import Cookies from 'js-cookie'
import router from '../router'

const TokenKey = 'vue_admin_template_token';

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

export function checkExpire(res) {
  if (res.data.msg === 'expire') {
    router.push(`/login`);
    this.$notify.error('登陆过期，请重新登陆');
  }
}
