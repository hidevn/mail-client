import socket, select, string, sys, getpass, time, ssl, quopri, email
from email.parser import Parser
parser = Parser()


username = 'recent:tuansut1997@gmail.com'
password = 'mot2345sau'
host = "pop.gmail.com"
port = 995
# username = 'tuanpa292'
# password = 'Dr@gon01'
# host = 'pop3.viettel.com.vn'
# port = 995
secured = True
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ECDHE-RSA-AES128-GCM-SHA256
# RC4-SHA
if secured:
    s = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv23, ciphers="ECDHE-RSA-AES128-GCM-SHA256")
else:
    s = sock

def quickOut2(msg):
    socket_list = [s]
    msg = msg + '\n'
    s.sendall(msg.encode('utf-8'))
    read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
    # data = recv_timeout(s)
    data = recv_timeout(s)
    if not data:
        print('Connection closed')
        sys.exit()
    else:
        try:
            print(quopri.decodestring(data).decode('utf-8'))
            return quopri.decodestring(data).decode('utf-8')   
        except:
            print(data)
            return data   

def quickOut(msg):
    socket_list = [s]
    msg = msg + '\n'
    s.sendall(msg.encode('utf-8'))
    read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
    # data = recv_timeout(s)
    data = recvall(s, 19536)
    rst = parser.parsestr(data)
    print('#######################33')
    print(rst)
    print('#######################33')
    if not data:
        print('Connection closed')
        sys.exit()
    else:
        try:
            print(quopri.decodestring(data).decode('utf-8'))
            return quopri.decodestring(data).decode('utf-8')   
        except:
            # print(data)
            return data             
                
def login(username, password):
    quickOut2('USER ' + username)
    quickOut2('PASS ' + password)

def numberOfMails():
    return quickOut2('STAT').split()[1]

def recvall(sock, maxLength):
    sock = [sock]
    count = 0
    BUFF_SIZE = 4096 # 4 KiB
    data = ""
    size = 0
    while True:
        count = count + 1
        print(count)
        sock, write_sockets, error_sockets = select.select(sock , [], [])
        part = sock[0].recv(BUFF_SIZE)
        data += part.decode('utf-8')
        size += sys.getsizeof(part)
        if size > maxLength:
            break
        print(sys.getsizeof(part))
    return data

def recv_timeout(the_socket,timeout=0.2):
    the_socket.setblocking(0)
    total_data=[]
    data=''
    begin=time.time()
    while 1:
        if total_data and time.time()-begin > timeout:
            break
        elif time.time()-begin > timeout*2:
            break
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)
                begin=time.time()
            else:
                time.sleep(0.1)
        except:
            pass
    return ''.join([bytes.decode('utf-8') for bytes in total_data])

class Mail:

    def __init__(self, i):
        self.__headers = {}
        self.__body = ""
        self.getMail(i)
    
    def getMail(self, index):
        response = quickOut('retr ' + str(index))
        response = str(response).split('\n')
        for i in range(1, len(response)-1):
            if not response[i].startswith('\t') and not response[i].startswith('\r') and not response[i].startswith(' '):
                line = response[i].split(':', 1)
                if len(line) > 1:
                    try:
                        self.__headers[line[0]] += '\n' + line[1].strip()
                    except:
                        self.__headers[line[0]] = line[1].strip()
                    currentHeaderName = line[0]
                else:
                    self.__headers[currentHeaderName]+=line[0]
            elif response[i] == '\r':
                break
            elif response[i].startswith('\t'):
                self.__headers[currentHeaderName]+=response[i].replace('\t',' ')
            else:
                self.__headers[currentHeaderName]+=response[i]
        for j in range(i+1, len(response)-1):
            self.__body = self.__body + response[j].replace('\r','\n')

    def getHeaders(self):
        return self.__headers

    def getBody(self):
        return self.__body

if __name__ == "__main__":
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((host, port))
    except Exception as e: 
        print('Unable to connect')
        print(e)
        sys.exit()
    print('Connected')
    data = s.recv(4096)
    login(username, password)
    mail = Mail(30)
    for k, v in mail.getHeaders().items():
        print('%s : %s'%(k, v))
    print('------------')
    # with open('out.txt', 'a') as out:
    #     out.write(mail.getBody())
    # print(mail.getHeaders()['Received'])