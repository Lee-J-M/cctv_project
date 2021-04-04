import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from pushbullet import PushBullet
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


me = "jimin778@gmail.com"
you = "jimin778@gmail.com"


google_server = smtplib.SMTP('smtp.gmail.com', 587)
google_server.starttls()
google_server.login('jimin778@gmail.com','rtkfkdgo!7')

msg = MIMEBase('multipart', 'mixed')

contents = "[CCTV] \n Check only the latest email(including all phothos sent so far)"

cont = MIMEText(contents, _charset = "euc-kr")
cont['Subject'] = '[CCTV]'
cont['From'] = me
cont['To'] = you
msg.attach(cont)

api_key = "o.hMRCQwU6kHg4QaRSW5KjPWg3K3GP6tlN"

pb = PushBullet(api_key)

GPIO.setmode(GPIO.BCM)

pirPin = 7
LED = 13

GPIO.setup(pirPin, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(LED, GPIO.OUT)
camera = PiCamera()
counter = 1



while True:
  if GPIO.input(pirPin):
    GPIO.output(LED, True)
    print "Motion detected!"

    try:
      camera.start_preview()
      camera.capture('/home/pi/image%s.jpg' % counter)
      camera.stop_preview()
      path = "/home/pi/image%s.jpg" % counter  
      part = MIMEBase("application", "octet-stream")
      part.set_payload(open(path,'rb').read())
      encoders.encode_base64(part)
      part.add_header('Content-Disposition','attachment; filename = "%s"' %os.path.basename(path))
      msg.attach(part)
      google_server.sendmail(me, you , msg.as_string())
      push = pb.push_note("[CAUTION!!]", "Motion Detected!")
      time.sleep(2)
      push = pb.push_link("Click here to check CCTV " ,"https://mail.google.com/mail/u/0/?ogbl#inbox")
      counter = counter + 1

      ## CCTV VIDEO  ##
      #camera.start_preview()
      #camera.start_recording('/home/pi/video%s.h264' % counter)
      #time.sleep(5)
      #camera.stop_recording()
      #camera.stop_preview()
      #path = '/home/pi/video%s.h264' % counter
      #part = MIMEBase("application", "octet-stream")
      #part.set_payload(open(path,'rb').read())
      #encoders.encode_base64(part)
      #part.add_header('Content-Disposition','attachment; filename = "%s"' %os.path.basename(path))
      #msg.attach(part)
      #google_server.sendmail(me, you , msg.as_string())
      #push = pb.push_note("[CAUTION!!]", "Motion Detected!")
      #time.sleep(5)
      #push = pb.push_link("Click here to check CCTV " ,"https://mail.google.com/mail/u/0/?ogbl#inbox")
      #counter = counter + 1

    except:
      camera.stop_preview()

  else:
    GPIO.output(LED, False)
    print "No motion"
  
  time.sleep(3)
      
google_server.close()