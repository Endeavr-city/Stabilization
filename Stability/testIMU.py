import time 
import board 
import adafruit_mpu6050
from datetime import datetime as dt
import busio
#import numpy as np
#import cv2 and numpy for processing
import numpy as np
import cv2

#Create a low-pass filter function, that will utilize an alpha value, and adjust the specific acceleration coordinate as needed
#The higher the alpha value, the more filtering will be required for this to be done, to get the smoother signal. 
#If alpha value is too high, then that will make the application slow to respond to specific changes, so alpha will need to be switched via trial and error
alpha = 0.10 # to start with apply a value of 0.60
def low_pass_filter(prev_val, new_val): 
    return alpha * prev_val + (1 - alpha) * new_val
#apply the previous_values for all three acceleration coordinates
#initialize all three to be 0 at first
filter_x = 0
filter_y = 0
filter_z = 0

#i2C = board.I2C()
i2c = busio.I2C(board.SCL, board.SDA) #uses board.SCL and board.SDA as format (SCL, SDA), here we will need to specify the pins for the specific SCL and SDA ports for both IMU chips
#above pin is the I2C layout for the first pin, not specified as SCL_0, but rather SCL_

# if wishing to retrieve data from a second MPU chip, declare the below i2C variable
#i2c_2 = busio.I2C(board.SCL_1, board.SDA_1) #use board SCL_1, SDA_1 for the second pin to process data

# apply the mpu conversion to the i2C object for one chip
mpu = adafruit_mpu6050.MPU6050(i2c) #setting up the mpu for the 1st chip
#mpu_2 = adafruit_mpu6050.MPU6050(i2c_2) #setting up the mpu for the 2nd chip

# open a new file to write for one-chip
chip1_out = open("/home/orin/Desktop/RetroPilotFiles/demoTesting/Test3.csv", "a")
# if wishing to use a second MPU chip, then open a new file
#chip2_out = open("/home/orin/Desktop/RetroPilotFiles/RawIMU_data/chip2_run0.csv", "a")

# while true, receive data points individually from each of the chips
while True: 
    currentTime = dt.now() #extract the current time in order to write to the CSV

    # To verify, read and print values for acceleration, output the following format
    #print("Acceleration Chip 1: X: %.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
    #print("Acceleration Chip 2: X: %.2f, Y: %.2f, Z: %.2f m/s^2 " % (mpu_2.acceleration))
    #accelFile.write(str(currentTime), float(mpu.acceleration['x']), float(mpu.acceleration['y']), float(mpu.acceleration['z']))
    
    # Extract acceleration in x, y and z direction from the mpu chip
    acc_x, acc_y, acc_z = mpu.acceleration
    # if wishing to do so for a second chip, do the following
    #acc_x_2, acc_y_2, acc_z_2 = mpu_2.acceleration
    #Apply the low-pass filter here to acceleration coordinates for x, y and z
    filter_x = low_pass_filter(filter_x, acc_x)
    filter_y = low_pass_filter(filter_y, acc_y)
    filter_z = low_pass_filter(filter_z, acc_z)

    # To verify, read and print values for the gyroscope, output the following format
    #print("Gyro Chip 1: X: %.2f, Y: %.2f, Z: %.2f rad/s" % (mpu.gyro))
    #print("Gyro Chip 2: X: %.2f, Y: %.2f, Z: %.2f rad/s" % (mpu_2.gyro))
    #gyroFile.write(str(currentTime), float(mpu.gyro['x']), float(mpu.gyro['y']), float(mpu.gyro['z']))

    # Extract gyroscope data from the mpu in x, y and z directions
    gyro_x, gyro_y, gyro_z = mpu.gyro
    # If needed to do so for a second chip
    #gyro_x_2, gyro_y_2, gyro_z_2 = mpu_2.gyro

    # write to the CSV file for the first chip
    chip1_out.write(str(currentTime)+","+str(filter_x)+","+str(filter_y)+","+str(filter_z)+","+
                    str(gyro_x)+","+str(gyro_y)+","+str(gyro_z)+"\n")
    # if wishing to do for a second chip, do the following
    #chip2_out.write(str(currentTime)+","+str(acc_x_2)+","+str(acc_y_2)+","+str(acc_z_2)+","+
                    #str(gyro_x_2)+","+str(gyro_y_2)+","+str(gyro_z_2)+"\n")

    #Wait for 'q' key to stop the program
    key = cv2.waitKey(20) 
    if key & 0xFF == ord('q'): 
        chip1_out.flush()
        #chip2_out.flush()
        break 

    time.sleep(1)


#After we release the webcam, we also release the out.release() for all windows
cv2.destroyAllWindows()
