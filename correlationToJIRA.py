#coding=UTF8
'''
入参：
1.issueID,格式：“GXQ-xxxx”
2.file绝对路径，格式：'F:/Apache-test/5864ab29780c1.png'

'''
import sys , os

from jira import JIRAError

from uploadAttachmentuByIssueId import JIRA_TOOL
import ConfigParser

class Config_read(object):
    def get_value(self):
        #file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.join(r'\config','config.ini')
        file_path = os.path.abspath(os.path.join('config','config.ini'))

        config = ConfigParser.ConfigParser()
        config.read(file_path)
        #print file_path

        server = config.get("server", "server") #分别代表所在区域名 和变量名
        user_name = config.get("user", "user_name")
        passwd = config.get("user", "password")
        return (server, user_name,passwd)


def checkIssueID(issueID):
    project = 'GXQ-'
    if project in issueID :
        print u'符合条件，开始上传附件'
        return True
    else :
        print u'不是bug上报，无需处理!!!'
        return False



def insertToJIRA(issueID ,file):
    jira_info = Config_read()
    conf = jira_info.get_value()
    jiraTool=JIRA_TOOL(conf)
    result =True
    try :
        issueId = issueID
        file = file
    except :
        result = u'参数异常！！！'
        return result
    else :
        #判断是否符合规则的issueID
        if checkIssueID(issueId) :
            if jiraTool.login():
                issue=None
                try:
                    issue=jiraTool.jiraClient.issue(issueId)
                except Exception  as e:
                    if isinstance(e,JIRAError):
                        print e.text
                        result = e.text
                    else :
                        print e
                        result = e
                else :
                    jiraTool.uploadAttachment(issueId,file)
                    print u'插入附件成功'
                    result = True
                return result

            else :
                result = u'登录失败'
                return result
        else :
            result = u'bugID不符合规则'
            return result


if __name__ == '__main__':
    try :
        issueId = sys.argv[0]
        file = sys.argv[1]
    except :
        print u'参数异常！！！'
    else :
        #判断是否符合规则的issueID
        if checkIssueID(issueId) :
            if jiraTool.login():
                issue = jiraTool.findIssueById(issueId)
                if issue :
                    jiraTool.uploadAttachment(issueId,issue,file)
                else :
                    exit()
            else :
                exit()
        else :
            exit()