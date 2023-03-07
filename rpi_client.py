''' 
This program streams a live analytics feed from a raspberry pi to a local machine 

Input Paramters: 

Parameter 1: IP address/ Host name from computer you wish to act as a server 

Parameter 2: To add a new face to the Faceial Recoginiton Database attach the following parameter "A" or "a: 

The live Raspberry Pi video stream is processed through a facial recoginiton pipline,

the resulting video stream is annotated with the persons name, that meta data is then packed into

a socket where it is passed through a via TCP to port 555 on the local network 

'''


import cv2
import sys
import zmq  
import time
import socket
import imagezmq
import traceback
from time import sleep
from imutils.video import VideoStream
from face_rec_simple import simple_face_rec
import numpy as np 




'''
    class to establish the TCP socket from the RPI
    @param sender
    @param reciever 
'''
class rpi_video_stream:
    def __init__ (self, tcp_port, recognizer): 
        self.connect_to = tcp_port
        self.rpiName = 0
        self.rpiCam = 0
        self.sender = 0 
        self.refreshTime = 5  # number of seconds to sleep between sender restarts
        self.self.jpegQuality = 95  # cv2 default quality
        self.recognizer = recognizer
    '''
        Initalize tcp port router 
    '''
    def init_sender(self, connect_to=None):
        #connect_to = 'tcp://192.168.0.11:5555'
        sender = imagezmq.ImageSender(connect_to=self.connect_to)
        sender.zmq_socket.setsockopt(zmq.LINGER, 0)  # prevents ZMQ hang on exit
        sender.zmq_socket.setsockopt(zmq.RCVTIMEO, 2000)  # set a receive timeout
        sender.zmq_socket.setsockopt(zmq.SNDTIMEO, 2000)  # set a send timeout
        return sender
    
    '''
        initalize rpi camera 
    '''
    def init_pi_camera(self):
        self.sender = self.sender_start()
        self.rpiName = socket.gethostname()  # send RPi hostname with each image
        self.rpiCam = VideoStream(usePiCamera=True).start()
        time.sleep(3.0)  # allow camera sensor to warm up

    '''
        Stream the video over the Raspberry pi 
    '''
    def stream_video(self): 
        img = 0 
        imgMetaData = 0
        try:
            while True: 

                img = self.rpiCam.read() # read image from RPI camear 

                imgMetaData = self.recognizer.run_facial_recognition(img)  #run facial recognition on new image 
            
                if (np.shape(imgMetaData) == ()): 
                    imgMetaData = img

                ret_code, jpg_buffer = cv2.imencode(
                    ".jpg", imgMetaData, [int(cv2.IMWRITE_JPEG_QUALITY), self.jpegQuality])
                try:
                    reply_from_mac = self.sender.send_jpg(self.rpiName, jpg_buffer)

                except (zmq.ZMQError, zmq.ContextTerminated, zmq.Again):

                    if 'sender' in locals():

                        print('Closing ImageSender.')

                        self.sender.close()

                    sleep(self.refreshTime)

                    print('Restarting ImageSender.')

                    self.sender = self.sender_start()

        except (KeyboardInterrupt, SystemExit):

            pass  # Ctrl-C was pressed to end program
        except Exception as ex:
        
            print('Python error with no Exception handler:')
        
            print('Traceback error:', ex)
        
            traceback.print_exc()

        finally:
            if 'sender' in locals():
            
                self.sender.close()
        
            self.rpiCam.stop()  # stop the camera thread
            sys.exit()



#main stack thread 
if __name__ == '__main__': 

    tcpVideoStream = 0 
    #instantiate new face recognizer 
    face_regonizer = simple_face_rec() 
    
    #retrieve known faces from database 
    face_regonizer.retrieve_faces_from_database()

    #find encodings for dataset 

    face_regonizer.find_encodings()

    print('Encoding Complete')

    try: 

        
        #get TCP port from user 
        if sys.argv[1] == None: 
            print("You must run the script with an input IP adress or hostname to server")
            
        if sys.argv[2].upper() == "A": 
            face_regonizer.new_face_label() 

        tcp_port = f'tcp://{sys.argv[1]}:5555'
        
        #instantiate new rpi video sender 
        tcpVideoStream = rpi_video_stream(tcp_port, face_regonizer)
        
        #initalize sender 
        tcpVideoStream.init_sender()
        #initalize rpi camera 
        tcpVideoStream.init_pi_camera()
        #start streaming 
        tcpVideoStream.stream_video()


    except Exception as e:
        print(e) 
        os._exit(0)
        pass