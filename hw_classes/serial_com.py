# **************************************************************************
# * Authors: Tibor Füzik
# *
# * This program is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program.  If not, see <https://www.gnu.org/licenses/>.
# *
# * Copyright (C) 2020 Tibor Füzik
# **************************************************************************

import serial


class Serial_communication:
    def __init__(self, port):
        self.port = port
        self.connect(port)
        self.SEQUENCE = '\x31'
        self.addres_to_ascii = {"0": "1", "1": "2", "2": "3", "3": "4", "4": "5", "5": "6", "6": "7", "7": "8",
                                "8": "9", "9": ":", "A": ";", "B": "<", "C": "=", "D": ">", "E": "?", "F": "@"}

    def connect(self, port):
        self.ser = serial.Serial(baudrate=9600, timeout=2, port=port)

    def disconnect(self):
        self.ser.close()

    def _make_checksum(self, packet):
        checksum = 0
        for el in packet:
            checksum ^= ord(el)
        return checksum

    def _read_com_response(self):
        response = self.ser.read_until(b'\x03')
        if len(response) > 0:
            while response[0] != 2 and response[0] != 3:
                response = response[1:]
                if len(response) == 0:
                    break
        return response

    def _decode_response(self, response):
        if len(response) > 0:
            status_ready = False
            address = response[1]
            status_byte = response[2]
            if status_byte & 0b0100000:
                status_ready = True
            error_code = int(status_byte & 0b1111)
            data = response[4:response.index(b'\x03')]
            return address, status_ready, error_code, data
        return 0, 0, 0, 0

    def send_command(self, command_buffer, hw_address):
        STX = '\x02'
        ETX = '\x03'
        if ord(self.SEQUENCE) < ord('\x37'):
            self.SEQUENCE = chr(ord(self.SEQUENCE) + 1)
        else:
            self.SEQUENCE = '\x31'

        ADDRESS = self.addres_to_ascii[hw_address]

        command = STX + ADDRESS + self.SEQUENCE + command_buffer + ETX
        CHECKSUM = self._make_checksum(command)

        response = b''
        max_repeat = 5

        while len(response) < 1 and max_repeat > 0:
            self.ser.write((command + chr(CHECKSUM)).encode())
            #print((command + chr(CHECKSUM)).encode())
            response = self._read_com_response()
            max_repeat -= 1

        return self._decode_response(response)
