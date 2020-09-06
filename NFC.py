import time
import serial

pallets_numbers = {'3640960611': 'Щ234', '187973901': 'Н167'}

def pallet_accordance(pallet_n):
    if pallet_n not in pallets_numbers:
        return
    return pallets_numbers[pallet_n]

def key_by_value(value, dct):
    for key, alue in dct.items():
        if alue == value:
            return key
    return


class NFCAnalyzer:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.lst = []
        self.ser = serial.Serial(port=self.port, baudrate=self.baudrate)
        self.ser.close()
        
    def getUid(self):
        self.ser.open()
        while True:
            while self.ser.inWaiting() > 0:
                line = self.ser.readline()
                if line:
                    self.ser.close()
                    return line.decode().strip()
                break


if __name__ == '__main__':
    NFC = NFCAnalyzer('/dev/ttyACM0', 9600)
    while True:
        time.sleep(2)
        print(NFC.getUid())
