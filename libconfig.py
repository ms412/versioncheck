from ConfigParser import ConfigParser
import re

class Config(object):
    
    def __init__(self):
    
        self._config = ConfigParser()
    
    def Open(self,filename):
        
        self._config.read(filename)
        
        return True
    
    def GetSection(self,pattern):
          
        sectionlist = []

        for item in self._config.sections():
            if re.match(pattern,item) != None:
                sectionlist.append(item)
                 
        return sectionlist
    
    def GetConfig(self,section,pattern):
    
        return self._config.get(section,pattern)
        
if __name__ == '__main__':
    
    test=Config()
    test.Open('config')
    sectionlist = test.GetSection('Server[0-9]+')
    print test.GetSection('Test')
    
    if sectionlist > 0:
        for section in sectionlist:
            print test.GetConfig(section,'user')
    
    
    
    
    
#     config = ConfigParser()
#     config.read('config')
#     print config._sections
#     print config.sections()
#     
#     print config.get('Server1','user')
#     for item in config.sections():
#         sect = re.match("Server[0-9]+",item)
#         if sect:
#             print item
        #print config.get(sect,'hostname')
        #print config.get(sect,'user')
    


 