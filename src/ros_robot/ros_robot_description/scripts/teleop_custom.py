#!/usr/bin/env python
import rospy
import getch
from geometry_msgs.msg import Twist
msg = """
WELCOME TO KUROBUTA CONTROL PANEL!!
---------------------------
Moving around:
   q    w    e
   a    s    d
   z    x    c
i/o : increase/decrease max speeds by 20%
k/l : increase/decrease only linear speed by 20%
,/. : increase/decrease only angular speed by 20%
s : force stop
Press 'f' button to quit
"""
class kurobuta_teleop():
    def __init__(self):
        self.moveKey = {
            'w':(1,0),
            'e':(1,-1),
            'a':(0,1),
            'd':(0,-1),
            'q':(1,1),
            'x':(-1,0),
            'c':(-1,1),
            'z':(-1,-1),
        }
        self.adjustSpeed = {
            'i':(1.2,1.2),
            'o':(.8,.8),
            'k':(1.2,1),
            'l':(.8,1),
            ',':(1,2.1),
            '.':(1,.8),
        }

        self.control_speed = 0.5
        self.control_turn = 1.0 
        self.control_vlx = 0.0
        self.control_wz = 0.0
        self.key_input = ""
        self.vl_x = 0.0
        self.w_z = 0.0
        self.target_speed = 0.0
        self.target_turn = 0.0
        rospy.init_node('Kurobuta_Teleop')
        
        self.freq = rospy.Rate(1000) 
        self.publish_msg = rospy.Publisher("/cmd_vel", Twist, queue_size=1)

    def vels(self,speed,turn,choice):
        if choice == 1 :
            return "currently:\tspeed %s\tturn %s " % (speed,turn)
        elif choice == 2 : 
            return "Target:\tspeed %s\tturn %s " % (speed,turn)

    def main(self):
        print(msg)
        print(self.vels(self.vl_x,self.w_z,1))
        while not rospy.is_shutdown():
            self.key_input = getch.getch()
            if (self.key_input in self.moveKey):
                self.control_vlx = self.moveKey[self.key_input][0]
                self.control_wz = self.moveKey[self.key_input][1]
            elif (self.key_input in self.adjustSpeed):
                self.control_speed = self.control_speed * self.adjustSpeed[self.key_input][0]
                self.control_turn = self.control_turn * self.adjustSpeed[self.key_input][1]
            elif (self.key_input == 's'):
                self.control_vlx = 0 
                self.control_wz  = 0
                self.vl_x = 0
                self.w_z = 0
            elif(self.key_input == 'f'):
                break


            self.target_speed = self.control_speed * self.control_vlx 
            self.target_turn = self.control_turn * self.control_wz

            if self.target_speed > self.vl_x:
                self.vl_x = min( self.target_speed, self.vl_x + 0.05 )
            elif self.target_speed < self.vl_x:
                self.vl_x = max( self.target_speed, self.vl_x - 0.05 )
            else:
                self.vl_x = self.target_speed

            if self.target_turn > self.w_z:
                self.w_z = min( self.target_turn, self.w_z + 0.2 )
            elif self.target_turn < self.w_z:
                self.w_z = max( self.target_turn, self.w_z - 0.2 )
            else:
                self.w_z = self.target_turn


            self.twist_msg = Twist()
            self.twist_msg.linear.x = self.vl_x; self.twist_msg.linear.y = 0; self.twist_msg.linear.z = 0
            self.twist_msg.angular.x = 0; self.twist_msg.angular.y = 0; self.twist_msg.angular.z = self.w_z 
            self.publish_msg.publish(self.twist_msg)
            print(self.vels(self.target_speed,self.target_turn,2))
            self.freq.sleep()


kurobuta_teleop().main()
        
        
        



