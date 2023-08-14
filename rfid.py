from ctypes import *
import ctypes
import time
import sys

SCANNED_TAGS = []


def python_print_hex(di, Length):
    # print(
    #     "\n#============================================================================="
    # )
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

    # print(hexstr)
    # print(
    #     "#==========================================================================="
    # )
    # print("End of RFID Tag Data.")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # print("Timestamp:", timestamp)
    # print("\n")

    return hexstr, timestamp


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
        # python_print_hex(Response1, Response1_length[0])
        print("Success!\n")

    # ======================================================================================
    resuilt = dll.SYSIOT_NET_Python_MultiTagReadStop(ReaderHandl)
    print("SYSIOT_NET_Python_MultiTagReadStop resuilt:", resuilt)
    # ======================================================================================
    SendData = byte_Sarr300()
    SendData[0] = 0xFF
    SendData[1] = 0x08
    SendData[2] = 0xC1
    SendData[3] = 0x02
    SendData[4] = 0x00
    SendData[5] = 0x00
    SendData[6] = 0xBC
    print("SendData:", SendData)

    SendData_length = int_arr2()
    SendData_length[0] = 7
    SendData_length[1] = 0
    print("SendData_length[0]:", SendData_length[0])

    resuilt = dll.SYSIOT_NET_Python_MultiTagReadStart(
        ReaderHandl, SendData_length, SendData
    )
    print("SYSIOT_NET_Python_MultiTagReadStart resuilt:", resuilt)

    if resuilt != 0:
        return 0
    try:
        index = 1
        while True:
            Response = bytearray(300)
            Response = b"\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00"

            Response_length = int_arr2()
            Response_length[0] = 0
            Response_length[1] = 0

            # Filter response

            resuilt = dll.SYSIOT_NET_Python_MultiTagGetData(
                ReaderHandl, Response_length, Response
            )

            # print("SYSIOT_NET_Python_MultiTagGetData resuilt:", resuilt)
            # print("Response_length:", Response_length[0])
            # print("Response:", Response)
            # print("Response:")

            if Response_length[0] >= 11:
                # python_print_hex(Response, Response_length[0])
                print("Tag #", index)
                index += 1
                resp = Response[8 : Response_length[0]]
                hexstr, timestamp = python_print_hex(resp, Response_length[0] - 11)

                # Create a dictionary of the scanned tag data
                tag_data = {"timestamp": timestamp, "tag_data": hexstr}
                print(tag_data)

                # Append the dictionary to the SCANNED_TAGS list or update the timestamp if the same tag has been scanned before
                if tag_data not in SCANNED_TAGS:
                    SCANNED_TAGS.append(tag_data)
                else:
                    for tag in SCANNED_TAGS:
                        if tag == tag_data:
                            tag["timestamp"] = timestamp

    except KeyboardInterrupt:
        resuilt = dll.SYSIOT_NET_Python_MultiTagReadStop(ReaderHandl)
        print("SYSIOT_NET_Python_MultiTagReadStop resuilt:", resuilt)

        # Write the SCANNED_TAGS list to a file
        with open("scanned_tags.txt", "w") as f:
            f.write(str(SCANNED_TAGS))

        return 0


if __name__ == "__main__":
    main()
