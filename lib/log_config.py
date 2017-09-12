# coding=UTF-8
import logging
import os
from logging.handlers import RotatingFileHandler

from lib.read_config import readConfig

'''
    CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
'''

def customer_config():
    log_file = os.path.join(readConfig('config.ini','log','log_file'),'log.log')
    print log_file
    logging.root.setLevel(logging.DEBUG)
    # 控制台、日志文件输出日志格式设置
    format1=logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(lineno)s %(message)s')
    format2=logging.Formatter('[%(name)s] [%(levelname)s] %(lineno)s %(message)s')
    # 创建控制台输出日志的handler
    ch=logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(format2)
    # 创建文件输出日志的handler
    fh=RotatingFileHandler(log_file,maxBytes=10*1024*1024,backupCount=10) # 日志文件最大10M，最多备份5个文件
    fh.setLevel(logging.INFO)
    fh.setFormatter(format1)
    # 为logging添加handler
    logging.root.addHandler(ch)
    logging.root.addHandler(fh)

customer_config()

def get_logger(name='root'):
    return logging.getLogger(name)

if __name__=='__main__':
    mylogger=get_logger('666')
    mylogger.debug('Test start !')
    mylogger.info('Test start !')
    mylogger.error('Test start !')