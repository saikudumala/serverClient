# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 22:12:14 2020

@author: yaswa
"""
import socket
import pandas as pd
import json
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8192        # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 1024


def server_socket():
    data = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST,PORT))
        s.listen()
        while 1: # Accept connections from multiple clients
            print('Listening for client...')
            conn, addr = s.accept()
            print('Connection address:', addr)
            while 1: # Accept multiple messages from each client
                buffer = conn.recv(BUFFER_SIZE)
                buffer = buffer.decode()
                if buffer == ";":
                    conn.close()
                    print("Received all the data")
                    for x in data:
                        print(x)
                    break
                elif buffer:
                    print("received data: ", buffer)
                    json_Buffer = json.loads(buffer.replace(';',''))
                    #print(json_Buffer['rfw_id'])
                    rfw_id = json_Buffer['rfw_id'] #if key doesn't exist, returns None
                    benchmark_type = json_Buffer['benchmark_type']#if key doesn't exist, returns a 400, bad request error
                    workload_metric = json_Buffer['workload_metric']
                    batch_unit = json_Buffer['batch_unit'] #if key doesn't exist, returns None
                    batch_id = json_Buffer['batch_id'] #if key doesn't exist, returns a 400, bad request error
                    batch_size = json_Buffer['batch_size']
                   # c=len(data[workload_metric])
                    mul=abs(batch_id-batch_size)
                    last_batch_id=batch_id-1
                    #samples_requested=(mul+1)*batch_unit
                    dat=[]
                   
                    for i in range(0,(mul+1)):
                        data1=pd.read_csv("https://raw.githubusercontent.com/haniehalipour/Online-Machine-Learning-for-Cloud-Resource-Provisioning-of-Microservice-Backend-Systems/master/Workload%20Data/"+benchmark_type+".csv")
                        data2=pd.DataFrame(data1[workload_metric])
                        dam=data2.iloc[i*batch_unit:(i+1)*batch_unit]
                        print(dam)
                        dam=dam.to_json()
                        dat.append(dam)
                        i+=1
                        batch_id+=1
                        print("batch_id:",batch_id,)
                       # print("i:",i)
                    #dat=dat.to_json()
                    dat_json=json.dumps(dat)
                    reply = {
                            'rfw_id':rfw_id,
                    	   'batch_id':last_batch_id,
                            'sample_Data':dat
                        }
                    reply_json = json.dumps(reply)
                    conn.sendall(reply_json.encode())
                    #conn.sendall(dat_json.encode())
                    print(dat_json)
                    
                else:
                    break

server_socket()
