import socket
import course   # course.py
import sys

import numpy as np
import matplotlib.pyplot as plt


# Feedback phase function
def feedback():
    global element_cnt        # plot element count
    global plot_interval        # plot point interval
    global fb_arr               # feedback array

    # from course.py course's coordinate point
    course.original_course(element_cnt, plot_interval)

    _X_abs = np.abs(X)          # run coordinate point 'x'
    _P_abs = np.abs(course.P)   # from course.py coordinate point 'x'
    _X_ave = _X_abs.mean()      # average
    _P_ave = _P_abs.mean()      # average
    _point_error = _X_ave - _P_ave    # point_average_error

    _fb_val = _point_error / 2        # Feedback value
    fb_arr = np.append(fb_arr, _fb_val)

    if _fb_val < 0:
        _fb_val = _fb_val * -1

    if Lap > 0 and fb_arr[Lap] < fb_arr[Lap - 1]:
        _fb_val = _fb_val / 2 * -1

    _fb_val_str = str(_fb_val)
    print('FeedbackSteer ' + _fb_val_str)
    conn.send(_fb_val_str.encode())

# variable initialize
gyro = []
element_cnt = 1   # element count
plot_interval = 30   # plot point interval
X = np.zeros(0)
Y = np.zeros(0)
fb_arr = np.zeros(0)
Lap = 0
ROUND_CHECK = 355   # confirm one round

# Main program
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('169.254.207.161', 50010))   # your PC's Bluetooth IP & PORT
    s.listen(1)
    print('Start program...')

    while True:
        conn, addr = s.accept()
        with conn:
            while True:
                gyro_data = conn.recv(1024).decode()
                if not gyro_data:
                    break
                gyro_data_float = float(gyro_data)  # change type
                gyro = np.append(gyro, gyro_data_float)    # gyro angle
                np.set_printoptions(suppress=True)

                cosgy = plot_interval * np.cos(np.radians(gyro)) * -1
                singy = plot_interval * np.sin(np.radians(gyro))
                X = np.append(X, np.sum(cosgy[0:element_cnt]))
                Y = np.append(Y, np.sum(singy[0:element_cnt]))

                if ROUND_CHECK < gyro_data_float:
                    plt.figure()
                    plt.plot(X, Y, '-', color='blue')
                    print('Plot file output')
                    print(str(Lap) + '-plot.png')
                    plt.savefig(str(Lap) + '-plot.png')
                    feedback()

                    # reset phase
                    element_cnt = 0
                    X = np.zeros(0)
                    Y = np.zeros(0)
                    gyro = []
                    plt.clf()   # figure clear
                    plot_interval = 30
                    Lap += 1

                element_cnt = element_cnt + 1   # Element count

            print('End program')
            sys.exit()
