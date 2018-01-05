# coding:utf-8

import os

from flask import Flask, render_template, jsonify, request

from  insertAttachment import insertToJIRA
from lib.log_config import get_logger
from lib.saveFile import save_file

app = Flask(__name__)
UPLOAD_FOLDER = 'uploadFiles'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
BASEPATH = os.path.abspath(os.path.dirname(__file__))

_mylogger = get_logger('bugHunter')

if  not os.path.exists('log'):
    _mylogger.info('No such dir,create one!')
    os.mkdir('log')

file_dir = os.path.join(BASEPATH, app.config['UPLOAD_FOLDER'])
# 如果不存在，创建目录uploadFiles，用于存放上传的文件
if not os.path.exists(file_dir):
    _mylogger.debug('create uploadFiles dir!')
    os.makedirs(file_dir)

# 用于测试提交表单的页面
@app.route('/test/upload')
def upload_tst():
    return render_template('upload1.html')


#用于上传文件
@app.route('/bughunter/upload' , methods=['POST'] , strict_slashes= False)
def api_upload():
    '''
    用于接收客户端提交的文件和bugID
    请求方式：POST
    参数：attachment、bugID
    :return:
        1000 上传文件成功,插入jira附件成功
        1001 参数异常，上传失败
        1002 参数为空，上传文件失败
        1003 上传文件成功，插入jira附件失败
    '''
    # 获取真实ip
    # real_ip = request.headers.get('X-Real-Ip', request.remote_addr)
    # print real_ip
    try:
        file = request.files['attachment']  # 从表单的file字段获取文件，myfile为该表单的name值
        bugID = request.form['bugID']
    except:
        _mylogger.error(u'参数异常')
        return jsonify({"errocde":1001 , "errmsg":"参数异常，上传失败"})
    if file and bugID:
        file_path = save_file(file_dir,file)
        _mylogger.info(u'开始往jira往对应bug中插入附件,bugID:%s' %bugID)
        insert = insertToJIRA(bugID, file_path)
        if insert == True:
            os.remove(file_path)
            _mylogger.info(u'插入附件成功，删除本地存储的文件成功！！！')
            return jsonify({"errcode":1000 , "errmsg":"上传文件成功,插入jira附件成功"})
        else :
            _mylogger.error(u'插入附件失败：%s' %insert)
            return jsonify({"errcode":1003 , "errmsg":insert})
    else:
        _mylogger.error(u'参数异常，上传文件或bugID异常：file:{} bugID:{}'.format(request.files['attachment'],request.form['bugID']))
        return jsonify({"errocde":1002 , "errmsg":"参数异常，上传文件失败"})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port =9528,debug=True)