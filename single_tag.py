from ctypes import *
import ctypes
import time

SCANNED_TAGS = []
REGISTERED_TAGS = []


def python_print_hex(di, Length):
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

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # Create a dictionary of the scanned tag data
    tag_data = {"timestamp": timestamp, "tag_data": hexstr}
    print(tag_data)

    time.sleep(1)


def main():
    dll = cdll.LoadLibrary("./libSYSIOT_NET_Driver.so")

    ReaderIP = "192.168.2.159"
    ReaderIPBytes = bytes(ReaderIP, encoding="utf8")
    ReaderPort = 200

    byte_Sarr300 = ctypes.c_byte * 300
    byte_Rarr300 = ctypes.c_byte * 300
    int_arr2 = ctypes.c_int * 2

    print("Reader IP =", ReaderIP)
    print("Reader Port =", ReaderPort)

    ReaderHandl = 0
    ReaderHandl = dll.SYSIOT_NET_OpenPort(ReaderIPBytes, ReaderPort)

    if ReaderHandl <= 0:
        print("Connect Reader Fail:")
        return 0

    # ======================================================================================

    SendData1 = byte_Sarr300()
    SendData1[0] = 0xFF
    SendData1[1] = 0x06
    SendData1[2] = 0x03
    SendData1[3] = 0x00
    SendData1[4] = 0x00

    SendData1_length = int_arr2()
    SendData1_length[0] = 5
    SendData1_length[1] = 0

    Response1 = bytearray(300)
    Response1 = b"\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00"

    Response1_length = int_arr2()
    Response1_length[0] = 0
    Response1_length[1] = 0

    resuilt = dll.SYSIOT_NET_Python_ExeCution(
        ReaderHandl, SendData1_length, SendData1, Response1_length, Response1
    )

    if Response1_length[0] > 0:
        print("Success!\n")

    # ======================================================================================
    while True:
        SendData = byte_Sarr300()
        SendData[0] = 0xFF
        SendData[1] = 0x08
        SendData[2] = 0xC8
        SendData[3] = 0x02
        SendData[4] = 0x00
        SendData[5] = 0x00
        SendData[6] = 0xBC

        SendData_length = int_arr2()
        SendData_length[0] = 7
        SendData_length[1] = 0

        Response = bytearray(300)
        Response = b"\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00"

        Response_length = int_arr2()
        Response_length[0] = 0
        Response_length[1] = 0

        resuilt = dll.SYSIOT_NET_Python_ExeCution(
            ReaderHandl, SendData_length, SendData, Response_length, Response
        )
        time.sleep(1)
        print(Response1_length[0])

        if Response1_length[0] >= 0:
            resp = Response[8 : Response_length[0]]
            # python_print_hex(resp, Response1_length[0] - 11)


if __name__ == "__main__":
    main()
