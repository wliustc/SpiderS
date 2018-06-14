# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import time
import socket
import json
import web


def _get_ip():
    myname = socket.getfqdn(socket.gethostname())
    return socket.gethostbyname(myname)

def _get_tsp():
    return str(time.time())[0:10]


def update_result_path(tuid, path):
    db = web.database(dbn='mysql', db='hillinsight', user='work', pw='phkAmwrF', port=3306, host='10.15.1.24')
    try:
        db.update('t_platform_jobs', where="uid = '%s'" % tuid, result_path='%s' % path)
    except:
        pass


class WriteFilePipeline(object):
    def __init__(self,save_path,max_size,project,task_uid,task_date,hdfs_path,hdfs_ip,hdfs_port):
        self.dir = save_path
        self.task_uid = task_uid
        self.hdfs_module = hdfs_path.strip()
        self.hdfs_port = hdfs_port.strip()
        self.hdfs_ip = hdfs_ip.strip()
        save_path = save_path+"/{}/{}/{}".format(project,task_date.strip(),task_uid)
        if save_path and not os.path.exists(save_path):
            os.makedirs(save_path)
        self.count = 1
        self.maxSize = 500
        if max_size:
            self.maxSize = int(max_size)
        self.save_path = save_path
        self.ip = _get_ip()
        self.file_name = save_path+'/{}_{}.json'
        self.file_name_now = self.file_name.format(self.ip,_get_tsp())
        if self.save_path:
            os.system('cd {} && rm -rf *'.format(self.save_path))
        self.file = open(self.file_name_now, 'wb')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            save_path = crawler.settings.get('SAVE_PATH',''),
            max_size = crawler.settings.get('MAX_FILESIZE',''),
            project = crawler.settings.get('BOT_NAME',''),
            task_uid = crawler.settings.get('TASK_UID',''),
            hdfs_path = crawler.settings.get('HDFS_MODULE',''),
            hdfs_port = crawler.settings.get('HDFS_PORT','9668'),
            hdfs_ip = crawler.settings.get('HDFS_IP',''),
            task_date = crawler.settings.get('TASK_DATE',time.strftime("%Y-%m-%d",time.localtime(time.time()))),
        )
    def open_spider(self, spider):
        update_result_path(self.task_uid, self.save_path)

    def close_spider(self, spider):
        self.file.close()
        p=os.popen('rsync -aczuRP --port {} {} {}::{}; 2>&1'.format(self.hdfs_port,self.save_path,self.hdfs_ip,self.hdfs_module),'r')
        if not p.close() and self.save_path != "/":
            os.system("rm -rf {};".format(self.save_path))
        pass

    def process_item(self, item, spider):
        if self.count % 500 == 0:
            self.file.flush()
            if os.path.getsize(self.file_name_now) > 1048576*self.maxSize:
                self.file.close()
                p=os.popen('rsync -aczuRP --port {} {} {}::{}'.format(self.hdfs_port,self.file_name_now,self.hdfs_ip,self.hdfs_module),'r')
                if not p.close() and self.file_name_now != "/":
                    os.system("rm -f {}".format(self.file_name_now))
                self.file_name_now = self.file_name.format(self.ip,_get_tsp())
                self.file = open(self.file_name_now, 'wb')
        line = dict(item)
        # if line and 'content' in line and line['content']:
        if line:
            line = json.dumps(line) + "\n"
            self.file.write(line)
            self.count += 1
        return item


