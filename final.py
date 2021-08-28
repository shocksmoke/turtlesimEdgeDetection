#!/usr/bin/env python
import rospy
from turtlesim.srv import *
from std_srvs.srv import Empty
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt
import cv2
import numpy as np



class Turtle:
    def __init__(self, i):
        self.name = 'turtle' + str(i)

    def __repr__(self):
        print("Turtle {}".format(self.name))

    def spawn(self, x, y, theta):
        """
        Function to spawn turtles in the Turtle-sim
        :param x: x-position with respect to origin at bottom-left
        :type x: float
        :param y: y-position with respect to origin at bottom-left
        :type y: float
        :param theta: orientation with respect to x-axis
        :type theta: float between [0 to 3] OR [0 to -3]
        """
        try:
            serv = rospy.ServiceProxy('/spawn', Spawn)
            serv(x, y, theta, self.name)
        except rospy.ServiceException as e:
            rospy.loginfo("Service execution failed: %s" + str(e))

    def set_pen(self, flag=True):
        """
        Function to sketch the turtle movements
        :param flag: To turn sketching pen - ON[True]/OFF[False]
        :type flag: bool
        """
        try:
            if not flag:
                set_serv = rospy.ServiceProxy('/' + self.name + '/set_pen', SetPen)
                set_serv(0, 0, 0, 0, 1)
            elif flag:
                set_serv = rospy.ServiceProxy('/' + self.name + '/set_pen', SetPen)
                set_serv(255, 255, 255, 2, 0)
        except rospy.ServiceException as e:
            rospy.loginfo("Service execution failed: %s" + str(e))

    def teleport(self, x, y, theta):
        """
        Function to teleport the turtle
        :param x: x-position with respect to origin at bottom-left
        :type x: float
        :param y: y-position with respect to origin at bottom-left
        :type y: float
        :param theta: orientation with respect to x-axis
        :type theta: float between [0 to 3] OR [0 to -3]
        """
        try:
            serv = rospy.ServiceProxy('/' + self.name + '/teleport_absolute', TeleportAbsolute)
            serv(x, y, theta)
        except rospy.ServiceException as e:
            rospy.loginfo("Service execution failed: %s" + str(e))

    def kill_turtle(self):
        """
        Function to remove the turtle from Turtle-sim
        """
        try:
            serv = rospy.ServiceProxy('/kill', Kill)
            serv(self.name)
        except rospy.ServiceException as e:
            rospy.loginfo("Service execution failed: %s" + str(e))


# read the image
image = cv2.imread("opencv.png")
image = cv2.resize(image,(500,500))
# convert to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)



# create a binary thresholded image
_, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY_INV)
# show it
#plt.imshow(binary, cmap="gray")
#plt.show()
# find the contours from the thresholded image
#binary= cv2.Canny(image,150,200)
image,contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# draw all contours

if __name__ == '__main__':
    try:
        t1=Turtle(1)
        for i in contours:
            a=0
            for j in i:
               
                if (a == 0):
                    for z in j:
                    
                        x=z[0]*11/500
                        y=(500-z[1])*11/500
                        t1.set_pen(False)  
                        t1.teleport(x,y,0)
                        t1.set_pen(True)   
                else :
                    for z in j:
                        x=float(z[0]*11)/500
                        y=float((500-z[1])*11)/500
                        print(x)
                        print(y)
                        t1.teleport(x,y,0)
                a=a+1
        t1.kill_turtle()
        
    except KeyboardInterrupt:
        exit()
