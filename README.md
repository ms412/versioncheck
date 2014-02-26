
## Version check tool

Tool checks version board version of Huawei Transport Platform against the official version list

### Call the tool

./versioncheck.py [Reference File][Inventory File][Output File]

### Requirements

##### 1. Reference File:
contains at least following informations per board in CSV format either separated by `,` or `;`
+ Board BOM Item
+ Board Type
+ Subrack Type
+ Software Version
+ FPGA Version

##### 2. Inventory File:

+ Board BOM Item
+ Board Type
+ Subrack Type
+ Software Version
+ FPGA Version
+ Board Bar Code
+ NE
+ Subrack ID
+ Slot ID
