import serial                              

port= "/dev/ttyACM0"                        
serialFromArduino = serial.Serial(port, 9600)
serialFromArduino.flushInput()              
while True:                                
    input_s = serialFromArduino.readline() 
    input = float(input_s)                
    print(input)                         
