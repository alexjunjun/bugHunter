#coding:utf-8
from werkzeug.utils import secure_filename
from flask import  Flask ,render_template ,jsonify , request

import time
import os
import correlationToJIRA as toJIRA

app = Flask(__name__)
UPLOAD_FOLDER = 'uploadFiles'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))



#用于删除插入jira附件成功的文件
def dele_file(file):
    os.remove(file)
    print u'删除文件成功！！！'


#用于测试提交表单的页面
@app.route('/test/upload')
def upload_tst():
    return render_template('upload.html')


#用于上传文件
@app.route('/bughunter/upload' , methods=['POST'] , strict_slashes= False)
def api_upload():
    '''
    用于接收客户端提交的文件和bugID
    请求方式：POST
    参数：attachment、bugID
    返回值：
    1000 上传文件成功,插入jira附件成功
    1001 参数异常，上传失败
    1002 参数为空，上传文件失败
    1003 上传文件成功，插入jira附件失败
    :return:
    '''
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    try:
        file = request.files['attachment']  # 从表单的file字段获取文件，myfile为该表单的name值
        bugID = request.form['bugID']
    except:
        return jsonify({"errocde":1001 , "errmsg":"参数异常，上传失败"})
    if file and bugID:
        fname = secure_filename(file.filename)
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        file_name_temp = fname.rsplit('.', 1)[0]
        unix_time = int(time.time())
        file_name = file_name_temp + str(unix_time) + '.' + ext
        file_path = os.path.join(file_dir, file_name)
        file.save(file_path)
        print 'bugID:' , bugID
        print 'file path:' , file_path ,u'文件保存成功'
        insert = toJIRA.insertToJIRA(bugID ,file_path)
        if insert == True:
            dele_file(file_path)
            return jsonify({"errcode":1000 , "errmsg":"上传文件成功,插入jira附件成功"})
        else :
            return jsonify({"errcode":1003 , "errmsg":insert})
    else:
        return jsonify({"errocde":1002 , "errmsg":"参数为空，上传文件失败"})

if __name__ == '__main__':
    app.run(host='10.3.20.32',port =8000,debug=True)