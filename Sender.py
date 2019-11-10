import sys
import getopt

import Checksum
import BasicSender

'''
This is a skeleton sender class. Create a fantastic transport protocol here.
'''
class Sender(BasicSender.BasicSender):
    def __init__(self, dest, port, filename, debug=False, sackMode=False):
        super(Sender, self).__init__(dest, port, filename, debug)
        self.sackMode = sackMode
        self.debug = debug

    def handshake(self):
        for i in range (0 , 20):
            self.send(self.make_packet('syn' , 0 , ''))
            ans = self.receive(1)
            if ans is None: continue
            return True
        return False

    # Main sending loop.
    def start(self):
        sz = 300
        b = self.handshake()
        # print(b)
        if not b: return
        data = self.infile.read()
        chunks = []
        chunks.append(b"das")
        for i in range(0 , len(data) , sz):
            chunks.append(data[i :min(i + sz , len(data))])
        # print(chunks)
        to_send = {}
        for i in range(1 , min(8 , len(chunks))):
            to_send[i] = chunks[i]
        index = 1
        while True:
            if len(to_send) == 0: break
            for ind in to_send.keys():
                self.send(self.make_packet('dat' , ind , to_send[ind]))
            answers = []
            while True:
                ans = self.receive(0.5)
                if ans is None: break
                if Checksum.validate_checksum(ans):
                    answers.append(ans)

            c = 0
            for elem in answers:
                msg_type, seqno, data, _ = self.split_packet(elem)
                if(msg_type == 'ack' and seqno == index):c+=1
            if(c >= 4):
                to_send.clear()
                to_send[index] = chunks[index]
                continue
            
            for elem in answers:
                msg_type, seqno_str, data, _ = self.split_packet(elem)
                if(msg_type == 'ack' ): 
                    seqno = int(seqno_str)
                    index = max(index , seqno)   
                if(msg_type == 'sack') :
                    pieces = elem.split('|')        
                    index = max(index , int(pieces[1].split(';')[0]))   
                    ls = pieces[1].split(';')[1].split(',')
                    for ind in ls:
                        if(ind == ''): continue
                        if(int(ind) in to_send.keys()) :del to_send[int(ind)]                
                   
            to_send.clear()
            for i in range(index , min(index + 7 , len(chunks))):
                to_send[i] = chunks[i]
        
        self.send(self.make_packet('fin' , index , ''))
        pass
        
        
'''
This will be run if you run this script from the command line. You should not
change any of this; the grader may rely on the behavior here to test your
submission.
'''
if __name__ == "__main__":
    def usage():
        print "BEARS-TP Sender"
        print "-f FILE | --file=FILE The file to transfer; if empty reads from STDIN"
        print "-p PORT | --port=PORT The destination port, defaults to 33122"
        print "-a ADDRESS | --address=ADDRESS The receiver address or hostname, defaults to localhost"
        print "-d | --debug Print debug messages"
        print "-h | --help Print this usage message"
        print "-k | --sack Enable selective acknowledgement mode"

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                               "f:p:a:dk", ["file=", "port=", "address=", "debug=", "sack="])
    except:
        usage()
        exit()

    port = 33122
    dest = "localhost"
    filename = None
    debug = False
    sackMode = False

    for o,a in opts:
        if o in ("-f", "--file="):
            filename = a
        elif o in ("-p", "--port="):
            port = int(a)
        elif o in ("-a", "--address="):
            dest = a
        elif o in ("-d", "--debug="):
            debug = True
        elif o in ("-k", "--sack="):
            sackMode = True

    s = Sender(dest,port,filename,debug, sackMode)
    try:
        s.start()
    except (KeyboardInterrupt, SystemExit):
        exit()




# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py
# python TestHarness.py -s Sender.py -r Receiver.py