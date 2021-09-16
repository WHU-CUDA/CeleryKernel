from kernel import app
import ctypes

@app.task
def run(args):
    lib_name = args.lib_name
    lib = ctypes.cdll.LoadLibrary(lib_name)
    lib.run()