
import paramiko

class SSH(object):
    
    def __init__(self,user,passwd,host,port = 22):
        
        self._user = user
        self._passwd = passwd
        self._host = host
        self._port = port

    def ssh_Connect(self):
        
        result = False
        try:
            self._ssh = paramiko.SSHClient()
            self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._ssh.connect(self._host,username=self._user,password=self._passwd)
            result = True
        except Exception, e:
            print "================================================"
            print 'ERROR: Remote connection failed with %s' % e
            print "================================================"
            
        return result

    def ssh_Disconnet(self):
        
        result = False
        try:
            self._ssh.close()
            result = True
        except Exception, e:
            print "================================================"
            print 'ERROR: Commands Execution failed with %s' % e
            print "================================================"

        return result

    def ssh_Command(self,cmd):
        
        try:
            stdin, stdout, stderr =self._ssh.exec_command(cmd)
        except Exception, e:
            print "================================================"
            print 'ERROR: Commands Execution failed with %s' % e
            print "================================================"
            
        return (stdin,stdout,stderr)
            
    def ssh_Find(self,path, filename):
        
        result = []
        
        cmd = 'find' + ' ' + path + ' ' + '-name' + ' ' + filename
        
        (stdin, stdout, stderr) =self.ssh_Command(cmd)
        
        for line in stdout:
            result.append(line.strip('\n'))
            print result

        return result
    
    def ssh_Delet(self, path, filename = ''):
        
        cmd = 'rm' + ' ' + path + filename
        
        (stdin, stdout, stderr) =self.ssh_Command(cmd)
        print "DEL", stdout
        
        return stdout        
    
    def ssh_Copy(self, source, dest):
        
        result = False
        try:    
            self._sftp = paramiko.Transport((self._host, self._port))
            self._sftp.connect(username=self._user, password=self._passwd)    
            sftp = paramiko.SFTPClient.from_transport(self._sftp)
            sftp.get(source, dest)
            
        except Exception, e:
            print "================================================"
            print 'ERROR: Commands Execution failed with %s' % e
            print "================================================"
            
        finally:    
            self._sftp.close() 
            result = True

        return result
    
    
class GetFiles(object):
    
    def __init__(self,host,user,passwd,path,filename,tempdir):
        self._host = host
        self._user = user
        self._passwd = passwd
        self._path = path
        self._filename = filename
        self._tempdir = tempdir

    def Connect(self):
        result = False
        result_txt = 'NOK'
        sshHandle = SSH(self._user,self._passwd,self._host)
        
        if sshHandle.ssh_Connect()== True:
            filelist = sshHandle.ssh_Find(self._path,self._filename)
            
            if filelist > 0:
                for item in filelist:
                    sshHandle.ssh_Copy(item,self._tempdir)
                    
                for item in filelist:
                    sshHandle.ssh_Delet(item)
                    result = True
                    result_txt = 'OK'
            else:
                result_txt = 'NoFiles'
                result = False
        else:
            result_txt = 'NoServer'
            result = False
            
        sshHandle.ssh_Disconnet()
        return (result,result_txt)

# if __name__ == "__main__":
#     
#     def GetFiles():
#     
#     a = SSH('tgdscm41','Swisscom10','hsonedp1')
#     a.ssh_Connect()
#     result = a.ssh_Find('/opt/oss/client/client/report/inventoryDump','Board_Report*')
#     result = a.ssh_SearchFile()
# 
#     if result > 0:
#         for item in result:
#             a.ssh_Copy(item,'./temp')
#             
#         for item in result:
#             a.ssh_Delet(item)   
#             
#     a.ssh_Disconnet()