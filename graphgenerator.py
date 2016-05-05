#!/usr/bin/env python

from packetgenerator import packets

import sys
import networkx as nx
import numpy as np
import math
import matplotlib.pyplot as plt
from itertools import islice

from decoder_optimized import *
from encoder import *



# separate the string and packets.
def copy_source_dst_time(x):
    source_c = []
    dst_c = []
    time_c = []
    # print x[:,0]
    for i in range(0, len(x[:, 0])):
        source_c.append(x[i][1])
        # print source_c[i]
        dst_c.append(x[i][0])
        time_c.append(x[i][2])
    return (source_c, dst_c, time_c)


# pad the packets to take the time into acount.
def padding_packet_info(source_find, dst_find, starttime, fill_num):
    l1 = []
    for i in range(0, len(source_find)):
        path = (nx.shortest_path(G, source_find[i], dst_find[i], starttime[i]))
        # sys.exit()
        path.reverse()
        for j in range(0, starttime[i]):
            path.append(-1)

        path.reverse()
        for k in range(0, fill_num - len(path)):
            path.append(-1)
        # print path
        l1.append(path)
    return l1, fill_num


def padding_packet_info_linear(source_find, dst_find, starttime, fill_num):
    l1 = []
    total_time = 0
    for i in range(0, len(source_find)):
        path = (nx.shortest_path(G, source_find[i], dst_find[i], starttime[i]))
        # sys.exit()

        if total_time <= (len(path)+ starttime[i]):
            total_time = len(path)+ starttime[i]
        else:
            total_time = total_time

        path.reverse()
        for j in range(0, starttime[i]):
            path.append(-1)

        path.reverse()
        for k in range(0, fill_num - len(path)):
            path.append(-1)
        # print path
        l1.append(path)
    #print total_time
    #sys.exit()
    return l1, fill_num,total_time


# split the string into separate elments for better manipulation.
def split_string(num_pack, l1):
    temp = [0]
    split_t = []
    # print l1[0]
    for i in range(0, num_pack):
        # print i
        temp = l1[i]
        # temp.append(l1[i])
        split_t.append([temp[j:j + 1] for j in range(0, len(l1[i]), 1)])
        # print split_t
    return split_t

# count reduce transmission.
def count_reduced_transmission(path_in_order, num_packets, fill_num):
    reduced_transmission = []
    transmision_num = []
    for j in range(0, fill_num):
        temp1 = []  # a dictionary shows that what are the different elments at time unit.
        temp2 = []  # a dictionary shows the nodes at each unit for each packet.
        for i in range(0, num_packets - 1):
            if path_in_order[i][j] != [-1]:
                temp2.append(path_in_order[i][j])
            else:
                pass
        for k in range(0, num_packets - 1):
            if path_in_order[k][j] != [-1]:

                if not temp1:
                    temp1.append(path_in_order[k][j])

                else:
                    length = len(temp2)
                    for l in range(0, length - 1):

                        if path_in_order[k][j] in temp1:
                            pass

                        else:
                            temp1.append(path_in_order[k][j])
            else:
                pass

        reduced_transmission.append(len(temp2) - len(temp1))
        transmision_num .append(len(temp1))
    return reduced_transmission, transmision_num

# count reduce transmission.
def count_reduced_transmission_linear(path_in_order, num_packets, fill_num):
    # sys.exit()
    reduced_transmission = []
    transmision_num = []
    flag = 0
    index2 = 0
    index1 = 0  # at each time unit, see how many different nodes involved
    count = 0  # how many transmission could be reduced for each different node at each time unit.
    elements1 = 0
    elements12 = 0
    temp_equal = []

    for j in range(0, fill_num):
        temp1 = []  # a dictionary shows that what are the different elments at time unit.
        temp2 = []  # a dictionary shows the nodes at each unit for each packet.
        for i in range(0, num_packets - 1):
            # print i
            if path_in_order[i][j] != [-1]:
                temp2.append(path_in_order[i][j])
            else:
                pass
        # print temp2
        for k in range(0, num_packets - 1):
            # print k
            if path_in_order[k][j] != [-1]:
                # print path_in_order[k][j]
                # sys.exit()
                if not temp1:
                    temp1.append(path_in_order[k][j])
                    # print temp1
                    # sys.exit()
                else:
                    length = len(temp2)
                    # print "length alkdjalk;dj"
                    # print length
                    for l in range(0, length - 1):
                        # print "asfkjhsd;glkn"
                        # print temp1
                        # print temp1
                        # sys.exit()
                        if path_in_order[k][j] in temp1:
                            pass
                            # print "temp1 ksfjlajfk"
                            # print temp1
                        else:
                            # print "hfakljfbhlk"
                            temp1.append(path_in_order[k][j])
                            # print temp1
                            # sys.exit()
            else:
                pass
        # print "sjfklhfdjk"
        reduced_transmission.append(len(temp2) - len(temp1))
        # print reduced_transmission
        transmision_num.append(len(temp1))
        # return reduced_transmission
        # print "total reduced", reduced
    return reduced_transmission, transmision_num


#compare the string after paddding.
# if the elements are the same, then insert that element to the packet who has a later starttime.
def insert_padding(x, time, num_packets, fill_num):
    start_compare_index = 0
    for i in range(0, num_packets):
        for j in range (i+1, num_packets):
            #print i
            #print j
            for k in range(0, fill_num):
                if x [i][k] == [-1] or x [j][k] == [-1]:
                    pass
                else:
                    if x[i][k] == x[j][k]:
                        #print x [i][k]
                        #print x[j][k]
                        if time[i] == time[j]:
                            insert_element(x[j], k)
                            del (x[j])[-1]
                        else:
                            pass
                    else:
                        pass
    return x

#insert a elemtn into a list.
def insert_element(aList, index):
    aList.insert( index, [-2])
    #print "Final List : ", aList
    #sys.exit()

# find the node that give the last transmission
def find_last_transmission(x, y, i):
    index = 0
    x[i].reverse()
    for j in range (0, y ):
        if x[i][j] == [-1]:
            index += 1

        else:
            index = y -index
            x[i].reverse()
            return index


def non_linear(paramaters, num_packets, fill_num):
    # main function:

    #paramaters = np.loadtxt('packets.txt', dtype=np.int32)

    (source, dst, time) = copy_source_dst_time(paramaters)

    path_info_len = 0

    l1, path_info_len = padding_packet_info(source, dst, time, fill_num)

    path_in_matrix = split_string(num_packets, l1)


    reduced_transmission, transmision_num = count_reduced_transmission(path_in_matrix, num_packets, fill_num)

    b = sum(reduced_transmission)
    c = sum(transmision_num)

    print "The total number of transmission for non-linear encoding scheme"
    print b + c
    path_in_matrix = insert_padding(path_in_matrix ,time, num_packets ,fill_num)



    for i in range(0, num_packets):
        if i == 0:
            last_one = find_last_transmission(path_in_matrix, fill_num, i)
        else:
            if last_one >= find_last_transmission(path_in_matrix,fill_num, i):
                pass
            else:
                last_one = find_last_transmission(path_in_matrix,fill_num, i)

    print "The total time unit spent on non linear coding transmission"
    print last_one
    return b + c, last_one


def common_elements(list1, list2):
    return [element for element in list1 if element in list2]


def linear(paramaters, num_packets, fill_num):
    (source, dst, time) = copy_source_dst_time(paramaters)

    l1, path_info_len, total_time_global = padding_packet_info_linear(source, dst, time, fill_num)

    path_in_matrix = split_string(num_packets, l1)

    reduced_transmission, transmision_num = count_reduced_transmission_linear(path_in_matrix, num_packets, fill_num)

    print "number of transmission reduced"
    b = sum(reduced_transmission)
    print b
    print "Total number of transmission using linear coding scheme"
    c = sum(transmision_num)
    print c

    for i in range(0, num_packets - 1):
        # print i
        if i == 0:
            last_one = find_last_transmission(path_in_matrix, fill_num, i)
        else:
            if last_one >= find_last_transmission(path_in_matrix, fill_num, i):
                pass
            else:
                last_one = find_last_transmission(path_in_matrix, fill_num, i)

    print "The total time unit spent on non linear coding transmission"
    print last_one

    return b, c, last_one






    # determine if the node needs to broadcast the packets or not.
    # dstde means the decoded destination, if the dstde equals to the node
    # flag determines if the packets need to be broadcasted
    # recevie means if the packets has been broadcasted or not.

    # test commom elements:
    common1 = [1, 2, 3, 4]
    common2 = [1, 2, 3, 4]
    list_common = []
    number_reduced = 0


    list_common = common_elements(common1, common2)
    number_reduced = len(list_common)






if __name__ == "__main__":

    data = []
    for edge in range(500, 1100, 20):
        num_packets = 100
        node_number = 100
        total_time = 350
        size = 127
        fill_num = total_time + 20

        paramaters = packets(num_packets, node_number, total_time, size)
        #paramaters = np.loadtxt('packets.txt', dtype=np.int32)

        G = nx.dense_gnm_random_graph(node_number, edge)
        pos = nx.spring_layout(G)
        H = G.number_of_edges()

        colors = range(H)
        nx.draw(G, pos, node_color='#A0CBE2', width=0.4, edge_cmap=plt.cm.Reds, with_labels=True)

        non_linear_trans, non_linear_time = non_linear(paramaters, num_packets, fill_num)
        reduce_time, linear_trans, linear_time = linear(paramaters, num_packets, fill_num)
        data.append([num_packets, node_number, edge, total_time, size, fill_num, non_linear_trans, non_linear_time, linear_trans, linear_time, reduce_time])

    data = np.array(data)
    print data
    np.savetxt("data.csv", data, delimiter=",", header='num_packets, node_number, edge, total_time, size, fill_num, non_linear_trans, non_linear_time, linear_trans, linear_time, reduce_time')



