import ftplib
import os
import time

class FTPSync(object):
    conn = ftplib.FTP()
    conn.encoding ='UTF-8'

    def __init__(self ,host ,port=21):
        self.savelog("connect to " + str(host) + " " + str(port))
        self.conn.connect(host ,port,60*1000)
        self.savelog("connect successful")

    def login(self ,username ,password):
        self.savelog("login to " + username)
        self.conn.login(username ,password)
        self.conn.set_pasv(True)
        self.savelog(self.conn.welcome)

    def close(self):
        self.conn.close()

    def test(self ,ftp_path):
        print(ftp_path)
        print(self._is_ftp_dir(ftp_path))
        # print self.conn.nlst(ftp_path)
        # self.conn.retrlines( 'LIST ./a/b')
        # ftp_parent_path = os.path.dirname(ftp_path)
        # ftp_dir_name = os.path.basename(ftp_path)
        # print ftp_parent_path
        # print ftp_dir_name


    def _is_ftp_file(self ,ftp_path):
        try:
            if ftp_path in self.conn.nlst(os.path.dirname(ftp_path)):
                return True
            else:
                return False
        except ftplib.error_perm as e:
            return False

    def _ftp_list(self, line):
        list = line.split(' ')
        if self.ftp_dir_name == list[-1] and list[0].startswith('d'):
            self._is_dir = True

    def _is_ftp_dir(self ,ftp_path):
        ftp_path = ftp_path.rstrip('/')
        ftp_parent_path = os.path.dirname(ftp_path)
        self.ftp_dir_name = os.path.basename(ftp_path)
        self._is_dir = False
        if ftp_path == '.' or ftp_path== './' or ftp_path == '':
            self._is_dir = True
        else:
            # this ues callback function ,that will change _is_dir value
            try:
                self.conn.retrlines('LIST %s' %ftp_parent_path, self._ftp_list)
            except ftplib.error_perm as e:
                return self._is_dir
        return self._is_dir


    def get_file(self, ftp_path, local_path='.'):
        ftp_path = ftp_path.rstrip('/')
        if self._is_ftp_file(ftp_path):
            file_name = os.path.basename(ftp_path)
            # 如果本地路径是目录，下载文件到该目录
            if os.path.isdir(local_path):
                file_handler = open(os.path.join(local_path, file_name), 'wb')
                self.conn.retrbinary("RETR %s" % (ftp_path), file_handler.write)
                file_handler.close()
            # 如果本地路径不是目录，但上层目录存在，则按照本地路径的文件名作为下载的文件名称
            elif os.path.isdir(os.path.dirname(local_path)):
                file_handler = open(local_path, 'wb')
                self.conn.retrbinary("RETR %s" % (ftp_path), file_handler.write)
                file_handler.close()
            # 如果本地路径不是目录，且上层目录不存在，则退出
            else:
                print
                'EROOR:The dir:%s is not exist' % os.path.dirname(local_path)
        else:
            print
            'EROOR:The ftp file:%s is not exist' % ftp_path


    def put_file(self, local_path, ftp_path='.'):
        ftp_path = ftp_path.rstrip('/')
        if os.path.isfile(local_path):
            # file_handler = codecs.open(local_path, "r")
            file_handler = open(local_path, "rb")
            local_file_name = os.path.basename(local_path)
            # 如果远程路径是个目录，则上传文件到这个目录，文件名不变
            if self._is_ftp_dir(ftp_path):
                self.conn.storbinary('STOR %s' % os.path.join(ftp_path, local_file_name), file_handler)
            # 如果远程路径的上层是个目录，则上传文件，文件名按照给定命名
            elif self._is_ftp_dir(os.path.dirname(ftp_path)):
                print
                'STOR %s' % ftp_path
                self.conn.storbinary('STOR %s' % ftp_path, file_handler)
            # 如果远程路径不是目录，且上一层的目录也不存在，则提示给定远程路径错误
            else:
                print
                'EROOR:The ftp path:%s is error' % ftp_path
            file_handler.close()
        else:
            print
            'ERROR:The file:%s is not exist' % local_path


    def get_dir(self, ftp_path, local_path='.', begin=True):
        ftp_path = ftp_path.rstrip('/')
        # 当ftp目录存在时下载
        if self._is_ftp_dir(ftp_path):
            # 如果下载到本地当前目录下，并创建目录
            # 下载初始化：如果给定的本地路径不存在需要创建，同时将ftp的目录存放在给定的本地目录下。
            # ftp目录下文件存放的路径为local_path=local_path+os.path.basename(ftp_path)
            # 例如：将ftp文件夹a下载到本地的a/b目录下，则ftp的a目录下的文件将下载到本地的a/b/a目录下
            if begin:
                if not os.path.isdir(local_path):
                    os.makedirs(local_path)
                local_path = os.path.join(local_path, os.path.basename(ftp_path))
            # 如果本地目录不存在，则创建目录
            if not os.path.isdir(local_path):
                os.makedirs(local_path)
            # 进入ftp目录，开始递归查询
            self.conn.cwd(ftp_path)
            ftp_files = self.conn.nlst()
            for file in ftp_files:
                local_file = os.path.join(local_path, file)
                # 如果file ftp路径是目录则递归上传目录（不需要再进行初始化begin的标志修改为False）
                # 如果file ftp路径是文件则直接上传文件
                if self._is_ftp_dir(file):
                    self.get_dir(file, local_file, False)
                else:
                    self.get_file(file, local_file)
            # 如果当前ftp目录文件已经遍历完毕返回上一层目录
            self.conn.cwd("..")
            return
        else:
            print
            'ERROR:The dir:%s is not exist' % ftp_path
            return


    # def put_dir(self, local_path, ftp_path='.', begin=True):
    #     tmpftp_path = ftp_path.rstrip('/')
    #     # 当本地目录存在时上传
    #     if os.path.isdir(local_path):
    #         print(local_path)
    #         # 上传初始化：如果给定的ftp路径不存在需要创建，同时将本地的目录存放在给定的ftp目录下。
    #         # 本地目录下文件存放的路径为ftp_path=ftp_path+os.path.basename(local_path)
    #         # 例如：将本地文件夹a上传到ftp的a/b目录下，则本地a目录下的文件将上传的ftp的a/b/a目录下
    #         if begin:
    #             if not self._is_ftp_dir(tmpftp_path):
    #                 self.conn.mkd(tmpftp_path)
    #             tmpftp_path = os.path.join(ftp_path, os.path.basename(local_path))
    #             # 如果ftp路径不是目录，则创建目录
    #         if not self._is_ftp_dir(tmpftp_path):
    #             self.conn.mkd(tmpftp_path)

    #         # 进入本地目录，开始递归查询
    #         os.chdir(local_path)
    #         local_files = os.listdir('.')
    #         for file in local_files:
    #             # 如果file本地路径是目录则递归上传目录（不需要再进行初始化begin的标志修改为False）
    #             # 如果file本地路径是文件则直接上传文件
    #             if os.path.isdir(file):
    #                 print(file)
    #                 ftp_path = os.path.join(tmpftp_path, file)
    #                 self.put_dir(file, tmpftp_path+os.path.sep+str(file), False)
    #             else:
    #                 print(file)
    #                 self.put_file(file, tmpftp_path)
    #         # 如果当前本地目录文件已经遍历完毕返回上一层目录
    #         os.chdir("..")
    #     else:
    #         print('ERROR:The dir:%s is not exist' % local_path)
    #         return

    def put_dir(self, local_path, ftp_path='.'):
        self.savelog("put_dir:" + local_path + " ->" + ftp_path)
        # 当本地目录存在时上传
        if os.path.isdir(local_path):
            if local_path[-1] == '\\':
                local_path = local_path[0:len(local_path) - 1]
            # 只获得本地目录名
            folder = local_path[local_path.rindex('\\') + 1:len(local_path)]

            # 遍历本地目录下所有文件
            for dirpath, dirnames, filenames in os.walk(local_path):
                for filename in filenames:
                    #本地文件名
                    local_file_path = dirpath.strip() + "\\" + filename.strip()
                    path = dirpath[dirpath.index(folder):].replace("\\","/")
                    #远端文件名
                    remote_file_path = ftp_path + "/" + path + "/" + filename
                    remote_folder = ftp_path + "/" + path
                    self.remote_mkdirs(remote_folder)
                    self.savelog(local_file_path + " -> " + remote_file_path)
                    #开始上传文件
                    file_handler = open(local_file_path, "rb")
                    self.conn.storbinary("STOR " + remote_file_path, file_handler, 1024)
                    file_handler.close()
        else:
            self.savelog("无法找到目录：" + local_path)

    def remote_mkdirs(self,ftp_path='.'):
        #创建远端目录，支持多级目录
        remote_sep = "/"
        tmpftp_path = ftp_path.rstrip('/')
        dirarr = tmpftp_path.split(remote_sep)
        abspath = "/"
        for i in dirarr:
            p1 = str(i)
            p2 = p1.strip()
            if len(p2) > 0:
                abspath = abspath + p2 + remote_sep
                try:
                    self.conn.mkd(abspath)
                except Exception as e:
                    pass

    def savelog(self,strsen, display = True):
        if display:
            print(strsen)

        try:
            resultfile = open("FTPdebug.log",'a+')
            resultfile.write("[" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "]" + strsen + "\n")
            resultfile.close()
        except Exception as e:
            pass

if __name__ == '__main__':
    ftp = FTPSync('192.168.19.110')
    ftp.login('admin', 'bjkf@2017')
    # 上传文件，不重命名
    # ftp.put_file('111.txt','a/b')
    # 上传文件，重命名
    # ftp.put_file('111.txt','a/112.txt')
    # 下载文件，不重命名
    # ftp.get_file('/a/111.txt',r'D:\\')
    # 下载文件，重命名
    # ftp.get_file('/a/111.txt',r'D:\112.txt')
    # 下载到已经存在的文件夹
    # ftp.get_dir('a/b/c',r'D:\\a')
    # 下载到不存在的文件夹
    # ftp.get_dir('a/b/c',r'D:\\aa')
    # 上传到已经存在的文件夹
    # ftp.put_dir('b', 'a')
    # 上传到不存在的文件夹
    #ftp.put_dir('b', 'aa/B/')
    ftp.put_dir('C:\\estimate\\fundcrmfile\\20241218','./')
