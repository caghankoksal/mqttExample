# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 09:02:37 2018

@author: aviyonikstajyer
"""

import paho.mqtt.client as mqtt
import time
import struct
broker_address="broker.hivemq.com"

client1=mqtt.Client(client_id="2021")  #Sender
client1.connect(broker_address)


data=[0x01,0x03,0x00,0x02,0x02,0x04,0x10,0x04,0x01,0x03,0x00,0x02,0x02,0x04,0x10,0x04]  #Data to send

def checkTruthness(message):   
    print("message received",message.payload.decode("utf-8"))  #converts the message to utf-8 format
    takenData=list(message.payload)
    print(takenData)
    if takenData==data:
        print("Send Message is correct")
        return True
    else:
        return False


def on_log(client,userdata,level,buf):  #callback
    print("log:",buf)
def on_message(client, userdata,message): #Callback
    checkTruthness(message)
    print("message received",message.payload.decode("utf-8"))
    takenData=list(message.payload)
    print(takenData)
    if takenData==data:
        print("Send Message is correct")
    else:
        client1.publish("okumaYazma",bytearray(data))
        
       
def on_connect(client,userdata,flags,rc):
    #client1.subscribe("okumaYazma")
    client1.subscribe("okumaYazmaCheck") 
    data=[0x01,0x03,0x00,0x02,0x02,0x04,0x10,0x04,0x01,0x03,0x00,0x02,0x02,0x04,0x10,0x04]
    hexArray=bytearray(data)    #converts list to bytearray
    client1.publish("okumaYazma",hexArray) #publish message to the topic called okumaYazma
    len_str=(data[2]*256)+data[3]    

def on_subscribe(client,userdata,mid,granted_qos):
    print("Welcome,You subscribed")
    
def on_publish(client,userdata,result):
    print("data published \n")
    pass
    
#CallBacks
client1.on_subscribe=on_subscribe
client1.on_message=on_message
client1.on_log=on_log
client1.on_connect=on_connect
client1.on_publish=on_publish
    
client1.loop_forever()



client1.loop_stop()
