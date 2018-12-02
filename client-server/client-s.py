#!/usr/bin/env python3

import socket
import struct
import time
from os import system

import csv

HOST = '127.0.0.1'
PORT = 8001
FILE = "/tmp/received.ply"  # change it to whatever you want


def main():
    system('displaz &')

    with open('metrics.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            count = count +1
            x = float(row["x"])
            y = float(row["y"])
            radius = float(row['radius'])

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                st = time.time()
                s.connect((HOST, PORT))
                s.sendall(struct.pack('!d d d', x, y, radius))
                data = s.recv(4)
                num = struct.unpack('!i', data)[0]

                data = b''
                while num - len(data):
                    packet = s.recv(num)
                    if not packet:
                        break
                    data += packet

            with open(FILE, 'bw') as myfile:
                myfile.write(data)

            if count % 10 == 0:
                print("Total Processed Location : " , count)
                

            system('displaz -clear %s' % FILE)

        print('Time taken: %f seconds' % (time.time() - st))
        print('Received: {0:,d} bytes\n'.format(len(data)))

if __name__ == '__main__':
    main()

