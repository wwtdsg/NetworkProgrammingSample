# Traditional message pasing -- chapter 9

import sys, email

msg = email.message_from_file(sys.stdin)
# input: < message.txt
print '*** headers in message:'
for header, value in msg.items():
    print header + ": "
    print value

if msg.is_multipart():
    print "This program cannot handle MIME multipart messages; exiting."
    sys.exit(1)

print '-' * 78
if 'Subject' in msg:
    print 'Subject: ', msg['Subject']
    print '-' * 78
print 'Message Body:'
print

print msg.get_payload()
