import socket
import sys

HOST = sys.argv[1]
PORT = 1337
number = 0 

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        if PORT == 9765:
            break
        NEWPORT = PORT
        request = "GET / HTTP/1.1\r\nHost:{}\r\n\r\n".format(HOST)
        s.send(request.encode())

        response = s.recv(4096)
        data = response.decode()
        print("=============================")
        if len(data) > 100 :
            print("Current PORT ", PORT) 
            index = data.index("GMT")
            res = data[index+5:].split()
            print(res)
            if res[0] == 'add':
                number += float(res[1]) 
            elif res[0] == 'minus':
                number -= float(res[1])
            elif res[0] == 'multiply':
                number = number * float(res[1])
            elif res[0] == 'divide':
                number = number / float(res[1])
            PORT = int(res[2]) # assign new PORT
        print("=============================")
    
        s.close()
        
    except KeyboardInterrupt: 
        print("Interrupting")
        raise
    except Exception as err:
        print(err)


print("RESULT ", number)