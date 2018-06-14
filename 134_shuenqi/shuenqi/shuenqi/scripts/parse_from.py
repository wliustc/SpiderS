# coding:utf8
import sys
import json
import time
import web
reload(sys)
sys.setdefaultencoding('utf8')
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


def time_conversion(date):
    date =  date/1000
    time_local = time.localtime(date)
    return time.strftime("%Y.%m",time_local)

type_dict = {'A_PLUS':'A+轮','ANGEL':'天使轮','B_PLUS':'B+轮','PRE_A':'Pre-A轮','A':'A轮','B':'B轮','C':'C轮','D':'D轮','E':'E轮及以后',
             'C_PLUS':'C+轮','D_PLUS':'D+轮'}
money_dict = {'CNY':'人民币','USD':'美元'}
def from_parse(dd):
    item = {}
    i = json.loads(dd)
    company_name = i.get('company_name')
    data = json.loads(i.get('data'))
    if len(data.get('data')):
        data = data.get('data')
        for i in data:
            financing_amountunit = i.get('financeAmount')
            financeAmountUnit = money_dict.get(i.get('financeAmountUnit'))
            if financeAmountUnit == None:
                financeAmountUnit = i.get('financeAmountUnit')
                if financeAmountUnit == None:
                    financeAmountUnit = ''
            financing_lun = type_dict.get(i.get('phase'))
            if financing_lun == None:
                financing_lun = i.get('phase')
            financing_V = i.get('participantVos')
            financing_year = time_conversion(i.get('financeDate'))
            financing_participants = []
            if financing_V:
                for f_v in financing_V:
                    financing_participants.append(f_v.get('entityName'))
            financing_participants = ','.join(financing_participants)
            dt =time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
            item['financing_year'] = financing_year
            item['financing_amountunit'] = financing_amountunit + financeAmountUnit
            item['financing_lun'] = financing_lun
            item['financing_participants'] = financing_participants
            item['company_name'] = company_name
            item['dt'] = dt
            try:
                db.insert('t_spider_hillhousecap_tyc_financing', **item)
            except Exception as e:
                print e



for line in sys.stdin:
    from_parse(line)




# def from_parse():
#
#     with open(r'E:\gongs_\kr36\login.jl','r') as f:
#         for i in f.readlines():
#             i = json.loads(i)
#             company_name = i.get('company_name')
#             data = json.loads(i.get('data'))
#             if len(data.get('data')):
#                 data = data.get('data')
#                 for i in data:
#                     financing_amountunit = i.get('financeAmount')
#                     financing_lun = type_dict.get(i.get('phase'))
#                     if financing_lun == None:
#                         financing_lun = i.get('phase')
#                     financing_V = i.get('participantVos')
#                     financing_year = time_conversion(i.get('financeDate'))
#                     financing_participants = []
#                     if financing_V:
#                         for f_v in financing_V:
#                             financing_participants.append(f_v.get('entityName'))
#                     financing_participants = ','.join(financing_participants)
#                     dt =time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
#                     print financing_year,financing_amountunit,financing_lun,financing_participants,company_name,dt
#
# from_parse()
    