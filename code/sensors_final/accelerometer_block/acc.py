#!/usr/bin/python

#	This is the base code needed to get usable angles from a BerryIMU
#	using a Complementary filter. The readings can be improved by
#	adding more filters, E.g Kalman, Low pass, median filter, etc..
#   See berryIMU.py for more advanced code.
#
#	For this code to work correctly, BerryIMU must be facing the
#	correct way up. This is when the Skull Logo on the PCB is facing down.
#
#   Both the BerryIMUv1 and BerryIMUv2 are supported
#
#	http://ozzmaker.com/


import time
import math
import IMU
import datetime
import os
import sys
import configparser

config_file = sys.argv[1]
config = configparser.ConfigParser()
config.read(config_file)

sleep_time = float(config['SETTINGS']['sleep_time'])

accx_log = config['PATHS']['accx_log']
accy_log = config['PATHS']['accy_log']
accz_log = config['PATHS']['accz_log']

gyrox_log = config['PATHS']['gyrox_log']
gyroz_log = config['PATHS']['gyroz_log']
gyroy_log = config['PATHS']['gyroy_log']



RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      # Complementary filter constant

################# Compass Calibration values ############
# Use calibrateBerryIMU.py to get calibration values
# Calibrating the compass isnt mandatory, however a calibrated
# compass will result in a more accurate heading values.

magXmin =  0
magYmin =  0
magZmin =  0
magXmax =  0
magYmax =  0
magZmax =  0


gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0



IMU.detectIMU()     #Detect if BerryIMUv1 or BerryIMUv2 is connected.
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass


a = datetime.datetime.now()




while True:
    try:
        #Read the accelerometer,gyroscope and magnetometer values
        ACCx = IMU.readACCx()
        ACCy = IMU.readACCy()
        ACCz = IMU.readACCz()
        GYRx = IMU.readGYRx()
        GYRy = IMU.readGYRy()
        GYRz = IMU.readGYRz()
        MAGx = IMU.readMAGx()
        MAGy = IMU.readMAGy()
        MAGz = IMU.readMAGz()
        '''


        #Apply compass calibration
        MAGx -= (magXmin + magXmax) /2
        MAGy -= (magYmin + magYmax) /2
        MAGz -= (magZmin + magZmax) /2

        ##Calculate loop Period(LP). How long between Gyro Reads
        b = datetime.datetime.now() - a
        a = datetime.datetime.now()
        LP = b.microseconds/(1000000*1.0)
        #print "Loop Time | %5.2f|" % ( LP ),


        #Convert Gyro raw to degrees per second
        rate_gyr_x =  GYRx * G_GAIN
        rate_gyr_y =  GYRy * G_GAIN
        rate_gyr_z =  GYRz * G_GAIN


        #Calculate the angles from the gyro.
        gyroXangle+=rate_gyr_x*LP
        gyroYangle+=rate_gyr_y*LP
        gyroZangle+=rate_gyr_z*LP


        #Convert Accelerometer values to degrees
        AccXangle =  (math.atan2(ACCy,ACCz)*RAD_TO_DEG)
        AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG

        #convert the values to -180 and +180
        if AccYangle > 90:
            AccYangle -= 270.0
        else:
            AccYangle += 90.0



        #Complementary filter used to combine the accelerometer and gyro values.
        CFangleX=AA*(CFangleX+rate_gyr_x*LP) +(1 - AA) * AccXangle
        CFangleY=AA*(CFangleY+rate_gyr_y*LP) +(1 - AA) * AccYangle



        #Calculate heading
        heading = 180 * math.atan2(MAGy,MAGx)/M_PI

        #Only have our heading between 0 and 360
        if heading < 0:
            heading += 360


        #Normalize accelerometer raw values.
        accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
        accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)


        #Calculate pitch and roll
        pitch = math.asin(accXnorm)
        roll = -math.asin(accYnorm/math.cos(pitch))






        #Calculate the new tilt compensated values
        magXcomp = MAGx*math.cos(pitch)+MAGz*math.sin(pitch)


        #The compass and accelerometer are orientated differently on the LSM9DS0 and LSM9DS1 and the Z axis on the compass
        #is also reversed. This needs to be taken into consideration when performing the calculations
        if(IMU.LSM9DS0):
            magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)-MAGz*math.sin(roll)*math.cos(pitch)   #LSM9DS0
        else:
            magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)+MAGz*math.sin(roll)*math.cos(pitch)   #LSM9DS1



        #Calculate tilt compensated heading
        tiltCompensatedHeading = 180 * math.atan2(magYcomp,magXcomp)/M_PI

        if tiltCompensatedHeading < 0:
            tiltCompensatedHeading += 360

        '''

        timestamp = round(time())

        file_dict = {
            'accx': [accx_log, ACCx],
            'accy': [accy_log, ACCy],
            'accz': [accz_log, ACCz],
            'gyrx': [gyrox_log, GYRx],
            'gyry': [gyroy_log, GYRy],
            'gyrz': [gyroz_log, GYRz],
        }

        for type in file_dict:
            open_file = open(file_dict[type][0], "a")
            open_file.write(('{} {}\n').format(unix_timestamp,file_dict[type][1]))
            open_file.close()

        '''
        if 1:			#Change to '0' to stop showing the angles from the accelerometer
            print ("# ACCX Angle %5.2f ACCY Angle %5.2f #  " % (AccXangle, AccYangle)),

        if 1:			#Change to '0' to stop  showing the angles from the gyro
            print ("\t# GRYX Angle %5.2f  GYRY Angle %5.2f  GYRZ Angle %5.2f # " % (gyroXangle,gyroYangle,gyroZangle)),

        if 1:			#Change to '0' to stop  showing the angles from the complementary filter
            print ("\t# CFangleX Angle %5.2f   CFangleY Angle %5.2f #" % (CFangleX,CFangleY)),

        if 1:			#Change to '0' to stop  showing the heading
            print ("\t# HEADING %5.2f  tiltCompensatedHeading %5.2f #" % (heading,tiltCompensatedHeading)),

        #print a new line
        print ""
        '''


        #slow program down a bit, makes the output more readable
        time.sleep(sleep_time)
    except Exception:
        time.sleep(0.1)
