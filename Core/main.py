import time
import sys
import struct
import threading
import win32pipe, win32com, win32file

#Thread polls the named pipe for available input, printing it out if found
def ListenThread(pipe):

    #Set the pipe to nonblocking
    win32pipe.SetNamedPipeHandleState(pipe, win32pipe.PIPE_NOWAIT, None, None)
    
    #Main Thread Loop
    while True:
        try:
            #Peek the pipe to get availableBytes
            (_, nAvail, _) = win32pipe.PeekNamedPipe(pipe, 0)

            #If no bytes available check again
            if nAvail < 1:
                continue

            #Read bytes from namedPipe
            (retVal, recieveMsg) = win32file.ReadFile(pipe, 1024, None)
            
            #Decode string and print it
            print(recieveMsg.decode('ascii'))
        
        except Exception as e:
            print(e)
            break

    print("Listen Thread Exited")

#Create a new named pipe with name 'Dashboard_Pipe'
#PIPE_ACCESS_DUPEX = allows for sending and receiving data, 
#PIPE_READMODE_MESSAGE = send blocks of data, not bytes, 
#PIPE_WAIT - calls to read / write from pipe are blocking
pipe = win32pipe.CreateNamedPipe(r'\\.\pipe\Dashboard_Pipe',
                                win32pipe.PIPE_ACCESS_DUPLEX, 
                                win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT, 
                                1, 65536, 65536, 
                                0, 
                                None)

print("Waiting for connection")
win32pipe.ConnectNamedPipe(pipe, None)
print("Connection Established")

#Init listener thread
ListenThread = threading.Thread(target=ListenThread, args=(pipe,))
ListenThread.start()

while True:
    print("Enter the message you want to send: ", end='')
    message = sys.stdin.readline()
    
    #Send message across the pipe to the wpf application
    win32file.WriteFile(pipe, message.encode())