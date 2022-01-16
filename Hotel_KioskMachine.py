#import library
import RPi.GPIO as GPIO
#import pandas as pd
from gpiozero import Servo
from mfrc522 import SimpleMFRC522
import time
import csv

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#Define Keypad
# Row
ROW1 = 5
ROW2 = 6
ROW3 = 13
ROW4 = 19
ROW5 = 26
# Column
COL1 = 21
COL2 = 20
COL3 = 16
COL4 = 12
#
ROW_Pin = [ROW1,ROW2,ROW3,ROW4,ROW5]
#
COL_Pin = [COL1,COL2,COL3,COL4]
# 
KEY_map =  [["F1","F2","#" ,"*"  ],
            ["1" ,"2" ,"3" ,"↑"  ],
            ["4" ,"5" ,"6" ,"↓"  ],
            ["7" ,"8" ,"9" ,"ESC"],
            ["←" ,"0" ,"→" ,"Ent"]]

# ---------------------Init function-----------------------#
def Servo_init():
    servo = Servo(22)
    servo.min()
def Keypad_Init():
    GPIO.setup(ROW1, GPIO.OUT)
    GPIO.setup(ROW2, GPIO.OUT)
    GPIO.setup(ROW3, GPIO.OUT)
    GPIO.setup(ROW4, GPIO.OUT)
    GPIO.setup(ROW5, GPIO.OUT)
    GPIO.setup(COL1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(COL2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(COL3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(COL4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 
# ------------------Display function-----------------------#
def Display_Login():
    print("")
    print("--------------------------------------------------------------")
    print("*****************************")
    print("****KIOSK SELF SERVICE*******")
    print("************Login************")
    print("Enter the password")
def Display_Service():
    print("")
    print("--------------------------------------------------------------")
    print("*****************************")
    print("****KIOSK SELF SERVICE*******")
    print("***********Service***********")
    print(" ")
    print("1.Room Service")
    print("2.Outside Service")
    print("*.Logout")
def Display_RoomService():
    print("")
    print("--------------------------------------------------------------")
    print("*****************************")
    print("****KIOSK SELF SERVICE*******")
    print("***********Service***********")
    print("********Room Service*********")
    print(" ")
    print("1.Checkin")
    print("2.Checkout")
    print("3.Room Renewal")
    print("4.Incident Notify")
    print("5.Back")
    print("*.Logout")
def Display_Checkin():
    print("")
    print("--------------------------------------------------------------")
    print("*****************************")
    print("****KIOSK SELF SERVICE*******")
    print("***********Service***********")
    print("********Room Service*********")
    print("**********Checkin************")
    print(" ")
def Display_Checkout():
    print("")
    print("--------------------------------------------------------------")
    print("*****************************")
    print("****KIOSK SELF SERVICE*******")
    print("***********Service***********")
    print("********Room Service*********")
    print("**********Checkout************")
    print(" ")

def Display_RoomRenewal():
    print("")
    print("--------------------------------------------------------------")
    print("*****************************")
    print("****KIOSK SELF SERVICE*******")
    print("***********Service***********")
    print("********Room Service*********")
    print("********Room Renewal*********")
    print(" ")
    print("Choose a room renewal package")
    print("    Package            Cost ")
    print("1.    1 Day             15$  ")
    print("2.    5 Day             70$  ")
    print("3.   10 Day             130$ ")
    print("4.   15 Day             195$ ")
    print(" ")
    print("5.Back")
    print("*.Logout")
    print("Note: If you want to renewal more than 15 days, please register on the website HotelHUST.com")
def Display_Payment(cost):
    print("")
    print("--------------------------------------------------------------")
    print(" ")
    print("The amount to be paid is",cost)
    print("Please pass your credit card through the card reader")
    print(" ")
def Display_Hotline(Hotline):
    print("")
    print("--------------------------------------------------------------")
    print("*****************************")
    print("****KIOSK SELF SERVICE*******")
    print("***********Service***********")
    print("********Room Service*********")
    print("*******Incident Notify*******")
    print("Electrical Troubleshooting(Hotline):",Hotline[0])
    print("Fix water system problems(Hotline):",Hotline[1])
    print(" ")
    print("1.Back")
    print("*.Logout")
def Display_Goodbyte():
    print("")
    print("--------------------------------------------------------------")
    print(" ")
    print("****Thank you for using the service. See you again!*******")
    print(" ")
def Display_OutsideService():
    print("")
    print("--------------------------------------------------------------")
    print("*****************************")
    print("****KIOSK SELF SERVICE*******")
    print("***********Service***********")
    print("******Outside Service********")
    print(" ")
    print("1.Laundry and Cleaing")
    print("2.Food and Drink")
    print("3.Parcals and Mail")
    print("4.Back")
    print("*.Logout")

# --------------------FSM function--------------------------#

#***********Login FSM*************#

def Get_password():
    Key_Login = ""
    Key_count = 0
    while(Key_count < 6 ):
        if(readKeypad()!=None):
            Key_Login += readKeypad()
            print(readKeypad(), end="")
            Key_count = Key_count + 1
            time.sleep(0.2)
            if(Key_count == 6):
                return Key_Login

def check_Login(Login_key):
    with open("LoginDatabase.csv", "r") as f:
        file = csv.DictReader(f)
        Keyword = []
        for col in file:
            Keyword.append(col['Keyword'])
        if Login_key in Keyword:
            print(" ")
            print("Logged in successfully")
            return True
        else:
            print(" ")
            print("Invalid password. Please re-enter your password!")
            time.sleep(1)
            return False

def Identification(Key_login):
    with open("LoginDatabase.csv", "r") as f:
        file = csv.DictReader(f)
        ID  = []
        User= []
        Keyword = []
        Start = []
        Close= []
        for col in file:
            ID.append(col['ID'])
            User.append(col['User'])
            Keyword.append(col['Keyword'])
            Start.append(col['Start'])
            Close.append(col['Close'])
    index = Keyword.index(Key_login)
    print("")
    print("--------------------------------------------------------------")
    print("ID : ",ID[index])
    print("Welcome",User[index])
    print("Start Time: ",Start[index])
    print("Close Time:",Close[index])
    time.sleep(3)



#**********Service FSM************#

def Service_Idle():
    Display_Service()
    Key_count = 0
    while(Key_count < 1):
        if(readKeypad()=="1"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "1"
        elif(readKeypad()=="2"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "2"
        elif(readKeypad()== "*"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "*"

# Room Service Function
def ServiceRoom_Idle():
    Display_RoomService()
    Key_count = 0
    while(Key_count < 1):
        if(readKeypad()=="1"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "1"
        elif(readKeypad()=="2"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "2"
        elif(readKeypad()=="3"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "3"
        elif(readKeypad()=="4"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "4"
        elif(readKeypad()=="5"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "5"
        elif(readKeypad()== "*"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "*"

def Checkin():
    Display_Checkin()
    print("Waiting......")
    time.sleep(0.5)
    servo = Servo(22)
    servo.min()
    time.sleep(0.5)
    servo.mid()
    time.sleep(0.5)
    servo.max()
    time.sleep(0.5)
    servo.min()
    time.sleep(0.5)
    servo.mid()
    time.sleep(0.5)
    servo.max()
    time.sleep(0.5)
    print("Provide Key Done!")
    time.sleep(2)

def Checkout():
    Display_Checkout()
    print("Please insert the key into the slot!")
    time.sleep(2)
    print("Waiting......")
    servo = Servo(22)
    servo.max()
    time.sleep(0.5)
    servo.mid()
    time.sleep(0.5)
    servo.min()
    time.sleep(0.5)
    servo.max()
    time.sleep(0.5)
    servo.mid()
    time.sleep(0.5)
    servo.min()
    time.sleep(0.5)
    print("Done!")
    time.sleep(0.5)
    Display_Goodbyte()
    time.sleep(2)
    
def RoomRenewal():
    Display_RoomRenewal()
    Key_count = 0
    while(Key_count < 1):
        if(readKeypad()=="1"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "1"
        elif(readKeypad()=="2"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "2"
        elif(readKeypad()=="3"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "3"
        elif(readKeypad()=="4"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "4"
        elif(readKeypad()=="5"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "5"
        elif(readKeypad()== "*"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "*"
def Payment(cost):
    Display_Payment(cost)
    rfid = SimpleMFRC522()
    id, text = rfid.read()
    if(int(text)>=cost):
        return True
    else:
        return False
    
def Update_InformationRenewal(Package_Renewal,Payment_Valid):
    if(Payment_Valid):
        print("Completed payment!")
        time.sleep(2)
        print("")
    else:
        print("The payment failed because the card ran out of money. Please try again!")
        time.sleep(2)
        print("")
def IncidentNotify():
    with open("HotlineNumber.csv", "r") as f:
        file = csv.DictReader(f)
        Hotline = []
        for col in file:
            Hotline.append(col['Hotline'])
    Display_Hotline(Hotline)
            
# Outside Service Function
def ServiceOutside_Idle():
    Display_OutsideService()
    Key_count = 0
    while(Key_count < 1):
        if(readKeypad()=="1"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "1"
        elif(readKeypad()=="2"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "2"
        elif(readKeypad()=="3"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "3"
        elif(readKeypad()=="4"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "4"
        elif(readKeypad()== "*"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "*"


def Laundry_Cleaing():
    pass

def Food_Drink():
    pass

def Parcals_Mail():
    pass



# --------------------function--------------------------#
#             

def readKeypad():
    for i in range(len(ROW_Pin)):
        GPIO.output(ROW_Pin[i], GPIO.HIGH)
        for j in range(len(COL_Pin)):
            if(GPIO.input(COL_Pin[j]) == 1):
                GPIO.output(ROW_Pin[i], GPIO.LOW)
                return KEY_map[i][j]
        GPIO.output(ROW_Pin[i], GPIO.LOW)
        
#---------------------------------------------------------

FSM_State = 'Login'
#
Login_State = 'EnterPIN'
#
Service_State = 'Idle'

RoomService_State = 'Idle'

OutsideService_State = 'Idle'




#---------------------------------------------------------
if __name__ == '__main__':
    Servo_init()
    Keypad_Init()
    while True:
        if(FSM_State == 'Login'):
            Key_Login = ""
            if(Login_State ==  'EnterPIN'):
                Display_Login()
                Key_Login = Get_password()
                Login_State = 'CheckPIN'
            if(Login_State ==  'CheckPIN'):
                Valid_key = check_Login(Key_Login)
                if(Valid_key == True):
                    Login_State =  'Identification'
                elif(Valid_key == False):
                    Login_State =  'EnterPIN'
            if(Login_State ==  'Identification'):
                Identification(Key_Login)
                FSM_State = "Service"
                Login_State =  'EnterPIN'
        if(FSM_State == 'Service'):
            if(Service_State == 'Idle'):
                Selection_Service = Service_Idle()
                if(Selection_Service == "1"):
                    Service_State = 'RoomService'
                if(Selection_Service == "2"):
                    Service_State = 'OutsideService'
                if(Selection_Service == "*"):
                    time.sleep(1)
                    FSM_State = 'Login'
            if(Service_State == 'RoomService'):
                if(RoomService_State == 'Idle'):
                    Selection_ServiceRoom = ServiceRoom_Idle()
                    if(Selection_ServiceRoom =="1"):
                        RoomService_State = 'Checkin'
                    elif(Selection_ServiceRoom =="2"):
                        RoomService_State = 'Checkout'
                    elif(Selection_ServiceRoom =="3"):
                        RoomService_State = 'RoomRenewal'
                    elif(Selection_ServiceRoom =="4"):
                        RoomService_State = 'IncidentNotify'
                    elif(Selection_ServiceRoom =="5"):
                        Service_State = 'Idle'
                    elif(Selection_ServiceRoom == "*"):
                        Service_State = 'Idle'
                        FSM_State = 'Login'
                if(RoomService_State == 'Checkin'):
                    Checkin()
                    RoomService_State = 'Idle'
                if(RoomService_State == 'Checkout'):
                    Checkout()
                    RoomService_State = 'Idle'
                    Service_State = 'Idle'
                    FSM_State = 'Login'
                if(RoomService_State == 'RoomRenewal'):
                    cost = 0
                    Selection_RoomRenewal = RoomRenewal()
                    if(Selection_RoomRenewal=="1"):
                        cost = 15
                        Payment_Valid = Payment(cost)
                        Update_InformationRenewal(Selection_RoomRenewal,Payment_Valid)
                        RoomService_State = 'Idle'
                    elif(Selection_RoomRenewal=="2"):
                        cost = 70
                        Payment_Valid = Payment(cost)
                        Update_InformationRenewal(Selection_RoomRenewal,Payment_Valid)
                        RoomService_State = 'Idle'
                    elif(Selection_RoomRenewal=="3"):
                        cost = 130
                        Payment_Valid = Payment(cost)
                        Update_InformationRenewal(Selection_RoomRenewal,Payment_Valid)
                        RoomService_State = 'Idle'
                    elif(Selection_RoomRenewal=="4"):
                        cost = 195
                        Payment_Valid = Payment(cost)
                        Update_InformationRenewal(Selection_RoomRenewal,Payment_Valid)
                        RoomService_State = 'Idle'
                    elif(Selection_RoomRenewal=="5"):
                        RoomService_State = 'Idle'
                    elif(Selection_RoomRenewal=="*"):
                        RoomService_State = 'Idle'
                        Service_State = 'Idle'
                        FSM_State = 'Login'
                if(RoomService_State == 'IncidentNotify'):
                    IncidentNotify()
                    Key_count = 0
                    while(Key_count < 1):
                        if(readKeypad()=="1"):
                            Key_count = Key_count + 1
                            time.sleep(0.2)
                            RoomService_State = 'Idle'
                        elif(readKeypad()=="*"):
                            Key_count = Key_count + 1
                            time.sleep(0.2)
                            RoomService_State = 'Idle'
                            Service_State = 'Idle'
                            FSM_State = 'Login'
            if(Service_State == 'OutsideService'):
                if(OutsideService_State == 'Idle'):
                    Selection_ServiceOutside = ServiceOutside_Idle()
                    if(Selection_ServiceOutside =="1"):
                        OutsideService_State = 'Laundry_Cleaing'
                    elif(Selection_ServiceOutside =="2"):
                        OutsideService_State = 'Food_Drink'
                    elif(Selection_ServiceOutside =="3"):
                        OutsideService_State = 'Parcals_Mail'
                    elif(Selection_ServiceOutside =="4"):
                        Service_State = 'Idle'
                    elif(Selection_ServiceOutside == "*"):
                        Service_State = 'Idle'
                        FSM_State = 'Login'
                if(OutsideService_State == 'Laundry_Cleaing'):
                    Laundry_Cleaing()
                if(OutsideService_State == 'Food_Drink'):
                    Food_Drink()
                if(OutsideService_State == 'Parcals_Mail'):
                    Parcals_Mail()    
            