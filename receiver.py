# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 10:51:01 2018

@author: aviyonikstajyer
"""

import paho.mqtt.client as mqtt
import struct
import sys

broker_address="broker.hivemq.com"

client2=mqtt.Client(client_id="2022")  #Sender
client2.connect(broker_address)
def case3(message):
    print("Hello World")
    msgType=int.from_bytes(message[1],byteorder=sys.byteorder)
    print(msgType)
def case0(message):
    print("deneme 0")
def case1(message):
    print("deneme1")
def case2(message):
    print("deneme2")

def Switcher(message):
    msgType=int.from_bytes(message[1],byteorder=sys.byteorder)
    options={
            0:case0,
            1:case1,
            2:case2,
            3:case3
            }
    func=options.get(message,"nothing")    
    print(msgType)
    options[msgType](message)

def on_connect(client,userdata,flags,rc):
    client2.subscribe("okumaYazma")
    
def on_log(client,userdata,level,buf):
    print("log:",buf)
    
def on_message(client,userdata,message):
    print("message received",str(message.payload)) 
    takenData=list(message.payload)
    #print(takenData)
    valid_message=checkValidence(takenData)
    print(type(valid_message))
    client2.publish("okumaYazmaCheck",message.payload)
    Switcher(valid_message)
    
def on_publish(client,userdata,result):
    print("data published \n")
    pass

def SumElementsArray (array,min,max_len):
    Sums = 0    
    for item in range(min,max_len):
        Sums+=int.from_bytes(array[item],byteorder=sys.byteorder)
    return Sums
    
def checkValidence(takenData):
    hexArray=bytearray(takenData)
    index=0
    L=struct.unpack((">%dc"%(len(hexArray))),hexArray)    
    for index in range(0,len(L)-1):
        if L[index]==b'\x01':
            calc_length=int.from_bytes(L[index+2],byteorder=sys.byteorder)*256 +int.from_bytes(L[index+3],byteorder=sys.byteorder)
            print("calc_length is: ",calc_length)  
            if L[index+2+calc_length+1+1+1]==b'\x04':
                message=L[index:index+2+calc_length+1+1+1+1]#§tart at index then goes to the end of the message
                cs=int.from_bytes(L[4+calc_length],byteorder=sys.byteorder)#check sum
                sumElement=SumElementsArray(message,4,4+calc_length) #sum of datas
                msgType=int.from_bytes(message[1],byteorder=sys.byteorder) #if its message, message[1] should be msgType
                sumRHS=msgType+sumElement+calc_length #sumRHS is sum of msgType+length+data
                if cs==sumRHS:#checks whether its real message or not 
                    print("Its valid")
                    print("index is: ",index)
                    print(message)
                    print("CS is",cs)
                    print("MSG Type is",msgType)
                    print("SUMRHS is",sumRHS)
                    print("LENGTH is",calc_length)
                    print("sum of Elements in data",sumElement)
                    return message
#Subbacks
client2.on_connect=on_connect
client2.on_message=on_message
client2.on_log=on_log
client2.on_publish=on_publish
client2.loop_forever()
'''
    len_str=(takenData[2]*256)+takenData[3]
    print("Len Str is:",len_str)
    print(takenData[4:len_str])
    print(type(takenData))  
    sumData=SumElementsArray(takenData,4,4+len_str)
    print("SumData is ",sumData)       
    cs=takenData[4+len_str]     
    print("cs is: ",cs)
    print(type(takenData[4:len_str]))
    print("SumData is: ",sumData )    
    sumRHS=takenData[1]+len_str+sumData
    print("RHS is: ",sumRHS)
    if cs==sumRHS:
        print("Its valid")
    else:
        print("Its not valid")
#c=struct.unpack(("c c h %d c c " % len_str ),takenData)
'''
#parsed_message=struct.unpack((">c c h %dc c c c c h %dc c c" % (len_str,len_str) ),message.payload)
#c=struct.unpack((">c c h %dc c c c c h %dc c c." % (len_str,len_str) ),bytearray(message.payload))

 