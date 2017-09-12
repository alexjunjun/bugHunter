# coding=UTF-8
from jira import JIRA, JIRAError

from lib.log_config import get_logger
from lib.read_config import readConfig
_mylogger = get_logger('bugHunter')

def loginJira():
    server= readConfig('config.ini','server','server')
    user_name= readConfig('config.ini','user','user_name')
    password= readConfig('config.ini','user','password')
    conf=(user_name,password)
    try:
        login=JIRA(server=server,basic_auth=conf)
    except Exception  as e:
        if isinstance(e,JIRAError):
            _mylogger.error(u'登录失败 %s' %e.text)
            result = e.text
        else :
            _mylogger.error(u'登录失败 %s' %e)
            result = e

        return result
    else:
        _mylogger.info(u'登录成功')
        return login