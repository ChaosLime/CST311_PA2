# UDPPingerClient.py

# Austin Ah Loo
# Micheal Reed
# Mitchell Saunders
# Nicholas Saunders

# declare modules
import time
import socket
import datetime
from socket import AF_INET, SOCK_DGRAM

# port and address of UDP IP ADDR
UDP_IP_ADDRESS = '127.0.0.1'
UDP_PORT_NO = 12000

# display message
print('Pinging', UDP_IP_ADDRESS, UDP_PORT_NO)
# create the socket
clientSocket = socket.socket(AF_INET, SOCK_DGRAM)
# set timeout for server reply (1 sec)
clientSocket.settimeout(1.0)
sequenceCount = 1
numberOfPings = 10
lostPackets = 0
min = 1.0
max = 0.0
mean = 0.0
estimatedRTT = 0.0
alpha = 0.125
devRTT = 0.0
beta = 0.25

message = 'This program is demonstrating ping'

# while loop to repeat process
while sequenceCount <= numberOfPings:
    start = time.time() # current time
    rTT = 0.0

    # client sends message var to server
    clientSocket.sendto(message.encode('utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))

    # try and except block to handle exceptions
    try:
        #print("Message Sent : " + str(message))
        modifiedMessage, address = clientSocket.recvfrom(1024)  # receives message from server
        
        # calculates RTT
        timeReceived = time.time()
        # print out time to client with readable time. See the following URL https://www.w3resource.com/python-exercises/date-time-exercise/python-date-time-exercise-6.php
        rTT = (timeReceived - start)
        timeSent = (timeReceived - rTT)

        print('This is Ping ' + str(sequenceCount) + " " + str(datetime.datetime.fromtimestamp(timeSent).strftime('%H:%M:%S.%f')))
        print('Time Received : ' + str(datetime.datetime.fromtimestamp(timeReceived).strftime('%H:%M:%S.%f')))
        print('RTT: ' + str(round(rTT, 6)) + ' s')
        # calc min, max, and mean
        if min > rTT:
            min = rTT
        if max < rTT:
            max = rTT
        mean = ((mean * (sequenceCount - 1)) + rTT) / sequenceCount
        
        # calc estimatedRTT and devRTT
        if sequenceCount > 1:
            estimatedRTT = ((1 - alpha) * estimatedRTT ) + (alpha * rTT)
        else:
            estimatedRTT = rTT
        
        if sequenceCount > 1:
            devRTT = ((1 - beta) * devRTT) + (beta * abs(rTT - estimatedRTT))

    # ping reply with timeout if no reply within one second
    except socket.timeout:
        print('This is Ping ' + str(sequenceCount) + " " + str(datetime.datetime.fromtimestamp(timeSent).strftime('%H:%M:%S.%f')))
        print('Request timed out')
        lostPackets += 1

    sequenceCount += 1    # increment sequenceCount by 1
    print('')

# end while

# print out original and modified message
print('Text sent to server: ' + str(message))
print('Text received from server: ' + str(modifiedMessage.decode()))

# print number of packets sent and recieved
print('Number of packets sent: ', numberOfPings)
print('Number of packets received: ', (numberOfPings - lostPackets))

# calculate loss rate and convert to string
loss_rate = str((lostPackets / numberOfPings) * 100)
print('Packet loss rate is: ' + loss_rate + '%')

# display Max RTT
print('Maximum Round Trip Time (RTT): ' + str(round(max, 4)) + ' ms')

# display Min RTT
print('Minimum Round Trip Time (RTT): ' + str(round(min, 4)) + ' ms')

# display average round trip time, estRTT, and devRTT
print('Average Round Trip Time: ' + str(round(mean, 4)) + ' s')
print('Estimated RTT: ' + str(round(estimatedRTT, 4)) + ' ms')
print('Deviation RTT: ' + str(round(devRTT, 4)) + ' ms')

# print out RTO
timeoutInterval = estimatedRTT + ((numberOfPings - lostPackets) * devRTT)
print('Timeout Interval : ' + str(round(timeoutInterval, 4)) + ' ms')

# close client socket after 10 packets
clientSocket.close()
