import json
import requests
import time
import random
from pyquery import PyQuery as pq

# 获取微博标题和正文内容
def get_content(id):
    url = 'https://m.weibo.cn/statuses/extend' #通用url
    # headers对爬虫进行伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
        'X-Requested-With': 'XMLHttpRequest'
    }
    # 所需参数
    param = {
        'id': id
    }
    # 发起请求
    response = requests.get(url=url,params=param,headers=headers)
    # 得到所需内容并格式化后返回
    return pq(response.json()['data']['longTextContent']).text()

# 获取某条微博的评论（理论上时所有评论，实际上会因为各种返回数据的错误而使得最终得到的评论数少于所有评论数，但已经很多了）
def get_comment(mid, scheme, cookie):
    url = 'https://m.weibo.cn/comments/hotflow' # 通用url
    # headers对爬虫进行伪装
    headers = {
        'Accept': 'application / json, text / plain, * / *',
        'MWeibo-Pwa': '1',
        'Referer': scheme,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
        'X-Requested-With': 'XMLHttpRequest',
        'cookie': cookie
    }
    # 所需参数
    param = {
        'id': mid,
        'mid': mid,
        'max_id_type': '0'
    }
    # 发起请求
    response = requests.get(url=url, params=param, headers=headers)
    # comment_page储存每个包中的数据
    comment_page = response.json()
    # 如果该微博没有评论直接结束，返回{}
    if comment_page['ok'] == 0:
        return []
    # comment_content储存爬取到的所有评论
    comment_content = []
    # 将数据包中的评论一条条添加到comment_content中
    for user in comment_page['data']['data']:
        comment_content.append(pq(user['text']).text())
    # max_id时comment_page中的一个参数，提供指向下一个数据包所需参数。若为0则已经爬完
    if comment_page['data']['max_id'] != 0:
        # 循环获取下一个包，得到其中评论数据
        while True:
            # 异常处理机制，试过各种处理，想让其出错后重新获取该数据并继续向下爬，但是效果并不理想，且对爬虫进度造成了极大干扰，最后选择了直接break，效果不错
            try:
                # 将max_id加入param中，使得param中的参数指向下一个数据包
                param['max_id'] = comment_page['data']['max_id']
                # 发出请求
                response = requests.get(url=url, params=param, headers=headers)
                # 存储数据
                comment_page = response.json()
                # 该数据包出错，终止该微博的评论爬取
                if comment_page['ok'] == 0:
                    break
                # 将数据包中的评论一条条添加到comment_content中
                for user in comment_page['data']['data']:
                    comment_content.append(pq(user['text']).text())
                # 该微博评论已经爬完
                if comment_page['data']['max_id'] == 0:
                    break
                # 起初没有sleep，被微博418警告。于是添加sleep降低爬虫速度，random使时间间隔不相同，让该程序看起来更不像是爬虫
                time.sleep(1+random.random()*2)
            except Exception as e:
                break  # 异常直接break
    return comment_content  # 返回评论数据


if __name__ == "__main__":
    # 初始headers，进行UA伪装
    sina_headers = {
        'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
    }

    # 微博用户主页api通用url
    url = 'https://m.weibo.cn/api/container/getIndex'

    # 所有要爬的用户的uid（最初的设计是将要爬取的用户的uid全部储存在该列表中，循环爬取。后来发现每一个都要爬很长时间，并且可能会因为网络等原因中止，所以就一个一个爬了）
    uid_list = ['2028810631']

    # 最外层循环，每次爬取完成一个用户
    for uid in uid_list:
        # 设置参数，url+parm得到特定用户主页api
        param = {
            'type': 'uid',
            'value': uid,
        }
        # 发起请求，得到用户主页
        response = requests.get(url=url, params=param, headers=sina_headers)
        # 将页面内容中的json转化为python字典并赋值给homepage
        homepage = response.json()
        # 查询该字典，获取该user的有关信息以及爬取其发布微博必备参数containerid
        # 将user的信息存进字典（通过json在线格式化工具，找到所需内容所在位置，详情见文档）
        user_Info_dic = {
            '微博用户名': homepage['data']['userInfo']['screen_name'],
            '微博主页地址': homepage['data']['userInfo']['profile_url'],
            '微博认证名': homepage['data']['userInfo']['verified_reason'],
            '微博说明': homepage['data']['userInfo']['description'],
            '关注数量': homepage['data']['userInfo']['follow_count'],
            '粉丝数量': homepage['data']['userInfo']['followers_count'],
        }
        # 将该字典存入文件，并覆盖原文件（该操作是为了储存下面所爬数据的微博用户信息，实际操作时爬虫中止后重启，忘记更换文件可能造成已爬取数据被覆盖，一般在第一次运行后将其注释掉）
        with open('sinanews7.text', 'w', encoding='utf-8') as fp:
            fp.write(json.dumps(user_Info_dic, indent=4, separators=(',', ':'), ensure_ascii=False))
            fp.write('\n')
        # 取containerid
        tab_list = homepage['data']['tabsInfo']['tabs']
        containerid = ''
        # containerid存储于一个'tabKey'：'weibo'的tab字典中，通过以下方式将其找出并赋值
        for tab in tab_list:
            if tab['tabKey'] == 'weibo':
                containerid = tab['containerid']
        # 将containerid参数加入parm，此时通过url+parm就可以爬取到包含该user发布微博内容的数据包，不使用page或者since_id参数时获得的是默认时间最近的数据包
        param['containerid'] = containerid
        # 以追加格式打开要储存爬取信息的文件，
        fp = open('sinanews7.text', 'a', encoding='utf-8')
        # 变量number用来记录当前爬取微博是这次程度运行的第几条
        number = 0
        # 变量pagen就是param中的page参数，最初是采用的since_id，但是这种方式只能从头爬起，十分繁琐和耗时，实际爬取中采用page
        pagen = 1739
        # 变量count是用来记录except已经捕获的异常个数，为了防止出现连续报错并及时更换cookie，当count为7是更新一次cookie，并重置count
        count = 0
        # 变量page是储存的一页（9条）微博的内容，至于为何定义在这里，应该是我最开始写的版本的需要，也就一直没更改过
        page = homepage
        # 在headers添加cookie（最初爬取时没有加cookie，发现爬下来的都是错误的数据）
        cookie = input('First cookie:\n')  # 最开始设计的是直接把cookie的内容复制粘贴到这里，发现很麻烦，用input从控制台输入获得更优的交互体验
        sina_headers['cookie'] = cookie
        # 不断发起请求，获取用户微博内容，while循环获取的一般是一个包含9条微博的数据包
        while True:
            pagen += 1  # 每个循环加一，指向下一个数据包
            param['page'] = str(pagen)  # 设置param中的page
            response = requests.get(url=url, params=param, headers=sina_headers)  # 发起请求
            page = response.json()   # 获取其中的json数据
            # page中含有9条微博的内容，通过for循环将其一个一个存下来（具体操作见文档描述）
            for card in page['data']['cards']:
                # 有时获取的数据有误，异常处理机制可以将此次循环跳过并执行相应的操作
                try:
                    if card['card_type'] == 9:  # 'card_type'：9表明该card是一条微博的内容
                        print(card['mblog']['created_at'])  # 在控制台输出正在爬取微博的发布时间，方便控制和了解爬虫运行状态
                        # 将需要的信息储存下来
                        content_dic = {
                            "微博地址": card['scheme'],
                            "发布时间": card['mblog']['created_at'],
                            "转发数": card['mblog']['reposts_count'],
                            "评论数": card['mblog']['comments_count'],
                            "点赞数": card['mblog']['attitudes_count'],
                            "微博内容": get_content(card['mblog']['id']),  # 由id获得该微博所在地址并返回微博标题和正文内容
                            "评论": get_comment(card['mblog']['mid'], card['scheme'], sina_headers['cookie'])  # sheme和mid是评论headers和param所需参数，由于评论是动态加载，所以要将cookie也传递过去
                        }
                        # 一条微博写入一次，json.dumps主要是将其格式化，indent参数控制其换行和每行的缩进，ensure_ascii=False是为了存储中文，加入separators参数是因为试爬取是有许多不必要的空格影响观感，这个参数可以将其删去
                        fp.write(json.dumps(content_dic, indent=4, separators=(',', ':'), ensure_ascii=False))
                        fp.write('\n')  # 另起一行，为下一条微博做准备
                        fp.flush()  # 将缓冲区内的内容写入指定文件（及时将每条微博的内容存进文件，方便我观察爬虫运行状况）
                        print('爬'+str(number))  # 输出number的值，看见number的值在一直增长可以判断运行正常（因为一天有很多条，只输出正在爬取微博的发布时间会造成长时间数值无变化，不好判断爬虫运行状况）
                        number += 1  # number循环加一
                # 以下注释掉的内容是采取since_id时的部分代码，实际爬取时未采用（其原理见文档）
                # time.sleep((int)(7+random.random()*5))
                # since_id=page['data']['cardlistInfo']['since_id']
                # param['since_id']=since_id
                except Exception as e:
                    count += 1  # 出现一次异常加一
                    if count == 7:  # 累计7次后执行下列操作
                        print(pagen)  # 输出当前爬虫进度（page到第几页了）
                        sina_headers['cookie'] = input('cookie:\n')  # 从控制台输入最新的cookie，实现更新cookie并继续运行
                        count = 0  # 重置count
                        continue
                    else:  # 不到7次时直接跳过
                        continue

