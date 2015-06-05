import sys, serial, argparse
from datetime import datetime

# plot class
class Sniff:
    # constr
    def __init__(self, strPort, baud):
        # open serial port
        self.ser = serial.Serial(strPort, baud)
 
    def read(self, count, store_ts):
        try:
            line = self.ser.readline()[:-1]
            if store_ts:
                ts = str(datetime.now()).split('.')[0]
                print(str(count) + ',' + ts + ',' + line)
            else:
                print(line)
                
            return 1

        except KeyboardInterrupt:
            return 0

    # clean up
    def close(self):
        # close serial
        self.ser.flush()
        self.ser.close()
 
# main() function
def main():
    # create parser
    parser = argparse.ArgumentParser(description='A serial sniffer that prints whatever complete \
                                                  lines being sent into serial buffer.', \
                                     epilog='example: to sniff 10,000 lines of data and store them into a csv file \
                                             with title "SYNC-TIME":  \
                                             python sniff.py -t "SYNC-TIME" -i 10000 > dataout.csv')
    # add expected arguments
    parser.add_argument('-t', '--title', dest='title', help='First line to be printed. \
                        This could be useful when concating output into a csv file.')
    parser.add_argument('-p', '--port', dest='port', help='Specify serial prot. default = "/dev/ttyACM0"')
    parser.add_argument('-b', '--baud', dest='baud', help='Baud rate used for communication. \
                        default = 115200 bps')
    parser.add_argument('-i', '--iter', dest='iter', help='Total number of lines to be printed. \
                        Will print out message endlessly until received keyboard termination signal, \
                        if this argument is not specified.')
    parser.add_argument('-s', action='store_true', help='Generate timestamps')
 
    # parse args
    args = parser.parse_args()

    if args.port:
        strPort = args.port
    else:
        strPort = '/dev/ttyACM0'

    if args.baud:
        baudRate = args.baud
    else:
        baudRate = 9600
        
    if args.iter:
        maxiter = int(args.iter)
    else:
        maxiter = 1 # any integer larger than 0
 
    if args.title:
        print(args.title)
    else:
        print('reading from serial port %s at %s bps...' % (strPort, baudRate) )
 
    # plot parameters
    sniff = Sniff(strPort, baudRate)

    # sniff sertial traffic
    iter = 0
    while (sniff.read(iter, args.s) and (iter < maxiter)):
        if (args.iter):
            iter += 1

    sniff.close()
  
# call main
if __name__ == '__main__':
    main()
