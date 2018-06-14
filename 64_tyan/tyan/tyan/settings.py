# -*- coding: utf-8 -*-
BOT_NAME='tyan'
SPIDER_MODULES=['tyan.spiders']
NEWSPIDER_MODULE='tyan.spiders'
DOWNLOAD_HANDLERS={'s3': None}
USER_AGENT="Dalvik/1.6.0 (Linux; U; Android 4.4.2; H60-L01 Build/HDH60-L01)"
USER_AGENTS=[
  "Dalvik/1.6.0 (Linux; U; Android 4.4.2; H60-L01 Build/HDH60-L01)",
]
CORE_METRICS_INTERVAL=5
HDFS_MODULE="hdfs"
HDFS_IP="10.15.1.11"
MAIL_FROM="spider_man_warn@126.com"
ITEM_PIPELINES= {
	'tyan.pipelines_global.WriteFilePipeline': 300,
}
LOG_LEVEL='WARNING'
DEFAULT_REQUEST_HEADERS={"version": "Android 3.1.1",
"Authorization":"kjCy5ueHGS0gEJug3psZIekyMriF0afmim/D2sdSbtTQCcVqKUuDB/DbKG1d4dw9","X-Auth-Token":"","user-agent": USER_AGENT
                        ,"Content-Type":"application/json","Host":"api.tianyancha.com","Connection":"Keep-Alive","Accept-Encoding":"gzip"}
MAIL_USER="spider_man_warn@126.com"
MAX_FILESIZE='500'
MAIL_PASS="dev123"
EXTENSIONS= {
	'tyan.stats_collector_global.PrintCoreMetrics': 500,
	'tyan.stats_mail_global.StatsMailer': 505,
}
SAVE_PATH='/home/work/backup/spiders_platform/data'
MAIL_HOST="smtp.126.com"
MAIL_PORT="25"
    
    