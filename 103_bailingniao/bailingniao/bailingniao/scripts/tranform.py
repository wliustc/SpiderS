import sys

import web
import json
import time

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
#dt = int(time.time())

def web_db_insert(data):

    db.insert('t_spider_bailingniao_field',**data)

for line in sys.stdin:
    data = json.loads(line)
    web_db_insert(data)

#for line in sys.stdin:
    # line_json = json.loads(line)
    # web_db_insert(line_json)
    # print line
#    line_json = json.loads(line)
    # print line_json
#    response_content = line_json.get('response_content')
 #   response_content = json.loads(response_content)
  #  data = response_content.get('data')
   # if data:
    #    items = data.get('items')
     #   if items:
      #      for item in items:
       #         result = {}
                # print item
        #        category = item.get('categorys')
         #       category_result = []
          #      for cate in category:
           #         category_result.append(json.dumps(cate))

            #    result['category'] = ';'.join(category_result)
                # print item.get('categorys')
                # print type(item.get('categorys'))
             #   result['addr'] = item.get('address')
              #  result['name'] = item.get('name')
               # result['lat'] = item.get('lat')
                #result['lng'] = item.get('lat')
                #result['tel'] = item.get('phone')
                #result['cityname'] = item.get('cityObj').get('name')
                #result['field_id'] = item.get('id')
                #result['task_time'] = dt
                # print result
                #web_db_insert(result)
        # time.sleep(100)
    
    
    