#!/usr/bin/env python3

import socket
import os
import sys
from time import sleep
from openpyn import root

def socket_connect(server, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, port))
    return s


def show():
    sleep(1)

    while True:
        try:
            s = socket_connect('localhost', 7015)
        except ConnectionRefusedError:
            sleep(3)
            continue
        break
    try:
        server_name = ""
        last_status_UP = False
        while True:
            data = s.recv(1024)
            data_str = repr(data)
            # print(data_str)
            # if 'UPDOWN:DOWN' or 'UPDOWN:UP' or 'INFO' in data_str:
            if 'UPDOWN:UP' in data_str:
                last_status_UP = True
                # print ('Received AN UP')

            if 'UPDOWN:DOWN' in data_str:
                last_status_UP = False

                # print ('Received A DOWN', data_str)

            server_name_location = data_str.find("common_name=")
            # print(server_name_location)
            if server_name_location != -1 and last_status_UP is True:
                server_name_start = data_str[server_name_location + 12:]
                server_name = server_name_start[:server_name_start.find(".com") + 4]
                # print("Both True and server_name", server_name)

            # break of data stream is empty
            if not data:
                break

    except (KeyboardInterrupt) as err:
        print('\nShutting down safely, please wait until process exits\n')
    except ConnectionResetError:
        sys.exit()

    s.close()
    return


if __name__ == '__main__':
    show()
