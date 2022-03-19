#!/usr/bin/python3
from ast import Bytes
import socket
import time
import struct
import math

'''
Short explanation of the Request and Response headers.

Modbus TCP/IP ADU Request header TX:
- Transaction identifier: 2 Bytes
- Protocol identifier: 2 Bytes
- Message length: 2 Bytes
- Unit identifier: 1 Byte
- Function code: 1 Byte
- The PLC data address: 2 Bytes
- Quantity of registers or writable coil/register: 2 Bytes

Modbus TCP/IP ADU Response header RX:
- Transaction identifier: 2 Bytes
- Protocol identifier: 2 Bytes
- Message length: 2 Bytes
- Unit identifier: 1 Byte
- Function code: 1 Byte
- The PLC data address: 2 Bytes
- Quantity of registers or writable coil/register: 2*n Bytes

'''

TCP_IP = 'localhost'
TCP_PORT = 502

# Class responsible for Modbus TCP/IP protocol and handling the response.
class TCP_socket():

    def __init__(self, buffer_size=1024):
        self.is_polling: bool = True
        self.unit_id: int = 1
        self.buffer_size: int = buffer_size
        self.function_code: int = 3
        self.register: int = 10
        self.plc_address: int = 0
        self.write_value: int = 255
        self.response = None

        # Switch data structure for case searching error codes
        self.error_switcher = {
            1 : 'Illegal Function',
            2 : 'Illegal Data Address',
            3 : 'Illegal Data Value',
            4 : 'Slave Device Failure',
            5 : 'Acknowledge',
            6 : 'Slave Device Busy',
            7 : 'Negative Acknowledge',
            8 : 'Memory Parity Error',
            10 : 'Gateway Path Unavailable',
            11 : 'Gateway Target Device Failed to Respond'
        }

        self.function_code_switcher = {
            1 : 'Read Coil Status',
            2 : 'Read Input Status',
            3 : 'Read Holding Registers',
            4 : 'Read Input Registers',
            5 : 'Force Single Coil',
            6 : 'Force Single Register',
            15 : 'Force Multiple Coils'
        }


    def __error_handler(self):
        '''
        Handle TCP response errors and show error codes.
        '''
        print('Function code: ' + str(self.response[7]))
        print('Error code: ' + str(self.response[8])+'. '+ self.error_switcher[self.response[8]])

    def __grouped(self, iterable, n):
        '''
        Make iterable datastructure as grouped. This can be used for looping 2 elements at the same time.
        '''
        return zip(*[iter(iterable)]*n)


    def tcp_handshake(self) -> Bytes:
        '''
        Connect TCP socket to modbus slave and establish handshake protocol 
        with using wanted function code.

        Parameters:
            - class self parameters

        Return values:
            - TCP response header, datatype = Bytes 
        '''
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((TCP_IP, TCP_PORT)) 
        
            print('Create request header..')
            if int(self.function_code in [1, 2, 3, 4]):
                req = struct.pack('12B', 0x00, 0x01, 0x00, 0x00, 0x00, 0x06,
                              int(self.unit_id), int(self.function_code), 0x00, int(self.plc_address),0x00, int(self.register))
            
            elif int(self.function_code) == 5:
                req = struct.pack('12B', 0x00, 0x01, 0x00, 0x00, 0x00, 0x06,
                              int(self.unit_id), int(self.function_code), 0x00, int(self.plc_address),int(self.write_value), 0x00)
            
            elif int(self.function_code) == 6:
                req = struct.pack('12B', 0x00, 0x01, 0x00, 0x00, 0x00, 0x06,
                              int(self.unit_id), int(self.function_code), 0x00, int(self.plc_address),0x00, int(self.write_value))
            
            elif int(self.function_code) == 15:
                get_input = True
                i = 0
                coil_values = ''

                while get_input:
                    # This works only with 3 values as the byte list implementation supports only coil_values between 0 and 255
                    value = input('Enter coil value: ')
                    if value == '':
                        get_input = False
                    else:
                        coil_values += value
                    i +=1
                
                bytecount = int(math.ceil(i / 8))
                self.register = i

                req = struct.pack("14B", 0x00, 0x05, 0x00, 0x00, 0x00, 0x08, int(self.unit_id), int(self.function_code), 0x00,
                            int(self.plc_address), 0x00, int(self.register), int(bytecount), int(coil_values[::-1]))

            sock.send(req)
            print("Request ADU TX: (%s)" % req)
            self.response = sock.recv(self.buffer_size)
            print(f'Response ADU RX: {self.response}')
            time.sleep(2)

        except ConnectionRefusedError:
            print(f'There was an error while connecting to modbus slave.')

        except Exception:
            print(f'There was an error in creating requests.')

        finally:
            print('CLOSING SOCKET\n')
            sock.close()


    def response_handler(self) -> None:
        '''
        Parameters:
            - None
        Return values:
            - None
        '''
        print('Modbus/TCP')
        print('Transaction identifier: '+ str(int.from_bytes(bytes(bytearray([self.response[0], self.response[1]])),byteorder='big')))
        print('Protocol identifier: '+ str(int.from_bytes(bytes(bytearray([self.response[2], self.response[3]])),byteorder='big')))
        print('Length: '+ str(int.from_bytes(bytes(bytearray([self.response[4], self.response[5]])),byteorder='big')))
        print('Unit identifier: '+ str(self.response[6]))
        print('')

        if self.response[7] in [1, 2, 3, 4, 5, 6, 15, 16]:
            print('Function code: '+ str(self.response[7]), self.function_code_switcher[int(self.response[7])])
            
            # Select function codes that response returns bit values (1/0) to show response correctly.
            if self.response[7] in [1, 2]:
                print('Byte count: '+ str(self.response[8]))
                coils_data = ''
               
                # Loop through all possible bytes that contain bit values in coils.
                for coil_byte in range(9, len(self.response)):
                    coils_data += str(bin(self.response[coil_byte]).lstrip('0b')[::-1])
               
               # Add zero padding to data that we want to show to show it correctly
                if len(coils_data) != self.register:
                    zeros_to_add = int(self.register) - len(coils_data)
                    zeros = ''
                    zeros = zeros.zfill(zeros_to_add)
                    coils_data += zeros

                # Show the Bit values that slave has.
                for i in range(int(self.register)):
                    print('Bit', i, ':', coils_data[i])

            elif self.response[7] in [3, 4]:
                print('Byte count: '+ str(self.response[8]))
                i = 0
                for byte1, byte2 in self.__grouped(self.response[9::],2):
                    print('Register '+str(i)+' (UINT16) : '+str((int.from_bytes(bytes(bytearray([byte1, byte2])),byteorder='big'))))
                    i += 1

            elif self.response[7] == 5:
                print('Reference Number: '+str(int.from_bytes(bytes(bytearray([self.response[8], self.response[9]])),byteorder='big')))
                print('Data: '+str(hex(int.from_bytes(bytes(bytearray([self.response[10], self.response[11]])),byteorder='big'))))
                print('Padding: '+ str(hex(self.response[11])))


            elif self.response[7] == 6:
                print('Reference Number: '+str(int.from_bytes(bytes(bytearray([self.response[9], self.response[10]])),byteorder='big')))
                print('Data: integer value = '+ str(self.response[11]) + ', hex value = ' + str(hex(self.response[11])))

            elif self.response[7] == 15:
                print('Reference Number: '+str(int.from_bytes(bytes(bytearray([self.response[8], self.response[9]])),byteorder='big')))
                print('Bit Count: '+str((int.from_bytes(bytes(bytearray([self.response[10], self.response[11]])),byteorder='big'))))

            print('')
        else:
            self.__error_handler()


    def get_info(self) -> None:
        '''
        Get Modbus TCP input arguments to send request to correct slave unit with correct data.
        '''
        print()

        ip_address = input('Provide PLC address: ')
        self.tcp_ip = 'localhost' if ip_address == '' else ip_address

        unit_id = input('Provide unit id number: ')
        self.unit_id = unit_id if unit_id.isnumeric() else 1

        f_code = input('Provide function code: ')
        self.function_code = int(f_code) if f_code.isnumeric() else 1


        if int(self.function_code) == 5:
            value = input('Enter coil write value (1/0): ')
            self.write_value = 255 if int(value) == 1 else 0
            self.plc_address = self.tcp_ip


        elif int(self.function_code) == 6:
            value = input('Enter register write value: ')
            self.write_value = value if value.isnumeric() else 0
            self.plc_address = self.tcp_ip

        elif int(self.function_code) == 15:
            plc_address = input('Enter starting pcl address: ')
            self.plc_address = plc_address if plc_address.isnumeric() else 0

        else:
            register_len = input('Provide quantity of registers:')
            self.register = register_len if register_len.isnumeric() else 10



def main():
    # Init TCP socket
    tcp_socket = TCP_socket()

    # Start continuous polling and ask user everytime request header values.
    while tcp_socket.is_polling:
        # Ask user parameters for request header
        tcp_socket.get_info()

        # Create request and catch the response if possible.
        tcp_socket.tcp_handshake()

        # Show response in proper format (Hex -> interger)
        if tcp_socket.response is not None:
           tcp_socket.response_handler()

        # poll or not to poll
        tcp_socket.is_polling = True if input("Continue polling (Y/n): ") == 'Y' else False
        


if __name__ == '__main__':
    main()