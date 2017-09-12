# coding=UTF-8
from jira import JIRA, JIRAError

from lib.log_config import get_logger

_mylogger = get_logger('bugHunter')

def uploadAttachment(login,issueId,file):
    try:
        login.add_attachment(issue=issueId, attachment=file)
    except Exception  as e:
        if isinstance(e,JIRAError):
            _mylogger.error(u'插入附件失败 %s' %e.text)
            result = e.text
        else :
            _mylogger.error(u'插入附件失败 %s' %e)
            result = e
        return result
    else:
        _mylogger.info(u'插入附件成功')
        return True


def findIssue(login,issueId):
    try:
        login.issue(issueId)
    except Exception  as e:
        if isinstance(e,JIRAError):
            _mylogger.error(u'查询bug失败 %s' %e.text)
            result = e.text
        else :
            _mylogger.error(u'查询bug失败 %s' %e)
            result = e
        return result
    else:
        _mylogger.info(u'查询bug成功')
        return True