import numpy as np
import matplotlib.pyplot as plt


def original_course(element_cnt, plot_interval):
    _element_cnt_f = element_cnt % 10    # element count fraction
    _element_cnt_unf = (element_cnt - _element_cnt_f)
    _element_cnt_s = _element_cnt_unf / 10  # element count one course section
    plot_interval = plot_interval + (_element_cnt_f*(plot_interval/_element_cnt_unf))

    _xcount = 1
    _ycount = 1
    _rcount = 1
    global P
    P = np.zeros(0)
    global Q
    Q = np.zeros(0)

    # 1
    while not _xcount > _element_cnt_s:
        _x1 = plot_interval * -1*_xcount
        _y1 = 0
        P = np.append(P, _x1)
        Q = np.append(Q, _y1)
        _xcount += 1

    # 2
    while not _xcount > _element_cnt_s * 2:
        _x2 = plot_interval * -1*_xcount
        _y2 = 0
        P = np.append(P, _x2)
        Q = np.append(Q, _y2)
        _xcount += 1

    # 3 cercle
    _rcount = 0
    while not _rcount > _element_cnt_s:
        _a1 = plot_interval*(_element_cnt_s*2) * -1    # cercle centerX
        _b1 = plot_interval*_element_cnt_s - plot_interval  # cercle centerY & radius
        _x3 = _a1 + _b1*np.cos(np.radians(270-(90 / _element_cnt_s*_rcount)))
        _y3 = _b1 + _b1*np.sin(np.radians(270-(90 / _element_cnt_s*_rcount)))
        P = np.append(P, _x3)
        Q = np.append(Q, _y3)
        _rcount += 1

    # 4
    while not _ycount > _element_cnt_s:
        _x4 = _x3
        _y4 = plot_interval*_ycount + _y3
        P = np.append(P, _x4)
        Q = np.append(Q, _y4)
        _ycount += 1

    # 5 cercle
    _rcount = 0
    while not _rcount > _element_cnt_s:
        _a2 = _a1    # cercle centerX
        _b2 = _y4    # cercle centerY
        _x5 = _a2 + _b1*np.cos(np.radians(180-(90 / _element_cnt_s*_rcount)))
        _y5 = _b2 + _b1*np.sin(np.radians(180-(90 / _element_cnt_s*_rcount)))
        P = np.append(P, _x5)
        Q = np.append(Q, _y5)
        _rcount += 1

    # 6
    _xcount = 1
    while not _xcount > _element_cnt_s:
        _x6 = _x5 + plot_interval*_xcount
        _y6 = _y5
        P = np.append(P, _x6)
        Q = np.append(Q, _y6)
        _xcount += 1

    # 7
    _xcount = 1
    while not _xcount > _element_cnt_s:
        _x7 = _x6 + plot_interval*_xcount
        _y7 = _y6
        P = np.append(P, _x7)
        Q = np.append(Q, _y7)
        _xcount += 1

    # 8 cercle
    _rcount = 0
    while not _rcount > _element_cnt_s:
        _a3 = 0     # cercle centerX
        _b3 = _y4    # cercle centerY
        _x8 = _a3 + _b1*np.cos(np.radians(90-(90 / _element_cnt_s*_rcount)))
        _y8 = _b3 + _b1*np.sin(np.radians(90-(90 / _element_cnt_s*_rcount)))
        P = np.append(P, _x8)
        Q = np.append(Q, _y8)
        _rcount += 1

    # 9
    _ycount = 1
    while not _ycount > _element_cnt_s:
        _x9 = _x8
        _y9 = plot_interval*_ycount*-1 + _y8
        P = np.append(P, _x9)
        Q = np.append(Q, _y9)
        _ycount += 1

    # 10 cercle
    _rcount = 0
    while not _rcount > _element_cnt_s:
        _a4 = 0     # cercle centerX
        _b4 = _b1     # cercle centerY
        _x10 = _a4 + _b1*np.cos(np.radians(0-(90 / _element_cnt_s*_rcount)))
        _y10 = _b4 + _b1*np.sin(np.radians(0-(90 / _element_cnt_s*_rcount)))
        P = np.append(P, _x10)
        Q = np.append(Q, _y10)
        _rcount += 1

if __name__ == '__main__':
    original_course(100, 30)
    plt.figure()
    plt.plot(P, Q, '-', color='blue')
    plt.show()
