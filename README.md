
#Version check tool

Tool checks version board version of Huawei Transport Platform against the official version list

#Call the tool

./versioncheck.py [Reference File][Inventory File][Output File]

#Requirements

Reference File:
contains at least following informations per board in CSV format either separated by ',' or ';'
'Board BOM Item','Board Type','Subrack Type',Software Version','FPGA Version'

Inventory File:

        self._BOM = dict.get('Board BOM Item')
        self._BRD_TYPE = dict.get('Board Type')
        self._BRD_SW = dict.get('Software Version')
        self._NE_TYPE = dict.get('Subrack Type')
        self._FPGA = dict.get('FPGA Version')
        
        self._SERIAL = dict.get('Board Bar Code',None)
        self._NE_NAME = dict.get('NE',None)
        self._RACK = dict.get('Subrack ID',None)
        self._SLOT = dict.get('Slot ID',None)