import serial
from Metadata import *

def getBaudRate() -> int:
    for baudRate in BAUD_RATES.keys(): 
        ser = serial.Serial(port=PORT_HC06, baudrate=baudRate, timeout=TIMEOUT)
        ser.write('AT'.encode())
        response = ser.readall()
        if response == b'OK':
            ser.close()
            return baudRate
        ser.close()
    return 0

def setBaudRate(newbaudRate: int) -> bool:
    baudRate = getBaudRate()
    if not baudRate:
        print('No accesible')
        return False
    ser = serial.Serial(port=PORT_HC06, baudrate=baudRate, timeout=TIMEOUT)
    if not (newbaudRate in BAUD_RATES.keys()):
        print('Baud rate no disponible')
        ser.close()
        return False
    index = BAUD_RATES[newbaudRate]
    ser.write(f'AT+BAUD{index}'.encode())
    response = ser.readall()
    if response.decode() != f'OK{newbaudRate}':
        print('No se cambió baud rate')
        ser.close()
        return False
    print(f'Baud rate cambiado a {newbaudRate} baud')
    ser.close()
    return True

def setName(name: str) -> bool:
    baudRate = getBaudRate()
    ser = serial.Serial(port=PORT_HC06, baudrate=baudRate, timeout=TIMEOUT)
    ser.write(f'AT+NAME{name}'.encode())
    response = ser.readall()
    if response.decode() != 'OKsetname':
        print('No se cambió el nombre')
        ser.close()
        return False
    print(f'Nuevo nombre: {name}')
    ser.close()
    return True