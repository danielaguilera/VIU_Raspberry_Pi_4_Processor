from time import sleep
import serial
import serial.tools.list_ports
import struct  # Asegurarse de importar el módulo struct
import gpiozero
import threading
import numpy as np

PORT_ARDUINO = '/dev/ttyUSB0'
BAUD_RATE_ARDUINO = 19200

PORT_HC06 = '/dev/ttyS0'
BAUD_RATE_HC06 = 9600

TIMEOUT = 1

G = 9.8067

def connectPort(port: str, baudRate: int, timeout: int) -> serial.Serial | None:
    availablePorts: list = serial.tools.list_ports.comports()
    for availablePort in availablePorts:
        print(availablePort)
        portName = str(availablePort).split(' - ')[0]
        if portName == port:
            try:
                ser = serial.Serial(port=port, baudrate=baudRate, timeout=timeout)
                if ser.is_open:
                    return ser
            except serial.SerialException:
                return
    return

def main():
    print("Esperando conexión serial")
    serHC06 = serial.Serial(port=PORT_HC06, baudrate=BAUD_RATE_HC06, timeout=TIMEOUT)
    serArduino = connectPort(port=PORT_ARDUINO, baudRate=BAUD_RATE_ARDUINO, timeout=TIMEOUT)
    if not serArduino:
        print('No se pudo conectar')
        return
    
    while True:
        data = serArduino.readline()
        if len(data) == 8:
            if (data[0] == 33) and (data[7] == 10):
                Ax, Ay, Az = struct.unpack('<hhh', data[1:7])
                ax = round(Ax/2048.0 * G, 2)
                ay = round(Ay/2048.0 * G, 2)
                az = round(Az/2048.0 * G, 2)
                a = round(np.sqrt((ax**2) + (ay**2) + (az**2)),2)
                print(f'SEND: #{a}\n')
                serHC06.write(f'#{a}\n'.encode())
        serArduino.reset_input_buffer()
        sleep(0.05)

if __name__ == '__main__':
    main()

