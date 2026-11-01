import time
import socket
import sys
import ev3dev.ev3 as ev3


# power range:-1050 -> 1050, turn_ratio range:-100 -> 100
def linetrace_steer(power, turn_ratio):
    global data_cycle
    if color.reflected_light_intensity > 30:
        ev3_motor_steer(power, turn_ratio*-1)
    else:
        ev3_motor_steer(power, turn_ratio)
    time.sleep(0.1)
    data_cycle += 1


def ev3_motor_steer(power, turn_ratio):
    if turn_ratio < 0:
        lm_b.run_forever(speed_sp=power*(1+turn_ratio/50))
        lm_c.run_forever(speed_sp=power)
    elif turn_ratio > 0:
        lm_b.run_forever(speed_sp=power)
        lm_c.run_forever(speed_sp=power*(1-turn_ratio/50))
    else:
        lm_b.run_forever(speed_sp=power)
        lm_c.run_forever(speed_sp=power)


def gyro_reset():
    time.sleep(1.0)
    gyro.mode = 'GYRO-ANG'
    gyro.mode = 'GYRO-RATE'
    gyro.mode = 'GYRO-ANG'
    time.sleep(1.0)


def dataget():
    global fb_steer     # feedback steering value
    global set_steer

    _gyro_data = gyro.value()  # gyro data
    _gyro_data_str = str(_gyro_data)
    s.send(_gyro_data_str.encode())
    print(_gyro_data_str)

    if ROUND_CHECK < _gyro_data:
        while not(button.up):
            ev3_motor_steer(0, 0)
            if fb_steer is None:
                fb_steer = s.recv(1024).decode()
                fb_steer_float = float(fb_steer)
                print(fb_steer_float)
                set_steer = set_steer - fb_steer_float
            if button.backspace:
                s.close
                print('End program')
                sys.exit()
        print('set_steer = ' + str(set_steer))
        # gyro reset
        gyro_reset()
        fb_steer = None

# sensors&motors definition
button = ev3.Button()
color = ev3.ColorSensor('in3')
gyro = ev3.GyroSensor('in2')
lm_b = ev3.LargeMotor('outB')
lm_c = ev3.LargeMotor('outC')

# gyro initialize
gyro_reset()

# variable initialize
data_cycle = 1           # counter
fb_steer = None    # Feedback turn
ROUND_CHECK = 355   # confirm one round

# motor initialize
lm_b.reset()
lm_c.reset()
set_power = 200
set_steer = 70

# get gyrodate and into array
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('169.254.207.161', 50010))    # your PC's Bluetooth IP & PORT
    while not(button.backspace):
        linetrace_steer(set_power, set_steer)
        if data_cycle % 4 == 0:    # gyro_get_frequency
            dataget()

lm_b.stop(stop_action='brake')
lm_c.stop(stop_action='brake')
print('End program')
sys.exit()
