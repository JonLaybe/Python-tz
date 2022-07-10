import socket
import threading

host = ''
port = 1300
clients = []#list clients

class User:#User(client)
	def __init__(self, conn, addr):
		self.conn = conn
		self.addr = addr
class TimeDate:#Time
	def __init__(self):
		self.number = ''
		self.id = ''
		self.hour = ''
		self.minutes = ''
		self.seconds = ''
		self.zhq = ''
		self.grop = ''
class ListLog:#Log
	def __init__(self):
		self.file = open('logs.txt', 'a')
	def Push(self, log):
		self.file.write(log+'\n')
	def __del__(self):
		self.file.close()

def MessageParcer(message, date_time):#Parcer message
	if (len(message) == 24 and len(message.split()) == 4):
		message = message.split()
		if (message[0].isdigit() and len(message[1]) == 2 and len(message[2]) == 12 and message[3].isdigit()):
			if (message[2][2] == ':' and message[2][5] == ':' and message[2][8] == '.'):
				if (message[2][:2].isdigit() and message[2][3:5].isdigit() and message[2][6:8].isdigit() and message[2][9:].isdigit()):
					if (0 <= int(message[2][:2]) < 60 and
						0 <= int(message[2][3:5]) < 60 and
						0 <= int(message[2][6:8]) < 60 and
						0 <= int(message[2][9:]) < 1000):
						date_time.number = message[0]
						date_time.id = message[1]
						date_time.hour = message[2][:2]
						date_time.minutes = message[2][3:5]
						date_time.seconds = message[2][6:8]
						date_time.zhq = message[2][9:]
						date_time.grop = message[3]
						return True
		return False

def ListenClient(client):#listening on this client
	try:
		while (True):
			date_time = TimeDate()
			data = client.conn.recv(1000).decode('utf-8')
			if (MessageParcer(data, date_time)):
				message = f'спортсмен, нагрудный номер {date_time.number} прошёл отсечку {date_time.id} в "{date_time.hour}:{date_time.minutes}:{date_time.seconds}"'
				if(date_time.grop == '00'):
					for i in clients:
						SendMassage(message, i)
					print(message)
				ListLog().Push(f'спортсмен, нагрудный номер {date_time.number} прошёл отсечку {date_time.id} в "{date_time.hour}:{date_time.minutes}:{date_time.seconds}.{date_time.zhq}"')
	except ConnectionResetError:
		clients.remove(client)
	except ConnectionAbortedError:
		clients.remove(client)

def SendMassage(message, client):#sending a message
	message = message.encode('utf-8')
	client.conn.send(message)

def Wait(host):#waiting for user connection
	while (True):
		print("[server]Connection")
		conn, addr = host.accept()
		client = User(conn, addr)
		clients.append(client)
		print("[server]Accept")
		threading.Thread(target = ListenClient, args = (client,)).start()

def StartServer(host, port):#StartServer
	tcp_host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_host.bind((host, port))
	tcp_host.listen(100)
	Wait(tcp_host)

StartServer(host, port)