#coding:utf-8
from flask import Flask, render_template, Response
 
import RPi.GPIO as GPIO
import time
import atexit
import redis
r = redis.Redis(host='localhost',port=6379,db=0)
atexit.register(GPIO.cleanup)

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT, initial=False)
GPIO.setup(27, GPIO.OUT, initial=False)
p = GPIO.PWM(22,50) #50HZ
level = GPIO.PWM(27,50)
x = float(r.get('vertical'))
y = float(r.get('level'))
def go_fun():
    p.start(0)
    global x 
    x = x+0.1
    r.set('vertical',x)
    print x
    p.ChangeDutyCycle(x) #设置转动角度
def back_fun():
    p.start(0)
    global x
    if x > 2.5:
        x = x-0.1
        r.set('vertical',x)
    print x
    p.ChangeDutyCycle(x) #设置转动角度
def right_fun():
    level.start(0)
    global y 
    y = y+0.1
    r.set('level',y)
    print y
    level.ChangeDutyCycle(y) #设置转动角度
def left_fun():
    level.start(0)
    global y
    if y>2.5:
        y = y-0.1
        r.set('level',y)
    print y
    #time.sleep(2)
    level.ChangeDutyCycle(y) #设置转动角度
app = Flask(__name__)

 
@app.route('/')
@app.route('/<cmd>')
def index(cmd=None):
    """Video streaming home page."""
    if cmd == 'go':
        go_fun()
    elif cmd == 'stop':
        p.ChangeDutyCycle(0)
        level.ChangeDutyCycle(0)
    elif cmd == 'back':
        back_fun()
    elif cmd == 'right':
       	right_fun() 
    elif cmd == 'left':
       	left_fun() 
    elif cmd == 'rights':
        pass
    elif cmd == 'lefts':
        pass
    return render_template('cmd.html',cmd=cmd)
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True, threaded=True)
