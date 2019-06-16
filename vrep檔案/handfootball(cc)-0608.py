import vrep
import sys, math
import keyboard
from math import sqrt
# child threaded script: 
# 內建使用 port 19997 若要加入其他 port, 在  serve 端程式納入
#simExtRemoteApiStart(19999)
  
vrep.simxFinish(-1)
  
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
KickBallV = 720
up_KickBallVel = (math.pi/180)*KickBallV
d_KickBallVel = -(math.pi/180)*KickBallV
if clientID!= -1:
    print("Connected to remote server")
else:
    print('Connection not successful')
    sys.exit('Could not connect')

errorCode,Sphere_handle=vrep.simxGetObjectHandle(clientID,'Sphere',vrep.simx_opmode_oneshot_wait)
errorCode,lmov_handle=vrep.simxGetObjectHandle(clientID,'lmov', vrep.simx_opmode_oneshot_wait)
errorCode,rmov_handle=vrep.simxGetObjectHandle(clientID,'rmov',vrep.simx_opmode_oneshot_wait)
errorCode,lrev_handle=vrep.simxGetObjectHandle(clientID,'lrev',vrep.simx_opmode_oneshot_wait)
errorCode,rrev_handle=vrep.simxGetObjectHandle(clientID,'rrev',vrep.simx_opmode_oneshot_wait)
errorCode,R_handle=vrep.simxGetObjectHandle(clientID,'R',vrep.simx_opmode_oneshot_wait)
errorCode,L_handle=vrep.simxGetObjectHandle(clientID,'L',vrep.simx_opmode_oneshot_wait)


vrep.simxSetJointTargetVelocity(clientID,lmov_handle,0,vrep.simx_opmode_oneshot_wait)
vrep.simxSetJointTargetVelocity(clientID,rmov_handle,0,vrep.simx_opmode_oneshot_wait)
vrep.simxSetJointTargetVelocity(clientID,lrev_handle,0,vrep.simx_opmode_oneshot_wait)
vrep.simxSetJointTargetVelocity(clientID,rrev_handle,0,vrep.simx_opmode_oneshot_wait)
def speed(handle,speed):
    errorCode = vrep.simxSetJointTargetVelocity(clientID,handle,speed,vrep.simx_opmode_oneshot_wait)
vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot_wait)
#vrep.simxSetJointTargetVelocity(clientID,P1_handle,5,vrep.simx_opmode_oneshot_wait)
while True:
        errorCode,position_LB=vrep.simxGetObjectPosition(clientID,lrev_handle,-1,vrep.simx_opmode_oneshot)
        errorCode,position_S=vrep.simxGetObjectPosition(clientID,Sphere_handle,-1,vrep.simx_opmode_oneshot)
        errorCode,position_RB=vrep.simxGetObjectPosition(clientID,rrev_handle,-1,vrep.simx_opmode_oneshot)
        BB =position_S[1] - position_LB[1] #左右
        BBB =position_S[0] - position_LB[0]#前後
        AA =position_S[1] - position_RB[1] #左右
        AAA =position_S[0] - position_RB[0]#前後
        #print(position_S)
        #print(AAA)
        if AAA>0:
            AAA=-AAA
        if BBB<0:
            BBB=-BBB
        
        #print((sqrt(AA**2+AAA**2)+AAA))
        if sqrt(AA**2+AAA**2) and sqrt(BB**2+BBB**2):
            dist_b2PR=5*(sqrt(AA**2+AAA**2)+AAA)+0.8*sqrt(AA**2+AAA**2)+2*((sqrt(AA**2+AAA**2)+AAA)/sqrt(AA**2+AAA**2))+2.5
            dist_b2PL=5*(sqrt(BB**2+BBB**2)-BBB)+0.8*sqrt(BB**2+BBB**2)+2*((sqrt(BB**2+BBB**2)-BBB)/sqrt(BB**2+BBB**2))+2.5
        else:
            dist_b2PR=0
            dist_b2PL=0
            
        if BBB <0.07:
            speed(lrev_handle, d_KickBallVel)
            #speed(lrev_handle, up_KickBallVel)
            #print('b down')
        elif BBB > 0.04:
            speed(lrev_handle, up_KickBallVel)
            #print('b up')
            
        if AAA >-0.07:
            speed(rrev_handle, up_KickBallVel)
            #speed(rrev_handle, d_KickBallVel)
            #print( 'a up')
        elif AAA < -0.04:
            speed(rrev_handle, d_KickBallVel)
            #print('a down')
        else:
            pass
        Mv = BB*dist_b2PL
        vrep.simxSetJointTargetVelocity(clientID,lmov_handle,Mv,vrep.simx_opmode_oneshot_wait)
        Mvv = AA*dist_b2PR
        vrep.simxSetJointTargetVelocity(clientID,rmov_handle,Mvv,vrep.simx_opmode_oneshot_wait)