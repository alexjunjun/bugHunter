# coding= utf-8
import os
import time
from werkzeug.utils import secure_filename

from lib.log_config import get_logger

_mylogger = get_logger('bugHunter')
def save_file(file_dir,file):
    fname = secure_filename(file.filename)
    ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
    file_name_temp = fname.rsplit('.', 1)[0]
    unix_time = int(time.time())
    file_name = file_name_temp + str(unix_time) + '.' + ext
    file_path = os.path.join(file_dir, file_name)
    file.save(file_path)
    _mylogger.info(u'文件接收并保存成功:%s' %file_path)
    return file_path