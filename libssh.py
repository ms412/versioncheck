
import paramiko

class SSH(object):
    
    def __init__(self,user,passwd,host,path,filename,port = 22):
        
        self._user = user
        self._passwd = passwd
        self._host = host
        self._path = path
        self._file = filename
        self._port = port

    def ssh_Connection(self):
        try:
            self._ssh = paramiko.SSHClient()
            self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._ssh.connect(self._host,self._user,self._passwd)

        except Exception, e:
            print "================================================"
            print 'ERROR: Remote connection failed with %s' % e
            print "================================================"


    def ssh_SearchFile(self):
        
        result = []
        
        command = 'find' + ' ' + self._path + ' ' + '-name' + ' ' + self._file
        
        try:
            stdin, stdout, stderr =self._ssh.exec_command(command)
        
            for line in stdout:
                result.append(line.strip('\n'))
                print result
            
        except Exception, e:
            print "================================================"
            print 'ERROR: Commands Execution failed with %s' % e
            print "================================================"
            
        finally:    
            self._ssh.close() 

        return result
    
    def sftp_Copy(self, source, dest):
        
        try:    
            self._sftp = paramiko.Transport((self._host, self._port))
            self._sftp.connect(self._user, self._passwd)    
            sftp = paramiko.SFTPClient.from_transport(self._sftp)
            sftp.get(source, dest)
            
        finally:    
            self._sftp.close() 

    
if __name__ == "__main__":
    
    a = SSH('tgdscm41','Swisscom10','hsonedp1','/opt/oss/client/client/report/inventoryDump','Board_Report*')
    a.ssh_Connection()
    result = a.searchFile()

    if result > 0:
        for item in result:
            a.sftp_Copy(item,'./temp')
            