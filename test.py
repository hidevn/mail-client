import socket, select, string, sys, getpass, time, ssl

username = 'tuanpa292'
password = 'Dr@gon01'
host = "pop3.viettel.com.vn"
port = 995
secured = True
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if secured:
    s = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv23, ciphers="RC4-SHA")
else:
    s = sock

def quickOut(msg):
    socket_list = [s]
    s.send(msg+'\n')
    read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
    data = recv_timeout(s)
    if not data :
        print 'Connection closed'
        sys.exit()
    else:
        print msg
        print data.decode('utf-8')
        return str(data).strip()          
                
def login(username, password):
    quickOut('USER ' + username)
    quickOut('PASS ' + password)

def numberOfMails():
    return quickOut('STAT').split()[1]

def recv_timeout(the_socket,timeout=0.1):
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
    return ''.join(total_data)

class Mail:
    def __init__(self):
        self.__headers = {}
        self.__body = ""
        
    def __init__(self, i):
        self.__headers = {}
        self.__body = ""
        self.getMail(i)
    
    def getMail(self, index):
        response = quickOut('retr ' + str(index))
        response = str(response).split('\n')
        print response
        for i in range(1, len(response)-1):
            if not response[i].startswith('\t') and not response[i].startswith('\r'):
                line = response[i].split(':')
                self.__headers[line[0]] = line[1].strip()
            elif response[i] == '\r':
                break
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
        print 'Unable to connect'
        print e
        sys.exit()
    print 'Connected'
    data = s.recv(4096)
    login(username, password)
    mail = Mail(1)
    # print mail.getHeaders()['From']
    # print numberOfMails()