#!/usr/bin/python

import sys
import os
import sys
import csv


class CSVfile(object):
    
    def __init__(self,csvfile, resultfile = 'result.csv'):

        self._boardlist = []
        

 #       self._csvfile = csvfile
        self._resultfile = resultfile
        self._tempfile = 'tempfile.csv'
        
        self.Copyfile(csvfile,self._tempfile)
        
    def __del__(self):
 #       os.remove(self._tempfile)
        if os.path.isfile(self._tempfile):
            os.remove(self._tempfile)
            print "Delete Object"
        
    def Copyfile(self, source, dest, buffer_size=1024*1024):
        """
        Copy a file from source to dest. source and dest
        can either be strings or any object with a read or
        write method, like StringIO for example.
        """
        if not hasattr(source, 'read'):
            source = open(source, 'rb')
        if not hasattr(dest, 'write'):
            dest = open(dest, 'wb')

        while 1:
            copy_buffer = source.read(buffer_size)
            if copy_buffer:
                dest.write(copy_buffer)
            else:
                break

        source.close()
        dest.close()


        
    def RemoveHaeder(self):
        readTempfile = file(self._tempfile)
        lines = readTempfile.readlines()
        readTempfile.close()
        
        for n in range(9):
            del lines[0]
        
        writeTempfile= file(self._tempfile,'w')
        
        for line in lines:
            writeTempfile.write(line)
        
        writeTempfile.close()
        
        return True
        
    def detectDelimiter(self,csvFile):
        with open(csvFile, 'r') as myCsvfile:
            header=myCsvfile.readline()
            if header.find(";")!=-1:
                return ";"
            if header.find(",")!=-1:
                return ","
            #default delimiter (MS Office export)
        return ";"

    def OpenFile(self):
        '''
        detect delimiter either ',' or ';'
        '''
        detectDelimiter = self.detectDelimiter(self._tempfile)

        self._reader = csv.DictReader(open(self._tempfile, "rb"),delimiter= detectDelimiter)
        
        for row in self._reader:
            self._boardlist.append(Board(row))
        
        return True
    
    def WriteFile(self,data):
        
  #      print data
        print "Resultfile", self._resultfile
        resultFile = csv.DictWriter(open(self._resultfile,"wb"),
                                ["RESULT","DETAIL","BRD_TYPE", "BOM", "SERIAL", "NE_NAME","NE_TYPE", "RACK",
                                  "SLOT", "SW_EXP", "SW_ACT", "FPGA_EXP", "FPGA_ACT"])
        
        resultFile.writerow({"RESULT":"Result","DETAIL":"Detail","BRD_TYPE":"Board Type", "BOM":"BOM", "SERIAL":"Serial Number",
                         "NE_NAME":"NE Name","NE_TYPE": "NE Type", "RACK":"Rack", 
                         "SLOT":"Slot", "SW_EXP": "SW expected", "SW_ACT": "SW actual", 
                         "FPGA_EXP":"FPGA expected", "FPGA_ACT": "FPGA actual"})
        
        resultFile.writerows(data) 
        
        
        return True
        
    def InstanceList(self):
        return self._boardlist

class Board(object):
    
    def __init__(self,dict):
        self._BOM = dict.get('Board BOM Item')
        self._BRD_TYPE = dict.get('Board Type')
        self._BRD_SW = dict.get('Software Version')
        self._NE_TYPE = dict.get('Subrack Type')
        self._FPGA = dict.get('FPGA Version')
        
        self._SERIAL = dict.get('Board BOM Item',None)
        self._NE_NAME = dict.get('NE',None)
        self._RACK = dict.get('Subrack ID',None)
        self._SLOT = dict.get('Slot ID',None)
                
    def BOM(self):
        return self._BOM

    def BRD_TYPE(self):
        return self._BRD_TYPE
    
    def BRD_SW(self):
        return self._BRD_SW
    
    def NE_TYPE(self):
        return self._NE_TYPE
    
    def FPGA(self, version = 0):
#        print "FPGA", self._FPGA
        if version != 0:
            self._FPGA = version
        return self._FPGA
    
    def NE_NAME(self):
        return self._NE_NAME
    
    def RACK(self):
        return self._RACK
    
    def SLOT(self):
        return self._SLOT
    
    def SERIAL(self):
        return self._SERIAL
    
class Compare(object):
    
    def __init__(self,referenceList,inventoryList):

        self._referenceList = referenceList
        self._inventoryList = inventoryList
        self._result = []
        
    def Search(self, item, value):

        result = getattr(item,value)()
#        print "Search::Result", result
        resultList = []
        
        for referenceItem in self._referenceList:
            referenceValue = getattr(referenceItem, value)()
 #           print "Search Reverence value", referenceValue
            if result.find(referenceValue) > -1:
                resultList.append(referenceItem)
            
  #          if result.find(referenceItem.value()) > -1:
   #             resultList.append(referenceItem) 
                
  #      print "Search::resultLsit", resultList
        return resultList
    
    def Searchnew(self, referenceList, item, value):

        result = getattr(item,value)()
    #    print "Search::Result", result
        resultList = []
        
        for referenceItem in referenceList:
            referenceValue = getattr(referenceItem, value)()
     #       print "Search Reverence value", referenceValue
            if result.find(referenceValue) > -1:
                resultList.append(referenceItem)
            
  #          if result.find(referenceItem.value()) > -1:
   #             resultList.append(referenceItem) 
                
      #  print "Search::resultLsit", resultList
        return resultList
        
    def Filter(self):
        compareState = False
        self._result = []

        for inventoryItem in self._inventoryList:
            validBoard = False
            statusmsg = 'NOK'

            
            ''' 
            if NE type and board found in reference only once -> OK
            else board or NE not defined or multiple definitions of board in reference list
            '''
            referenceList = self.Searchnew(self._referenceList,inventoryItem,'BRD_TYPE')
  #          print "BoardType",len(referenceList)
            
            if len(referenceList) != 0:
                referenceItem = self.Searchnew(referenceList, inventoryItem,'NE_TYPE')
                
   #             print "NE Type",len(referenceList)
                if len(referenceItem) == 1:
                    validBoard = True
                    resultmsg = 'OK'
                elif len(referenceItem) >= 1:
                    validBoard = False
                    detailmsg = 'Multiple Definitions of Board'
                    resultmsg = 'NOK'
                else:
                    validBoard = False
                    detailmsg = "Board not Valid for NE"
                    resultmsg = 'NOK'
            else:
                validBoard = False
                detailmsg = 'Board not Found'
                resultmsg = 'NOK'
                
                
            '''
            if board was found only once in reference list for the NE 
            than verify FPGA and Software version of board
            '''    
            if validBoard == True:
       #         print "FPGA Act", inventoryItem.FPGA(), "expected",referenceItem[0].FPGA()
        #        if '/' in inventoryItem.FPGA():
         #           print "heir"
          #      if 'ZERO' in referenceItem[0].FPGA():
           #         print "nnnn"
                ''' 
                if no FPGA on  board "/" and reference File = 'ZERO'
                '''
                if "/" in inventoryItem.FPGA() and 'ZERO' in referenceItem[0].FPGA():
                    resultmsg = 'OK'
                    detailmsg = 'FPGA::OK'
                    inventoryItem.FPGA('ZERO')
                    '''
                    if FPGA is present on Board
                    '''
                elif inventoryItem.FPGA() == referenceItem[0].FPGA():
                    resultmsg = 'OK'
                    detailmsg = 'FPGA::OK'
         #           print "FPGA found"
                else:
                    resultmsg = 'NOK'
                    detailmsg = 'FPGA::FAILED'
        #            print "FPGA not found", referenceItem[0].FPGA()
                
                ''
                if 'OK' in resultmsg:  
                    if inventoryItem.BRD_SW() == referenceItem[0].BRD_SW():
                        resultmsg = 'OK'
                        detailmsg = detailmsg + ' ' + 'SW::OK'
                    else:
                        resultmsg = 'NOK'
                        detailmsg = detailmsg + ' ' + 'SW::FAILED'
                else:
                    if inventoryItem.BRD_SW() == referenceItem[0].BRD_SW():
                        detailsmsg = detailmsg + ' ' + 'SW::OK'
                    else:
                        resultmsg = 'NOK'
                        detailmsg = detailmsg + ' ' + 'SW::FAILED'
                    
                    
                self._result.append({"RESULT":resultmsg,"DETAIL":detailmsg,"BRD_TYPE":inventoryItem.BRD_TYPE(),"BOM":inventoryItem.BOM(),
                                         "SERIAL":inventoryItem.SERIAL(),"NE_NAME":inventoryItem.NE_NAME(),"RACK":inventoryItem.RACK(),"SLOT":inventoryItem.SLOT(),
                                         "SW_EXP":referenceItem[0].BRD_SW(),"SW_ACT":inventoryItem.BRD_SW(),"FPGA_EXP":referenceItem[0].FPGA(),
                                          "FPGA_ACT":inventoryItem.FPGA()})
            else:
                self._result.append({"RESULT":resultmsg,"DETAIL":detailmsg,"BRD_TYPE":inventoryItem.BRD_TYPE(),"BOM":inventoryItem.BOM(),
                                "SERIAL":inventoryItem.SERIAL(),"NE_NAME":inventoryItem.NE_NAME(),"RACK":inventoryItem.RACK(),"SLOT":inventoryItem.SLOT()}) 
                
 #           print self._result
        return self._result
           
if __name__ == '__main__':
    
    if len(sys.argv) == 4:
        referenceFile = sys.argv[1]
        inventoryFile = sys.argv[2]
        resultFile = sys.argv[3]
        print "Debug Parameter", referenceFile, inventoryFile, resultFile
    else:
        resultFile = 'result.csv'
        inventoryFile = 'inventory.csv'
        referenceFile = 'reference.csv'
        print "parameter missing"
    
    reference = CSVfile(referenceFile)
    reference.OpenFile()
    print "reference", len(reference.InstanceList())
    
    inventory = CSVfile(inventoryFile,resultFile)
    inventory.RemoveHaeder()
    inventory.OpenFile()
    print "Inventory",len(inventory.InstanceList())
    
    compare = Compare(reference.InstanceList(), inventory.InstanceList())
    resultdata = compare.Filter()
    inventory.WriteFile(resultdata)