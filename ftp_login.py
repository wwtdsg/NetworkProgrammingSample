#! -*- encoding:utf-8 -*-
"""
常用ftp操作命令：
 ftp.getwelcome()  获取欢迎语
 ftp.pwd()  获取当前所在目录
 ftp.dir()  显示当前目录下的文件信息
 ftp.cwd('xxx/xxx') 更改远程目录
 ftp.quit()
 ftp.mkd(pathname)
 ftp.rmd(dirname)
 ftp.delete(filename)
 ftp.rename(fromname, toname)
 ftp.storbinary("STOR filename.txt", file, bufsize=8192)  上传目标文件，
                        file是一个打开的文件对象,bufsize是传输中使用的数据块大小。
 ftp.connect(IP，PORT)
 ftp.login(user, password)
"""
"""
这个脚本的主要功能：

借助于QPython，在android手机上搭建一个ftp服务器，
使用和手机在同一个局域网中的电脑，可以将电脑本地
文本文件发送到手机端，从而实现快速文件传递，免去
数据线等麻烦问题。

需注意的是，本脚本只在同一个局域网下的服务器中测
试通过，现在只支持在同一个局域网中的文本文件传输。

author： wwtdsg
version: 1.0
date: 2015.03.23

"""
import ftplib
from ftplib import FTP
import sys


class ftplog:
    def __init__(self):
        self.username = 'wwtdsg'
        self.password = 'wwtdsg'
        self.ftp = FTP()
        # url = raw_input('input server address: ')
        self.url = '10.180.56.154'
        self.port = '2121'

    def login(self):
        print 'Connecting...'
        try:
            self.ftp.connect(self.url, self.port)
            self.ftp.login(self.username, self.password)
        except:
            print "连接失败，请检查网络是否正常，或尝试重启电脑。"
            sys.exit(1)

    def logout(self):
        self.ftp.quit()

    def file_send(self):
        # 暂时只允许将文件发送到scripts文件夹
        self.ftp.cwd('scripts')
        self.ftp.dir()
        count = 5
        while True:
            count = count - 1
            filename = raw_input('输入文件名： ')
            try:
                file_opretor = open(filename)
                break
            except IOError, e:
                print str(e) + "文件名输入错误，请重试："
                if count is 0:
                    print "超过最大输入错误次数。"
                    sys.exit(1)
        self.ftp.storbinary("STOR %s" % filename, file_opretor)
        print "文件上传成功！"
        
    def file_delete(self):
        self.ftp.cwd('scripts')
        count = 5
        while True:
            count -= 1
            filename = raw_input('输入想要删除的文件名：')
            try:
                self.ftp.delete(filename)
                print '删除成功'
                break
            except ftplib.error_temp, e:
                print str(e) + '  请重新输入'
            except ftplib.error_parm, e:
                print str(e) + '  请重新输入'
            if count is 0:
                print "超过最大输入错误次数，删除未遂。"
                break
        

def main():
    print '命令提示：\n\n发送：send\n删除：delete\n查看脚本目录：view\n'
    cmd = raw_input('请输入命令：')

    my_android = ftplog()
    my_android.login()
    print '----------------------'
    try:
        if cmd == 'send':
            my_android.file_send()
        elif cmd == 'delete':
            my_android.file_delete()
        elif cmd == 'view':
            my_android.ftp.cwd('scripts')
            my_android.ftp.dir()
        else:
            print '傻逼，命令输错了！'
    finally:
        my_android.logout()
    print '----------------------'

if '__main__' == __name__:
    main()
