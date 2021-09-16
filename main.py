from kernel import run
if __name__ == '__main__':

    left = [1, 1, 1]
    right = [1, 1, 1]

    args = {
        'CPUn': 10000000,
        'GPUn': 10000000,
        'threadNum': 1,
        'left': left,
        'right': right,
        'factor': 0.5,
        'op': 1
    }
    print(args)
    # for i in range(0, 10):
    #     res = run.run.apply_async(args=[args], queue='kernel')
    #     print(res.get)


