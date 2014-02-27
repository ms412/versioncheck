'''
Created on Feb 27, 2014

@author: oper
'''

import smtplib
import os
import sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders


class smtpHandle(object):
    '''
    classdocs
    '''

    def __init__(self, smtpServer='gd2imail.swissptt.ch', sendFrom = 'automailer@swisscom.com'):
        '''
        Constructor
        '''
        self._smtpServer = smtpServer
        
        self._sendFrom = sendFrom
        self._sendToList = []
        
        self._date = formatdate(localtime=True)
        self._subject = ''
        self._message = ''
        self._attachement =[]
        
    def send_to(self,sendTo):
        
        self._sendToList.append(sendTo)
        
    def send_from(self,sendFrom):
        
        self._sendFrom = sendFrom
        
    def connectSmtp(self):
        
        self._smtp = smtplib.SMTP(self._smtpServer)
        
    def disconnectSmtp(self):
        
        self._smtp.close()    
        
    def sendSmtp(self, mailmsg):
        
        for sendTo in self._sendToList:
            self._smtp.sendmail(self._sendFrom, sendTo,mailmsg.as_string())
               
    def subject(self,subject):
        
        self._subject = subject
        
    def message(self, msg):
        
        self._message = msg
        
    def attachement(self, attachement):
        
        self._attachement.append(attachement)
        
    def sendMail(self):
        
        mailmsg = MIMEMultipart()
        mailmsg['From'] = self._sendFrom
        mailmsg['To'] = COMMASPACE.join(self._sendToList)
        mailmsg['Date'] = self._date
        mailmsg['Subject'] = self._subject
        
        mailmsg.attach(MIMEText(self._message))
        
        if self._attachement >= 1:
            for filename in self._attachement:
                part = MIMEBase('application', "octet-stream")
                part.set_payload( open(filename,"rb").read() )
                Encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(filename))
                mailmsg.attach(part)

        self.connectSmtp()
        self.sendSmtp(mailmsg)
        self.disconnectSmtp()
    
if __name__ == '__main__':


    smtp = smtpHandle('gd2imail.swissptt.ch')

    for i in range(len(sys.argv)):
        if i == 0:
            print "firts",(sys.argv[i])
        else:
            smtp.attachement(sys.argv[i])

    smtp.send_to('Markus.Schiesser@swisscom.com')
    smtp.send_to('M.Schiesser@gmail.com')
    smtp.send_to('tgdscm41@gmail.com')
    smtp.send_from('Test@swisscom.com')
    smtp.subject('Subject1234')
    smtp.message('Test,TEST.test')
    smtp.sendMail()

        