import socket
import json
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8192        # The port used by the server

def json_message():
    local_ip = socket.gethostbyname(socket.gethostname())
    data = {
        'rfw_id':12345,
		'benchmark_type' :"DVD-training",
		'workload_metric':"NetworkIn_Average",
		'batch_unit':2,
		'batch_id':1,
		'batch_size':1
    }

    json_data = json.dumps(data, sort_keys=False, indent=6)
    print("data %s" % json_data)

    send_message(json_data + ";")

    return json_data
def send_message(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(data.encode())
        data = s.recv(1024)
        json_data=json.loads(data)
		
    print(json_data)

json_message()