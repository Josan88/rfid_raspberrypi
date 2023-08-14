from ctypes import *
import ctypes
import time
import sys


def python_print_hex(di, Length):
    print(
        "#============================================================================="
    )
    s = ""
    hexstr = ""

    if di == None:
        return
    tt = 0
    for i in di:
        s = "{:02X}".format(int(i & 0xFF))
        hexstr = hexstr + s + " "

        tt = tt + 1
        if tt == Length:
            break
    print(hexstr)
    print(
        "#==========================================================================="
    )


def main():
    dll = cdll.LoadLibrary("./libSYSIOT_NET_Driver.so")

    ReaderIP = "192.168.2.159"
    ReaderIPBytes = bytes(ReaderIP, encoding="utf8")
    ReaderPort = 200

    byte_Sarr300 = ctypes.c_byte * 300
    byte_Rarr300 = ctypes.c_byte * 300
    int_arr2 = ctypes.c_int * 2
    # ======================================================================================
    print("Reader IP=", ReaderIP)
    print("Reader Port=", ReaderPort)

    ReaderHandl = 0
    ReaderHandl = dll.SYSIOT_NET_OpenPort(ReaderIPBytes, ReaderPort)
    print("ReaderHandl:", ReaderHandl)

    if ReaderHandl <= 0:
        print("Connect Reader Fail:")
        return 0
        # ======================================================================================
    # resuilt=dll.SYSIOT_NET_Python_MultiTagReadStop(ReaderHandl)
    # print ("SYSIOT_NET_Python_MultiTagReadStop resuilt:", resuilt)
    # ======================================================================================

    SendData1 = byte_Sarr300()
    SendData1[0] = 0xFF
    SendData1[1] = 0x06
    SendData1[2] = 0x03
    SendData1[3] = 0x00
    SendData1[4] = 0x00
    print("SendData1:", SendData1)

    SendData1_length = int_arr2()
    SendData1_length[0] = 5
    SendData1_length[1] = 0
    print("SendData1_length[0]:", SendData1_length[0])

    Response1 = bytearray(300)
    Response1 = b"\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00"

    Response1_length = int_arr2()
    Response1_length[0] = 0
    Response1_length[1] = 0

    # print("Response1_length:", Response1_length[0])
    # print("Response1:" , Response1)
    print("Response1[0]:", Response1[0])

    resuilt = dll.SYSIOT_NET_Python_ExeCution(
        ReaderHandl, SendData1_length, SendData1, Response1_length, Response1
    )
    print("resuilt:", resuilt)
    print("Response1_length:", Response1_length[0])
    print("Response1:", Response1)
    if Response1_length[0] > 0:
        python_print_hex(Response1, Response1_length[0])

    # ======================================================================================
    SendData = byte_Sarr300()
    SendData[0] = 0xFF
    SendData[1] = 0x05
    SendData[2] = 0x0F
    SendData[3] = 0x00
    print("SendData:", SendData)

    SendData_length = int_arr2()
    SendData_length[0] = 4
    SendData_length[1] = 0
    print("SendData_length[0]:", SendData_length[0])

    Response1 = bytearray(300)
    Response1 = b"\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00"

    Response1_length = int_arr2()
    Response1_length[0] = 0
    Response1_length[1] = 0

    # print("Response1_length:", Response1_length[0])
    # print("Response1:" , Response1)
    print("Response1[0]:", Response1[0])

    resuilt = dll.SYSIOT_NET_Python_ExeCution(
        ReaderHandl, SendData1_length, SendData1, Response1_length, Response1
    )
    print("resuilt:", resuilt)
    print("Response1_length:", Response1_length[0])
    print("Response1:", Response1)
    if Response1_length[0] > 0:
        python_print_hex(Response1, Response1_length[0])

    return 0


if __name__ == "__main__":
    main()
