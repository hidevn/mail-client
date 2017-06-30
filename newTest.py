import socket, select, string, sys, getpass, time, ssl, quopri, email, email.header

username = 'recent:tuansut1997@gmail.com'
password = 'mot2345sau'
host = "pop.gmail.com"
port = 995
secured = True
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


if secured:
    s = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv23, ciphers="ECDHE-RSA-AES128-GCM-SHA256")
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
        return str(data).strip()
                
def login(username, password):
    quickOut('USER ' + username)
    quickOut('PASS ' + password)

def numberOfMails():
    return quickOut('STAT').split()[1]

def recv_timeout(the_socket,timeout=1):
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
    def __init__(self, i):
        response = quickOut('retr ' + str(i))
        response = response[response.find('\n'):].strip()
        self.mail = email.message_from_string(response)
        
    def getMail(self):
        mail = self.mail
        t = [mail]
        print "Mail duoc gui tu: " + str(mail['From'])
        print "Mail duoc gui den: " + str(mail['To'])
        while len(t) != 0:
            for content in t:
                t.remove(content)
                if isinstance(content.get_payload(), str):
                    print content.get_payload()
                else:
                    for payload in content.get_payload():
                        if payload.is_multipart():
                            t.append(payload)
                        else:
                            type=payload.get_content_type()
                            dispo = payload.get('Content-Disposition')
                            if 'attachment' in str(dispo):
                                try:
                                    open(payload.get_filename(),'wb').write(payload.get_payload(decode=True))
                                    print "Save attachment " + payload.get_filename() + " succeed! "
                                except:
                                    print "Failed to save attachment " + payload.get_filename()
                                
                            if type == 'text/plain' and 'attachment' not in str(dispo):
                                print payload.get_payload(decode=True)
                            if type == 'text/html':
                                # print payload.get_payload(decode=True)
                                try:
                                    open("Content.html",'wb').write(payload.get_payload(decode=True))
                                    print "Saved html content to file!"
                                except:
                                    print "Failed to save html content"
    def getSubject(self):
        mail = self.mail
        headers = email.header.decode_header(mail['Subject'])
        return ''.join([ unicode(t[0], t[1] or 'utf-8') for t in headers ])

def displayHeaders(currentPage, numOfMail):
    print "Dang tai, xin doi"
    resultString = ""
    if (currentPage + 1)*10 + 1 > numOfMail + 1:
        limit = numOfMail + 1
    else:
        limit = (currentPage + 1)*10 + 1
    for currentMail in range(currentPage*10 + 1, limit):
        currentMailList[currentMail%10 - 1] = Mail(currentMail)
        resultString += "%d : %s\n"%(currentMail,currentMailList[currentMail%10 - 1].getSubject())
    return resultString

def connect():
    s.settimeout(5)
    try:
        s.connect((host, port))
    except Exception as e: 
        print 'Unable to connect'
        print e
        sys.exit()
    data = s.recv(4096)
    login(username, password)

def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False

if __name__ == "__main__":
    connect()
    numOfMail = int(numberOfMails())
    print "Tong so mail hien co: %d"%(numOfMail)
    currentMailList = [None]*10
    currentPage = 0
    displayHeaders = displayHeaders(currentPage, numOfMail)
    while 1:
        print 'Trang %d/%d'%(currentPage + 1, numOfMail/10 + 1)
        print displayHeaders
        print 'Nhap tiep:'
        msg = sys.stdin.readline()
        num, isInt = intTryParse(msg)
        if isInt and num >= (currentPage)*10 + 1 and num <= numOfMail:
            currentMailList[num % 10 - 1].getMail()
        elif msg == 'N\n' or msg == 'n\n':
            if currentPage < numOfMail/10 + 1:
                currentPage += 1
                displayHeaders = displayHeaders(currentPage, numOfMail)
            else:
                print "Ban dang o trang cuoi"
        elif msg == 'P\n' or msg == 'p\n':
            if currentPage >0:
                currentPage -= 1
                displayHeaders = displayHeaders(currentPage, numOfMail)
            else:
                print "Ban dang o trang dau"
        elif msg == 'Q\n' or msg == 'q\n':
            print "Bye :D"
            s.close()
            sys.exit()
        else:
            print "Nhap sai!"


