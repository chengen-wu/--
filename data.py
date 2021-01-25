import json
import requests
import time
import random
from pyquery import PyQuery as pq


def get_content(id):
    url = 'https://m.weibo.cn/statuses/extend'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }
    param = {
        'id': id
    }
    response = requests.get(url=url, params=param, headers=headers)
    return pq(response.json()['data']['longTextContent']).text()


def get_comment(mid, scheme, cookie):
    url = 'https://m.weibo.cn/comments/hotflow'
    headers = {
        'Accept': 'application / json, text / plain, * / *',
        'MWeibo-Pwa': '1',
        'Referer': scheme,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'X-XSRF-TOKEN': '7d6690',
        'cookie': cookie
    }
    param = {
        'id': mid,
        'mid': mid,
        'max_id_type': '0'
    }
    response = requests.get(url=url, params=param, headers=headers)
    comment_page = response.json()
    if comment_page['ok'] == 0:
        return []
    comment_content = []
    for user in comment_page['data']['data']:
        comment_content.append(pq(user['text']).text())
    if comment_page['data']['max_id'] != 0:
        while True:
            try:
                param['max_id'] = comment_page['data']['max_id']
                response = requests.get(url=url, params=param, headers=headers)
                comment_page = response.json()
                if comment_page['ok'] == 0:
                    break
                for user in comment_page['data']['data']:
                    comment_content.append(pq(user['text']).text())
                if comment_page['data']['max_id'] == 0:
                    break
                time.sleep(1 + random.random() * 2)
            except Exception as e:
                print(e)
                headers['cookie'] = input('cookie')
                headers['X-XSRF-TOKEN'] = input('token')
                continue
    return comment_content


if __name__ == "__main__":
    sina_headers = {
        'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }

    # 微博用户主页api通用url
    url = 'https://m.weibo.cn/api/container/getIndex'

    # 所有要爬的用户的uid
    uid_list = ['2028810631', '1887802145', '2140585607', '1796087453', '2810373291']

    # 最外层循环，每次爬取完成一个用户
    for uid in uid_list:
        # 设置参数，url+parm得到特定用户主页api
        param = {
            'type': 'uid',
            'value': uid,
        }
        # #发起请求，得到用户主页
        response = requests.get(url=url, params=param, headers=sina_headers)
        # #将页面内容中的json转化为字典并赋值给homepage
        homepage = response.json()
        # 查询该字典，获取该user的有关信息以及爬取其发布微博必备参数containerid
        # 将user的信息存进字典
        user_Info_dic = {
            '微博用户名': homepage['data']['userInfo']['screen_name'],
            '微博主页地址': homepage['data']['userInfo']['profile_url'],
            '微博认证名': homepage['data']['userInfo']['verified_reason'],
            '微博说明': homepage['data']['userInfo']['description'],
            '关注数量': homepage['data']['userInfo']['follow_count'],
            '粉丝数量': homepage['data']['userInfo']['followers_count'],
        }
        # 将该字典存入文件，并覆盖原文件
        with open('sinanews3.text', 'w', encoding='utf-8') as fp:
            fp.write(json.dumps(user_Info_dic, indent=4, separators=(',', ':'), ensure_ascii=False))
            fp.write('\n')
            # 取containerid
        tab_list = homepage['data']['tabsInfo']['tabs']
        containerid = ''
        for tab in tab_list:
            if (tab['tabKey'] == 'weibo'):
                containerid = tab['containerid']
            # 将containerid参数加入parm，此时通过url+parm就可以爬取到包含该user发布微博内容的第一个数据包
        param['containerid'] = containerid
        fp = open('sinanews3.text', 'a', encoding='utf-8')
        # 不断发起请求，获取用户微博内容
        i = 0
        pagen = 1501
        err = False
        begin = False
        count = 0
        page = homepage
        cookie = input('firstcookie')
        sina_headers['cookie'] = cookie
        while True:
            pagen += 1
            param['page'] = str(pagen)
            response = requests.get(url=url, params=param, headers=sina_headers)
            page = response.json()
            for card in page['data']['cards']:
                try:
                    if card['card_type'] == 9:

                        print(card['mblog']['created_at'])
                        content_dic = {
                            "微博地址:": card['scheme'],
                            "发布时间": card['mblog']['created_at'],
                            "转发数": card['mblog']['reposts_count'],
                            "评论数": card['mblog']['comments_count'],
                            "点赞数:": card['mblog']['attitudes_count'],
                            "微博内容:": get_content(card['mblog']['id']),
                            "评论": get_comment(card['mblog']['mid'], card['scheme'], sina_headers['cookie'])
                        }
                        fp.write(json.dumps(content_dic, indent=4, separators=(',', ':'), ensure_ascii=False))
                        fp.write('\n')
                        fp.flush()
                        print('爬' + str(i))
                        i += 1
                # time.sleep((int)(7+random.random()*5))
                # since_id=page['data']['cardlistInfo']['since_id']
                # param['since_id']=since_id
                except Exception as e:
                    count += 1
                    if count == 5:
                        print(pagen)
                        sina_headers['cookie'] = input('cookie')
                        count = 0
                        continue
                    else:
                        continue
