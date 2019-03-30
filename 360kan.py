import requests
import json

def get_video_info(url):
    '''
    请求url获得相应
    :param url: 传入的url链接
    :return: 返回视频信息，
    '''
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        datas=json.loads(resp.text)['data']['res']
        return datas
    except:
        print('首页输出失败！')

def parse_video_info(datas):
    '''
    获取单条视频的信息
    :param datas:
    :return:解析出标题、作者、视频链接、vid
    '''
    data_info = {}
    for data in datas:
        data_info['title'] = data['t']
        data_info['author'] = data['f']
        data_info['url'] = data['u']
        data_info['videoid'] = data['vid']
        yield data_info

def get_video_url(data,vid):
    '''
    通过获取的vid构造视频地址，从而解析出下载地址
    :param vid: 
    :return: 
    '''
    resp = requests.get('http://pc.k.360kan.com/pc/play?id={vid}'.format(vid=vid))
    download_video_url = json.loads(resp.text)['data']['url']
    data['download_video_url']=download_video_url
    return data

def download_video(data):
    '''
    通过url下载视频，存在本地
    :param data:
    :return:
    '''
    with open('{title}'.format(title=data['title'])+'.mp4','wb') as f:
        f.write(requests.get(data['download_video_url']).content)


if __name__ == '__main__':
    page = 1
    while True:
        url = 'http://pc.k.360kan.com/pc/list?n={p}&p=1&f=json'.format(p=page)
        datas = get_video_info(url)
        data_info = parse_video_info(datas)
        for data in data_info:
            data = get_video_url(data,data['videoid'])
            download_video(data)
        page+=1





