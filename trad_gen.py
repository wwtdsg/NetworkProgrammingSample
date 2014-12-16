# Traditional Message Generation -- Chapter 9
from email.MIMEText import MIMEText
from email import Utils

message = """Hello,

This is a test message from chapter 9, enjoy it.

-- Anonymous"""

msg = MIMEText(message)
msg['To'] = 'recipient@example.com'
msg['From'] = 'test sender <sender@example.com>'
msg['Subject'] = 'Test message, chapter 9'
msg['Date'] = Utils.formatdate(localtime=1)
msg['Message-ID'] = Utils.make_msgid()
fm = open('message.txt', 'w')
fm.write(msg.as_string())
fm.close()
print msg.as_string()
