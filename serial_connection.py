from serial import *
import serial.tools.list_ports

class SerialConnection:
    
    def __init__(self) -> None:
        self.available_ports = {"ports": [],
                                "descriptions": [],
                                "IDs": []}
    
    def check_available_ports(self) -> dict:
        # GET A LIST OF ALL AVAILABLE SERIAL PORTS
        ports = serial.tools.list_ports.comports()
        self.available_ports = {"ports": [],
                                "descriptions": [],
                                "IDs": []}
        # TO VERIFY IF THERE IF SOME CONECTE DEVICE
        if len(ports) != 0:
            for port, description, id in sorted(ports):
                if port not in self.available_ports["ports"]:
                    self.available_ports["ports"].append(port)
                    self.available_ports["descriptions"].append(description)
                    self.available_ports["IDs"].append(id)
                
        
        return self.available_ports
        
    
    # STARTING SERIAL CONNECTION
    def start(self, serial_port:str, baudrate:int=9600, timeout:int=1) -> bool:
        try: # SUCCESFUL CONNECTION
            
            return Serial(serial_port, baudrate=baudrate, timeout=timeout)
        
        except: # FAIL CONNECTION
            
            return None
    
    # ENDING SERIAL CONNECTION
    def end(self, connected_device) -> None:
        connected_device.close()