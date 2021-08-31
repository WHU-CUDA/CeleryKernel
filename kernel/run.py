from kernel import app
import ctypes
import platform


def islinux():
    sys = platform.system()
    if sys == "Windows":
        return False
    elif sys == "Linux":
        return True
    else:
        pass


@app.task
def run(conf):
    if islinux():
        dll = ctypes.cdll.LoadLibrary('./libkernel.so')
    else:
        dll = ctypes.windll.LoadLibrary('./kernel.dll')
    CPUn = ctypes.c_int(conf['CPUn'])
    GPUn = ctypes.c_int(conf['GPUn'])
    threadNum = ctypes.c_int(conf['threadNum'])
    factor = ctypes.c_float(conf['factor'])
    left = conf['left']
    right = conf['right']
    cleft = (ctypes.c_int * len(left))(*left)
    cright = (ctypes.c_int * len(right))(*right)
    op = ctypes.c_int(conf['op'])
    dll.init(CPUn, GPUn, op, threadNum, cleft, cright, factor)
    result = dll.run()
    return result
