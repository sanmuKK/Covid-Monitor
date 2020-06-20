from flask import jsonify,Blueprint
import json
from config import rd


ncov=Blueprint('ncov',__name__,url_prefix='/api')


@ncov.route('/get_province_data/confirmedCount')
def get_confirmedCount_data():
    province_data = json.loads(rd.get('ncovcity_data'))
    province_dist=[]
    for province in province_data['newslist']:
        dict={'name':province['provinceShortName'],'value':province['confirmedCount']}
        province_dist.append(dict)
    return jsonify(province_dist)


@ncov.route('/get_province_data/currentConfirmedCount')
def get_currentConfirmedCount_data():
    province_data = json.loads(rd.get('ncovcity_data'))
    province_dist=[]
    for province in province_data['newslist']:
        dict={'name':province['provinceShortName'],'value':province['currentConfirmedCount']}
        province_dist.append(dict)
    return jsonify(province_dist)


@ncov.route('/get_city_data/<provinceName>')
def get_all_city_data(provinceName):
    province_data = json.loads(rd.get('ncovcity_data'))
    dict={}
    for province in province_data['newslist']:
       if province['provinceName'] == provinceName:
           dict = {'confirmedCount': province['confirmedCount'],'curedCount':province['curedCount'],
                   'currentConfirmedCount':province['currentConfirmedCount'],'deadCount':province['deadCount'],
                   'suspectedCount':province['suspectedCount']}
           break
    return jsonify(dict)


@ncov.route('/get_city_data/<provinceName>/<cityname>')
def get_ont_city_data(provinceName,cityname):
    province_data = json.loads(rd.get('ncovcity_data'))
    dict = {}
    for province in province_data['newslist']:
       if province['provinceName'] == provinceName:
           for city in province['cities']:
               name = city['cityName'][:2]
               if name == cityname:
                    dict = {'cityName':city['cityName'],'confirmedCount': city['confirmedCount'],
                            'curedCount': city['curedCount'],'currentConfirmedCount': city['currentConfirmedCount'],
                            'deadCount': city['deadCount'], 'suspectedCount': city['suspectedCount']}
                    break
           break
    return jsonify(dict)


@ncov.route('/get_ncov_totalcount')
def ncov_totalcount():
    ncov_data = rd.get('ncov_data')
    result_ncov = json.loads(ncov_data)
    data = result_ncov['data']['chinaTotal']
    data['total']['noSymptom'] = data['extData']['noSymptom']
    data['today']['noSymptom'] = data['extData'].get('incrNoSymptom',None)
    data['total']['currentconfirm'] = data['total']['confirm']-data['total']['heal']-data['total']['dead']
    dist = {'total':data['total'],'today':data['today'],'lastUpdateTime':result_ncov['data']['lastUpdateTime']}
    return jsonify(dist)


@ncov.route('/get_ncov_trend/confirmedCount')
def ncov_trend_confirmedCount():
    ncov_data = rd.get('ncov_data')
    result_ncov = json.loads(ncov_data)
    datalist = result_ncov['data']['chinaDayList']
    step = int(len(datalist)/9)
    dict = {}
    date_list=[]
    confirmedCount_list = []
    suspect_list = []
    for i in range(0,len(datalist)-1,step):
        date_list.append(datalist[i]['date'][5:10].replace('-','.'))
        confirmedCount_list.append(datalist[i]['total']['confirm'])
        suspect_list.append(datalist[i]['total']['suspect'])
    date_list.append(datalist[-1]['date'][5:10].replace('-','.'))
    confirmedCount_list.append(datalist[-1]['total']['confirm'])
    suspect_list.append(datalist[-1]['total']['suspect'])
    dict['date'] = date_list
    dict['totalComfirm'] = confirmedCount_list
    dict['suspect'] = suspect_list
    return jsonify(dict)


@ncov.route('/get_ncov_trend/currentConfirmedCount')
def ncov_trend_currentConfirmedCount():
    ncov_data = rd.get('ncov_data')
    result_ncov = json.loads(ncov_data)
    datalist = result_ncov['data']['chinaDayList']
    step = int(len(datalist)/9)
    dict = {}
    date_list=[]
    currentConfirmedCount_list = []
    suspect_list = []
    for i in range(0,len(datalist)-1,step):
        date_list.append(datalist[i]['date'][5:10].replace('-','.'))
        currentConfirmedCount_list.append(datalist[i]['today']['confirm'])
        suspect_list.append(datalist[i]['today']['suspect'])
    date_list.append(datalist[-1]['date'][5:10].replace('-','.'))
    currentConfirmedCount_list.append(datalist[-1]['today']['confirm'])
    suspect_list.append(datalist[-1]['today']['suspect'])
    dict['date'] = date_list
    dict['increaseComfirm'] = currentConfirmedCount_list
    dict['suspect'] = suspect_list
    return jsonify(dict)


@ncov.route('/get_ncov_trend/dead')
def ncov_trend_dead():
    ncov_data = rd.get('ncov_data')
    result_ncov = json.loads(ncov_data)
    datalist = result_ncov['data']['chinaDayList']
    step = int(len(datalist)/9)
    dict = {}
    date_list=[]
    dead_list = []
    heal_list = []
    for i in range(0,len(datalist)-1,step):
        date_list.append(datalist[i]['date'][5:10].replace('-','.'))
        dead_list.append(datalist[i]['total']['dead'])
        heal_list.append(datalist[i]['total']['heal'])
    date_list.append(datalist[-1]['date'][5:10].replace('-','.'))
    dead_list.append(datalist[-1]['total']['dead'])
    heal_list.append(datalist[-1]['total']['heal'])
    dict['date'] = date_list
    dict['dead'] = dead_list
    dict['heal'] = heal_list
    return jsonify(dict)


@ncov.route('/get_ncov_world/comfirm')
def ncov_world_comfirm():
    ncov_data = rd.get('ncov_data')
    result_ncov = json.loads(ncov_data)
    datalist = result_ncov['data']['areaTree']
    list = []
    for data in datalist:
        dict = {}
        dict['name'] = data['name']
        dict['value'] = data['total']['confirm']
        list.append(dict)
    return jsonify(list)


@ncov.route('/get_ncov_world/currentconfirm')
def ncov_world_currentconfirm():
    ncov_data = rd.get('ncov_data')
    result_ncov = json.loads(ncov_data)
    datalist = result_ncov['data']['areaTree']
    list = []
    for data in datalist:
        dict = {}
        dict['name'] = data['name']
        dict['value'] = data['total']['confirm']-data['total']['heal']-data['total']['dead']
        list.append(dict)
    return jsonify(list)


@ncov.route('/get_ncov_global_totalcount')
def ncov_global_totalcount():
    ncov_data = rd.get('ncov_global_data')
    result_ncov = json.loads(ncov_data)
    data = result_ncov['data']
    dict = {}
    dict['lastUpdateTime'] = data['mtime']
    try:
        a=int(data['othertotal']['ecertain_inc'])+int(data['add_daily']['addecon_new'])
    except:
        a='未公布'
    today_dict = {
        "confirm": int(data['othertotal']['certain_inc'])+int(data['add_daily']['addcon']),
        "dead": int(data['othertotal']['die_inc'])+int(data['add_daily']['adddeath']),
        "heal": int(data['othertotal']['recure_inc'])+int(data['add_daily']['addcure']),
        "storeConfirm": a,
    }
    total_dict = {
        "confirm": int(data['othertotal']['certain'])+int(data['gntotal']),
        "currentconfirm": int(data['othertotal']['ecertain'])+int(data['econNum']),
        "dead": int(data['othertotal']['die'])+int(data['deathtotal']),
        "heal": int(data['othertotal']['recure'])+int(data['curetotal']),
    }
    dict['today'] = today_dict
    dict['total'] = total_dict
    return jsonify(dict)


@ncov.route('/get_ncov_trend/foreign/dead')
def ncov_global_dead_trend():
    ncov_data = rd.get('ncov_global_data')
    result_ncov = json.loads(ncov_data)
    data = result_ncov['data']['otherhistorylist']
    step = -1*int(len(data) / 9)
    date_list = []
    dead_list = []
    heal_list =[]
    for i in range(len(data)-1,0,step):
        date_list.append(data[i]['date'])
        dead_list.append(int(data[i]['die']))
        heal_list.append(int(data[i]['recure']))
    date_list.append(result_ncov['data']['mtime'][5:10].replace('-','.'))
    dead_list.append(int(result_ncov['data']['othertotal']['die']))
    heal_list.append(int(result_ncov['data']['othertotal']['recure']))
    return jsonify({"date":date_list,"dead":dead_list,"heal":heal_list})


@ncov.route('/get_ncov_trend/foreign/confirmedCount')
def ncov_global_confirmedCount_trend():
    ncov_data = rd.get('ncov_global_data')
    result_ncov = json.loads(ncov_data)
    data = result_ncov['data']['otherhistorylist']
    step = -1*int(len(data) / 9)
    date_list = []
    confirmedCount_list = []
    currconfirmedCount_list =[]
    for i in range(len(data)-1,0,step):
        date_list.append(data[i]['date'])
        confirmedCount_list.append(int(data[i]['certain']))
        currconfirmedCount_list.append(int(data[i]['certain'])-int(data[i]['die'])-int(data[i]['recure']))
    date_list.append(result_ncov['data']['mtime'][5:10].replace('-','.'))
    confirmedCount_list.append(int(result_ncov['data']['othertotal']['certain']))
    currconfirmedCount_list.append(int(result_ncov['data']['othertotal']['ecertain']))
    return jsonify({"date":date_list,"totalComfirm":confirmedCount_list,"currconfirmed":currconfirmedCount_list})


@ncov.route('/get_ncov_trend/foreign/china/confirmedCount')
def ncov_global_china_confirmedCount_trend():
    ncov_data = rd.get('ncov_global_data')
    result_ncov = json.loads(ncov_data)
    data1 = result_ncov['data']['otherhistorylist']
    data2 = result_ncov['data']['historylist']
    step = -1*int(len(data1) / 9)
    date_list = []
    foreign_list = []
    china_list =[]
    for i in range(len(data1)-1,0,step):
        date_list.append(data1[i]['date'])
        foreign_list.append(int(data1[i]['certain_inc']))
        china_list.append(int(data2[i]['cn_conadd']))
    date_list.append(result_ncov['data']['mtime'][5:10].replace('-','.'))
    foreign_list.append(int(result_ncov['data']['othertotal']['certain_inc']))
    china_list.append(result_ncov['data']['add_daily']['addcon'])
    return jsonify({"date":date_list,"foreignincrease":foreign_list,"chinaincrease":china_list})