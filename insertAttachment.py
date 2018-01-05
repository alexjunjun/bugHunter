# coding=UTF8
'''
入参：
1.issueID,格式：“GXQ-xxxx”
2.file绝对路径，格式：'F:/Apache-test/5864ab29780c1.png'
'''
from jira import JIRAError, JIRA
from lib.issueOprate import uploadAttachment, findIssue
from lib.log_config import get_logger
from lib.loginJira import loginJira

_mylogger = get_logger('bugHunter')


def checkIssueID(issueID):
    project = '-'
    if project in issueID:
        _mylogger.info(u'%s 符合条件，开始上传附件' % issueID)
        return True;
    else:
        _mylogger.info(u'%s 不符合条件，不做处理' % issueID)
        return False


def insertToJIRA(issueID, file):
    login = loginJira()

    # 判断是否符合规则的issueID
    if checkIssueID(issueID):
        try:
            findIssue(login,issueID)
        except Exception  as e:
            if isinstance(e, JIRAError):
                _mylogger.error(e.text)
                result = e.text
            else:
                _mylogger.error(e)
                result = e
        else:
            try:
                uploadAttachment(login,issueID, file)
            except Exception  as e:
                if isinstance(e, JIRAError):
                    _mylogger.error(u'插入失败 %s' %e.text)
                    result = e.text
                else:
                    _mylogger.error(u'插入失败 %s' %e)
                    result = e
            else:
                result = True
        return result
    else:
        _mylogger.warning(u'bugID不符合规则')
        return u'bugID不符合规则'

