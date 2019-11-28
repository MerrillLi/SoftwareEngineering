import request from '@/utils/axios'


export function login(params) {
    return request({
        url: 'api/user/login/',
        method: 'post',
        data: params
    })
}

export function logout(params) {
    return request({
        url: '/api/user/logout',
        method: 'get',
        data: params
    })
}


export function getUserInfo(params) {
    return request({
        url: '/user/info/get',
        method: 'get',
        data: params
    })
}

export function getUserList(reqData) {
    return request({
        url: '/user/list/get',
        method: 'get',
        data: reqData
    })
}


