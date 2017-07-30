# -*- coding: utf-8 -*-

#   base_url : http://s.weibo.com/weibo/
# + keyword : twice url encode
# + "&region=custom:": districts
# + "&scope=": type of weibo
# + "&suball=": kinds of the content contains
# + "&timescope=custom:": time scope
# + "&page="

# county-level city
all_region = {u'不限': ''}
anhui = {u'不限': '1000'}
beijing = {u'不限': '1000'}
chongqing = {u'不限': '1000'}
fujian = {u'不限': '1000'}
gansu = {u'不限': '1000'}
guangdong = {u'不限': '1000'}
guangxi = {u'不限': '1000'}
guizhou = {u'不限': '1000'}
hainan = {u'不限': '1000'}
hebei = {u'不限': '1000'}
heilongjiang = {u'不限': '1000'}
henan = {u'不限': '1000'}
hubei = {u'不限': '1000'}
hunan = {u'不限': '1000'}
neimenggu = {u'不限': '1000'}
jiangsu = {
    u'不限': '1000',
    u'南京': '1',
    u'无锡': '2',
    u'徐州': '3',
    u'常州': '4',
    u'苏州': '5',
    u'南通': '6',
    u'连云港': '7',
    u'淮安': '8',
    u'盐城': '9',
    u'扬州': '10',
    u'镇江': '11',
    u'泰州': '12',
    u'宿迁': '13'
}
jiangxi = {u'不限': '1000'}
jilin = {u'不限': '1000'}
liaoning = {u'不限': '1000'}
ningxia = {u'不限': '1000'}
qinghai = {u'不限': '1000'}
shanxi = {u'不限': '1000'}
shandong = {u'不限': '1000'}
shanghai = {u'不限': '1000'}
sichuan = {u'不限': '1000'}
tianjing = {u'不限': '1000'}
xizang = {u'不限': '1000'}
xinjiang = {u'不限': '1000'}
yunnan = {u'不限': '1000'}
zhejiang = {u'不限': '1000'}
shanxi = {u'不限': '1000'}
taiwan = {u'不限': '1000'}
xianggan = {u'不限': '1000'}
aomen = {u'不限': '1000'}
haiwai = {u'不限': '1000'}
qita = {u'不限': '1000'}

# provinces or cities

districts = {
    u'省/直辖市': ['', all_region],
    u'安徽': ['34', anhui],
    u'北京': ['11', beijing],
    u'重庆': ['50', chongqing],
    u'福建': ['35', fujian],
    u'甘肃': ['62', gansu],
    u'广东': ['44', guangdong],
    u'广西': ['45', guangxi],
    u'贵州': ['52', guizhou],
    u'海南': ['46', hainan],
    u'河北': ['13', hebei],
    u'黑龙江': ['23', heilongjiang],
    u'河南': ['41', henan],
    u'湖北': ['42', hubei],
    u'湖南': ['43', hunan],
    u'内蒙古': ['15', neimenggu],
    u'江苏': ['32', jiangsu],
    u'江西': ['36', jiangxi],
    u'吉林': ['22', jilin],
    u'辽宁': ['21', liaoning],
    u'宁夏': ['64', ningxia],
    u'青海': ['63', qinghai],
    u'山西': ['14', shanxi],
    u'山东': ['37', shandong],
    u'上海': ['31', shanghai],
    u'四川': ['51', sichuan],
    u'天津': ['12', tianjing],
    u'西藏': ['54', xizang],
    u'新疆': ['65', xinjiang],
    u'云南': ['53', yunnan],
    u'浙江': ['33', zhejiang],
    u'陕西': ['61', shanxi],
    u'台湾': ['71', taiwan],
    u'香港': ['81', xianggan],
    u'澳门': ['82', aomen],
    u'海外': ['400', haiwai],
    u'其他': ['100', qita]
}

weibo_type = {
    u'全部': '&typeall=1',
    u'热门': '&xsort=hot',
    u'原创': '&scope=ori',
    u'关注人': '&atten=1',
    u'认证用户': '&vip=1',
    u'媒体': '&category=1'
}

weibo_containing = {
    u'全部': '&suball=1',
    u'含图片': '&haspic=1',
    u'含视频': '&hasvideo=1',
    u'含音乐': '&hasmusic=1',
    u'含短链接': '&haslink=1'
}
