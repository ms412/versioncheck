
import paramiko

class SSH(object):
    
    def __init__(self,user,passwd,host,port = 22):
        
        self._user = user
        self._passwd = passwd
        self._host = host
        self._port = port

    def ssh_Connect(self):
        
        try:
            self._ssh = paramiko.SSHClient()
            self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._ssh.connect(self._host,username=self._user,password=self._passwd)
        except Exception, e:
            print "================================================"
            print 'ERROR: Remote connection failed with %s' % e
            print "================================================"

    def ssh_Dissconnet(self):
        
        try:
            self._ssh.close()
        except Exception, e:
            print "================================================"
            print 'ERROR: Commands Execution failed with %s' % e
            print "================================================"
            

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
        
#         try:
#             stdin, stdout, stderr =self._ssh.exec_command(command)
        
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
        
        try:    
            self._sftp = paramiko.Transport((self._host, self._port))
            self._sftp.connect(self._user, self._passwd)    
            sftp = paramiko.SFTPClient.from_transport(self._sftp)
            sftp.get(source, dest)
            
        finally:    
            self._sftp.close() 

    
if __name__ == "__main__":
    
    a = SSH('tgdscm41','Swisscom10','hsonedp1','/opt/oss/client/client/report/inventoryDump','Board_Report*')
    a.ssh_Connect()
    result = a.ssh_Find('/opt/oss/client/client/report/inventoryDump','Board_Report*')
    result = a.ssh_SearchFile()

    if result > 0:
        for item in result:
            a.ssh_Copy(item,'./temp')
            
        for item in result:
            a.ssh_Delet(item)   
            
    a.ssh_Disconnet()