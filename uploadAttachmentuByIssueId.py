# -*- coding=utf-8 -*-

from jira import JIRA
import sys , os
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

class JIRA_TOOL:
    def __init__(self,conf):
        print conf
        self.server = conf[0]
        self.basic_auth = (conf[1], conf[2])
        self.jiraClient = None

    def login(self):
        self.jiraClient = JIRA(self.server , basic_auth=self.basic_auth)
        if self.jiraClient != None:
            print u'登录成功！'
            return True
        else:
            print u'登录出错！'
            return False

    def uploadAttachment(self,issueId,file):
        self.jiraClient.add_attachment(issue=issueId, attachment=file)
        # issue = self.jiraClient.issue(issueId)
        # attachment = issue.fields.attachment
        print u'成功上传附件:' ,file
        pass

if __name__ == '__main__' :
    jira_info = Config_read()
    conf = jira_info.get_value()

    jiraTool=JIRA_TOOL(conf)
    issueId = 'GXQ-2038'
    file = 'F:/Apache-test/5864ab29780c1.png'

    if jiraTool.login():
        issue = jiraTool.findIssueById(issueId)
        if issue :
            jiraTool.uploadAttachment(issueId,issue,file)
        else :
            exit()
    else :
        exit()



