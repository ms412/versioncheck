#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Copyright (c) 2014 Markus Schiesser.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the GNU Public License v3.0
# which accompanies this distribution, and is available at
# http://www.gnu.org/licenses/gpl.html
# 
# Contributors:
#     Markus Schiesser - initial API and implementation
#-------------------------------------------------------------------------------

import sys
import os
import sys
import csv

from libemail import smtpHandle


class CSVfile(object):
    '''
    opens CSV file and creates a object instance for each board
    '''
    
    def __init__(self,csvfile, resultfile = 'result.csv'):

        self._boardlist = []
        
        self._resultfile = resultfile
        self._tempfile = 'tempfile.temp'
        
        self.Copyfile(csvfile,self._tempfile)
        
    def __del__(self):
        ''' 
        delete the tempfile if it exists
        '''
        
        if os.path.isfile(self._tempfile):
            os.remove(self._tempfile)
        
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
        '''
        remove first ten lines of Inventory file as it get created by U2000
        '''
        
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
        ''' 
        detects the delimiter between lines in CVS file
        either ',' or ';'
        '''
        
        with open(csvFile, 'r') as myCsvfile:
            header=myCsvfile.readline()
            if header.find(";")!=-1:
                return ";"
            if header.find(",")!=-1:
                return ","
        return ";"

    def OpenFile(self):
        '''
        open files
        detects delimiter of CSV file
        and creates Board instances for each line in file
        '''
        detectDelimiter = self.detectDelimiter(self._tempfile)

        self._reader = csv.DictReader(open(self._tempfile, "rb"),delimiter= detectDelimiter)
        
        for row in self._reader:
            self._boardlist.append(Board(row))
        
        return True
    
    def WriteFile(self,data):
        '''
        writes result to file
        expects a list of dictionaries
        '''
        resultFile = csv.DictWriter(open(self._resultfile,"wb"),
                                ["RESULT","DETAIL","BRD_TYPE", "BOM", "SERIAL", "NE_NAME","NE_TYPE", "RACK",
                                  "SLOT", "SW_EXP", "SW_ACT", "FPGA_EXP", "FPGA_ACT"], delimiter = ";")
        
        resultFile.writerow({"RESULT":"Result","DETAIL":"Detail","BRD_TYPE":"Board Type", "BOM":"BOM", "SERIAL":"Serial Number",
                         "NE_NAME":"NE Name","NE_TYPE": "NE Type", "RACK":"Rack", 
                         "SLOT":"Slot", "SW_EXP": "SW expected", "SW_ACT": "SW actual", 
                         "FPGA_EXP":"FPGA expected", "FPGA_ACT": "FPGA actual"})
        
        resultFile.writerows(data) 
        
        return True
        
    def InstanceList(self):
        '''
        returns the list of pointers of instances of the Boards
        '''
        return self._boardlist

class Board(object):
    
    def __init__(self,dict):
        ''' 
        creates a board instance
        '''
        self._BOM = dict.get('Board BOM Item')
        self._BRD_TYPE = dict.get('Board Type')
        self._BRD_SW = dict.get('Software Version')
        self._NE_TYPE = dict.get('Subrack Type')
        self._FPGA = dict.get('FPGA Version')
        
        self._SERIAL = dict.get('Board Bar Code',None)
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
        ''' 
        returns the FPGA version if the version is not set
        or overwritten by version if != 0
        '''
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
        '''
        class compares the reference with inventory list
        '''

        self._referenceList = referenceList
        self._inventoryList = inventoryList
        self._result = []
    
    def Search(self, referenceList, item, value):
        '''
        search in reference list for value present in item instance and reference list
        '''

        result = getattr(item,value)()
        resultList = []
        
        for referenceItem in referenceList:
            referenceValue = getattr(referenceItem, value)()
            if result.find(referenceValue) > -1:
                resultList.append(referenceItem)

        return resultList
        
    def Filter(self):
        compareState = False
        self._result = []

        for inventoryItem in self._inventoryList:
            validBoard = False
            resultmsg = 'EMPTY'
            detailmsg = 'EMPTY'
            ne_type = 'UNKNOWN'

            
            ''' 
            if NE type and board found in reference only once -> OK
            else board or NE not defined or multiple definitions of board in reference list
            '''
            referenceList = self.Search(self._referenceList,inventoryItem,'BRD_TYPE')
            
            if len(referenceList) != 0:
                referenceItem = self.Search(referenceList, inventoryItem,'NE_TYPE')
                
                if len(referenceItem) == 1:
                    validBoard = True
                    resultmsg = 'OK'
                    ne_type = referenceItem[0].NE_TYPE()
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
                else:
                    resultmsg = 'NOK'
                    detailmsg = 'FPGA::FAILED'
                
                if 'NOK' not in resultmsg:  
                    if inventoryItem.BRD_SW() == referenceItem[0].BRD_SW():
                        resultmsg = 'OK'
                        detailmsg = detailmsg + ' ' + 'SW::OK'
                    else:
                        resultmsg = 'NOK'
                        detailmsg = detailmsg + ' ' + 'SW::FAILED'
                else:
                    if inventoryItem.BRD_SW() == referenceItem[0].BRD_SW():
                        detailmsg = detailmsg + ' ' + 'SW::OK'
                    else:
                        resultmsg = 'NOK'
                        detailmsg = detailmsg + ' ' + 'SW::FAILED'
                    
                    
                self._result.append({"RESULT":resultmsg,"DETAIL":detailmsg,"BRD_TYPE":inventoryItem.BRD_TYPE(),"BOM":inventoryItem.BOM(),
                                         "SERIAL":inventoryItem.SERIAL(),"NE_NAME":inventoryItem.NE_NAME(),"NE_TYPE":ne_type,"RACK":inventoryItem.RACK(),"SLOT":inventoryItem.SLOT(),
                                         "SW_EXP":referenceItem[0].BRD_SW(),"SW_ACT":inventoryItem.BRD_SW(),"FPGA_EXP":referenceItem[0].FPGA(),
                                          "FPGA_ACT":inventoryItem.FPGA()})
            else:
                self._result.append({"RESULT":resultmsg,"DETAIL":detailmsg,"BRD_TYPE":inventoryItem.BRD_TYPE(),"BOM":inventoryItem.BOM(),
                                "SERIAL":inventoryItem.SERIAL(),"NE_NAME":inventoryItem.NE_NAME(),"NE_TYPE":ne_type,"RACK":inventoryItem.RACK(),"SLOT":inventoryItem.SLOT()}) 

        return self._result
           
if __name__ == '__main__':
    
    if len(sys.argv) == 4:
        referenceFile = sys.argv[1]
        inventoryFile = sys.argv[2]
        resultFile = sys.argv[3]
    else:
        print "Start tool with following parameter./versioncheck.py [Reference File][Inventory File][Output File]"
    
    reference = CSVfile(referenceFile)
    reference.OpenFile()
    
    inventory = CSVfile(inventoryFile,resultFile)
    inventory.RemoveHaeder()
    inventory.OpenFile()
    
    print "Number of Reference Objects:",len(reference.InstanceList())
    print "Number of Inventory Objects:",len(inventory.InstanceList())
    
    print "Verifiy Software and FPGA"
    compare = Compare(reference.InstanceList(), inventory.InstanceList())
    resultdata = compare.Filter()
    inventory.WriteFile(resultdata)
    
    print "Send libemail...."
    smtp = smtpHandle('gd2imail.swissptt.ch')            
    smtp.attachement(resultFile)
    smtp.send_to('Markus.Schiesser@swisscom.com')

    smtp.send_from('VersionCheck@sonate.com')
    smtp.subject('VersionCheck')
    smtp.message('VersionCheck Result')
    smtp.sendMail()
