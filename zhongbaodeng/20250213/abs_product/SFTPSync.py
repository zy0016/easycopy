import paramiko
import os

class SFTPSync(object):
    Hostname = None
    Port = 22
    transport = None
    sftp = None

    def __init__(self ,host ,port=22):
        print("SFTPSync init")
        self.Hostname = host
        self.Port = port
        self.transport = paramiko.Transport(self.Hostname,self.Port)

    def login(self ,username ,password):
        self.transport.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        print("sftp login succeeded.")

    def close(self):
        if self.sftp is not None:
            try:
                self.sftp.close()
            except Exception as e:
                pass
            finally:
                if self.transport is not None:
                    self.transport.close()

    def upload_dir(self, local_path, ftp_path='.'):
        self.put_dir(local_path,ftp_path)

    def put_dir(self, local_path, ftp_path='.'):
        # 当本地目录存在时上传
        if os.path.isdir(local_path):
            if local_path[-1] == '\\':
                local_path = local_path[0:len(local_path) - 1]
            folder = local_path[local_path.rindex('\\') + 1:len(local_path)]

            for dirpath, dirnames, filenames in os.walk(local_path):
                for filename in filenames:
                    local_file_path = dirpath.strip() + "\\" + filename.strip()
                    path = dirpath[dirpath.index(folder):].replace("\\","/")
                    remote_file_path = ftp_path + "/" + path + "/" + filename
                    remote_folder = ftp_path + "/" + path
                    self.remote_mkdirs(remote_folder)
                    self.sftp.put(local_file_path,remote_file_path)

    def get(self,remote_path,local_path):
        directory = os.path.dirname(local_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.sftp.get(remote_path,local_path)

    def remote_mkdirs(self,ftp_path='.'):
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
                    self.sftp.mkdir(abspath)
                except Exception as e:
                    pass

    def upload_files(self ,filelist, ftp_path='.'):
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
                    self.sftp.mkdir(abspath)
                except Exception as e:
                    pass
        
        for id in filelist:
            idarr = id.split(',')
            self.sftp.put(idarr[0],idarr[1])

if __name__ == '__main__':
    fileDestHost = "192.168.10.96"
    fileDestPort = 22
    fileDestUsername = "root"
    fileDestPassword = "1234qwer!@#$"
    sftp = SFTPSync(fileDestHost,fileDestPort)
    sftp.login(fileDestUsername,fileDestPassword)
    print('上传附件到sftp开始')

    local_path = 'E:\\code\\python\\定时脚本'
    ftp_path = "/home/fileserver/fundcrm/accessory/Tblobstorage"
    sftp.put_dir(local_path,ftp_path)

    print('上传附件到sftp结束')
    sftp.close()
    