from aip import AipFace
from picamera import PiCamera
import urllib.request
import RPi.GPIO as GPIO
import base64
import time
import serial
import requests
#百度人脸识别API账号信息
APP_ID = '33048162'
API_KEY = '8it96tjfoaSqiqZWwKFB0B9f'
SECRET_KEY = 'WD8hnf1YTNRUOzx46RwkRh2Y5fTPhVt7'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)#创建一个客户端用以访问百度云
#图像编码方式
IMAGE_TYPE='BASE64'
camera = PiCamera()#定义一个摄像头对象
#用户组
GROUP = 'pi_01'

ser = serial.Serial("/dev/ttyAMA0", 9600)#打开串口
ser.flushInput()#清除串口缓冲区

GPIO.setmode(GPIO.BOARD)
# 设置GPIO模式为BOARD
PIN_KEY6 = 18
# 按键GPIO口
GPIO.setup(PIN_KEY6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# 设置GPIO口为输入模式

#照相函数
def getimage():
    camera.resolution = (1024, 768)#摄像界面为1024*768
    camera.start_preview()#开始摄像
    time.sleep(2)
    camera.capture('faceimage.jpg')#拍照并保存
    time.sleep(2)
    
#对图片的格式进行转换
def transimage():
    f = open('faceimage.jpg','rb')
    img = base64.b64encode(f.read())
    return img

#上传到百度api进行人脸检测
def go_api(image):
    result = client.search(str(image, 'utf-8'), IMAGE_TYPE, GROUP);#在百度云人脸库中寻找有没有匹配的人脸
    if result['error_msg'] == 'SUCCESS':#如果成功了
        name = result['result']['user_list'][0]['user_id']#获取名字
        score = result['result']['user_list'][0]['score']#获取相似度        
        if score > 80:#如果相似度大于80            
            if name == 'yuan_lingzhi':                
                print("%s同学已到!" % name)
                r = requests.put("http://111.229.208.133:9090/v1/todo/10", json={'status': True})
            if name == 'xu_jiayang':
                print("%s同学已到!" % name)
                r = requests.put("http://111.229.208.133:9090/v1/todo/11", json={'status': True})
        else:            
            print('对不起，我不认识你！')
            ser.write(str(2).encode())
            name = 'Unknow'            
            return -1
        curren_time = time.asctime(time.localtime(time.time()))#获取当前时间        
        #将人员出入的记录保存到Log.txt中
        f = open('Log.txt','a')
        f.write("Person: " + name + "     " + "Time:"+ str(curren_time)+'\n')
        f.close()
        return 1    
    if result['error_msg'] == 'pic not has face':
        print('检测不到人脸')
        #time.sleep(2)        
        return 0
    else:
        print(result['error_code'])        
        return 0

def print_menu():
    print('同学你好，这里是智能签到门禁系统')
    print('按键K5进行指纹识别')
    print('按键K6进行人脸识别')

#主函数
if __name__ == '__main__':
    cnt = 0
    print_menu()
    while True:
        size = ser.inWaiting()
        if size != 0:
            serial_data = ser.read(size)
            ser.flushInput() #清除缓冲区
            if serial_data == b'1': #开始指纹检测
                print('指纹识别准备开始，请在指纹模块上按压手指')
            elif serial_data == b'2': #指纹检测失败一次
                print('对不起，我不认识你！')
            elif serial_data == b'3': #连续三次未识别，发送消息提示，并结束识别
                print('我无法识别，请检查指纹')
                time.sleep(6)
                print_menu()
            elif serial_data == b'4':
                r = requests.put("http://111.229.208.133:9090/v1/todo/10", json={'status': True})
                print('yuan_lingzhi同学已到!')
                time.sleep(2)
                print("开门")
                time.sleep(6)
                print_menu()
            elif serial_data == b'5':
                r = requests.put("http://111.229.208.133:9090/v1/todo/11", json={'status': True})
                print('xu_jiayang同学已到!')
                time.sleep(2)
                print("开门")
                time.sleep(6)
                print_menu()
        if GPIO.input(PIN_KEY6) == 0:  #人脸识别按键按下
            while True:
                ser.write(str(1).encode())
                print('人脸识别准备开始，请面向摄像头')
                time.sleep(2)
                getimage()#拍照
                img = transimage()#转换照片格式
                res = go_api(img)#将转换了格式的图片上传到百度云
                if res == 1:#是人脸库中的人
                    print("开门")
                    ser.write(str(4).encode())
                    time.sleep(6)
                    ser.write(str(5).encode())
                    print_menu()
                    break
                elif res == -1:#是陌生人
                    cnt = cnt+1
                    if cnt == 3:
                        time.sleep(3)
                        ser.write(str(3).encode())
                        cnt = 0
                        print('我无法识别，请检查人脸')
                        time.sleep(5)
                        #连续三次未识别，发送消息提示，并结束识别
                        ser.write(str(5).encode())
                        print_menu()
                        break
                    time.sleep(1)
                    print('重新识别')
                time.sleep(5)