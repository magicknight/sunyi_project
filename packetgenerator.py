from numpy.random import randint
import numpy as np


def packets(packets_number, node_number, total_time, size):
    return np.transpose(np.array([randint(node_number, size=packets_number), randint(node_number, size=packets_number), randint(total_time, size=packets_number), [size]*packets_number]))


if __name__ == "__main__":
    packets_number = 7
    node_number = 10
    total_time = 35
    size = 127
    np.savetxt('packets.txt', packets(packets_number, node_number, total_time, size), fmt='%i')