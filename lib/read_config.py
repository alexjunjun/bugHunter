# coding=UTF-8
import ConfigParser
import os

def readConfig(file,field,key):
    '''

    :param file:
    :param field:
    :param key:
    :return:
    '''
    config = ConfigParser.ConfigParser()
    conf_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","config",file))
    config.readfp(open(conf_path, "r"))
    return config.get(field, key)

if __name__ =='__main__':
    server= readConfig('config.ini','server','server')