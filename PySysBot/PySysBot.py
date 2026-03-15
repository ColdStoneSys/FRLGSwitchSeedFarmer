import sys
import socket
import binascii
from time import sleep

class PySysBot(object):
    def __init__(self,ip,port = 6000):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(1)
        self.s.connect((ip, port))
        print('Bot Connected')
        self.configure()
        self.moveLeftStick(0,0)
        self.moveRightStick(0,0)

    def configure(self):
        self.sendCommand('configure echoCommands 0')

    def sendCommand(self,content):
        content += '\r\n' #important for the parser on the switch side
        self.s.sendall(content.encode())

    def detach(self):
        self.sendCommand('detachController')

    def close(self,exitapp = True):
        print("Exiting...")
        self.pause(0.5)
        self.detach()
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()
        print('Bot Disconnected')
        if exitapp:
            sys.exit(0)

    # A/B/X/Y/LSTICK/RSTICK/L/R/ZL/ZR/PLUS/MINUS/DLEFT/DUP/DDOWN/DRIGHT/HOME/CAPTURE
    def click(self,button):
        self.sendCommand('click '+ button)

    def press(self,button):
        self.sendCommand('press '+ button)

    def release(self,button):
        self.sendCommand('release '+ button)

    # setStick LEFT/RIGHT <xVal from -0x8000 to 0x7FFF> <yVal from -0x8000 to 0x7FFF
    def moveStick(self,button,x,y):
        self.sendCommand('setStick ' + button + ' ' + hex(x) + ' ' + hex(y))

    def moveLeftStick(self,x = None, y = None):
        if x is not None:
            self.ls_lastx = x
        if y is not None:
            self.ls_lasty = y
        self.moveStick('LEFT',self.ls_lastx,self.ls_lasty)

    def moveRightStick(self,x = None, y = None):
        if x is not None:
            self.rs_lastx = x
        if y is not None:
            self.rs_lasty = y
        self.moveStick('RIGHT',self.rs_lastx,self.rs_lasty)

    #peek <address in hex, prefaced by 0x> <amount of bytes, dec or hex with 0x>
    #poke <address in hex, prefaced by 0x> <data, if in hex prefaced with 0x>       
    def read(self,address,size,filename = None):
        self.sendCommand(f'peek 0x{address:X} 0x{size:X}')
        sleep(size/0x8000)
        buf = self.s.recv(2 * size + 1)
        buf = binascii.unhexlify(buf[0:-1])
        if filename is not None:
            if filename == '':
                filename = f'dump_heap_0x{address:X}_0x{size:X}.bin'
            with open(filename,'wb') as fileOut:
                fileOut.write(buf)
        return buf

    def read_pointer(self,pointer,size,filename = None):
        jumps = pointer.replace("[","").replace("main","").split("]")
        self.sendCommand(f'pointerPeek 0x{size:X} 0x{" 0x".join(jump.replace("+","") for jump in jumps)}')
        sleep(size/0x8000)
        buf = self.s.recv(2 * size + 1)
        buf = binascii.unhexlify(buf[0:-1])
        if filename is not None:
            if filename == '':
                filename = f'dump_heap_{pointer}_0x{size:X}.bin'
            with open(filename,'wb') as fileOut:
                fileOut.write(buf)
        return buf

    def getTitleId(self):
        self.sendCommand('getTitleID')
        sleep(0.005)
        buf = self.s.recv(18)
        return buf[0:-1]

    def pause(self,duration):
        sleep(duration)

    def quitGame(self,needHome=True):
        if needHome:
            self.click("HOME")
            self.pause(0.8)
        self.click("X")
        self.pause(0.2)
        self.click("X")
        self.pause(0.4)
        self.click("A")
        self.pause(0.2)
        self.click("A")
        self.pause(1.3)

    def enterGame(self, verbose=True):
        if verbose:
            print("\nStarting the game")
        self.click("A")
        self.pause(0.2)
        self.click("A")
        self.pause(1.3)
        self.click("A")
        self.pause(0.2)
        self.click("A")

class FRLGBot(PySysBot):
        ADDRESSES = {
            0x01006FA0233F8000: {
                "Game": "FireRed (JPN)",
                "VBlankCounter": 0xBD68B304,
                "CurrentSeedAddress": 0xBD68D230
            },
            0x0100F1E0233FA000: {
                "Game": "LeafGreen (JPN)",
                "VBlankCounter": 0xBD68B304,
                "CurrentSeedAddress": 0xBD68D230
            },
            0x0100554023408000: {
                "Game": "FireRed (ENG)",
                "VBlankCounter": 0xBD68B3A4,
                "CurrentSeedAddress": 0xBD68D2D0
            },
            0x010034D02340E000: {
                "Game": "LeafGreen (ENG)",
                "VBlankCounter": 0xBD68B3A4,
                "CurrentSeedAddress": 0xBD68D2D0
            },
            0x01004B3023412000: {
                "Game": "FireRed (FRE)",
                "VBlankCounter": 0xBD68B2F4,
                "CurrentSeedAddress": 0xBD68D220
            },
            0x010087C02342E000: {
                "Game": "LeafGreen (FRE)",
                "VBlankCounter": 0xBD68B2F4,
                "CurrentSeedAddress": 0xBD68D220
            },
            0x010092302342A000: {
                "Game": "FireRed (ITA)",
                "VBlankCounter": 0xBD68B2F4,
                "CurrentSeedAddress": 0xBD68D220
            },
            0x01005C7023432000: {
                "Game": "LeafGreen (ITA)",
                "VBlankCounter": 0xBD68B2F4,
                "CurrentSeedAddress": 0xBD68D220
            },
            0x01007F8023416000: {
                "Game": "FireRed (GER)",
                "VBlankCounter": 0xBD68B2F4,
                "CurrentSeedAddress": 0xBD68D220
            },
            0x0100FD6023430000: {
                "Game": "LeafGreen (GER)",
                "VBlankCounter": 0xBD68B2F4,
                "CurrentSeedAddress": 0xBD68D220
            },
            0x0100EB702342C000: {
                "Game": "FireRed (SPA)",
                "VBlankCounter": 0xBD68B2F4,
                "CurrentSeedAddress": 0xBD68D220
            },
            0x01002B5023434000: {
                "Game": "LeafGreen (SPA)",
                "VBlankCounter": 0xBD68B2F4,
                "CurrentSeedAddress": 0xBD68D220
            },
        }

        def __init__(self,ip,port = 6000):
            PySysBot.__init__(self,ip,port)
            self.titleID = int(self.getTitleId(), 16)
            if self.titleID == 0:
                print("Game not running")
                self.close()
            elif self.titleID not in self.ADDRESSES:
                print(f"Unsupported title: {self.titleID:016X}")
                self.close()
            self.game = self.ADDRESSES[self.titleID]['Game']
            self.curentSeedAddress = self.ADDRESSES[self.titleID]['CurrentSeedAddress']
            self.VBlankCounter = self.ADDRESSES[self.titleID]['VBlankCounter']
            print(f"Game: {self.game}\n")

        def getInitialSeed(self):
            return int.from_bytes(self.read(0x1208000, 2), "little")

        def getCurrentSeed(self):
            return int.from_bytes(self.read(self.curentSeedAddress, 4), "little")

        def getVBlankCounter(self):
            return int.from_bytes(self.read(self.VBlankCounter, 4), "little")

        def isBoxPointerInitialized(self):
            return int.from_bytes(self.read(self.curentSeedAddress + 0x10, 4), "little") != 0
