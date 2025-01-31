import asyncio
import websockets
import psutil
import json
import datetime
import os
import platform

def shutdown_computer():
    current_os = platform.system()

    if current_os == "Windows":
        os.system("shutdown /s /t 1")
    elif current_os == "Linux" or current_os == "Darwin":
        os.system("sudo shutdown now")
    else:
        print("Unsupported OS")


def is_system_process(proc):
    try:
        process_user = proc.username()

        if process_user in ['root', 'SYSTEM']:
            return True
        
        if proc.status() in [psutil.STATUS_IDLE, psutil.STATUS_ZOMBIE]:
            return True

    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return True

    return False

# Отримання списку процесів
def get_process_list():
    processes = [{"id": p.pid, "name": p.name()} for p in psutil.process_iter() if not is_system_process(p)]
    return processes

# Завершення процесу за PID
def terminate_process(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()
        process.wait(timeout=3)
        print(f"Process {pid} has been terminated.")
        return 'success'
    except psutil.NoSuchProcess:
        print(f"No process found with PID {pid}.")
        return 'fail'
    except psutil.AccessDenied:
        print(f"Access denied to terminate process with PID {pid}.")
        return 'fail'
    except psutil.TimeoutExpired:
        print(f"Process {pid} did not terminate within the timeout period.")
        return 'fail'

# Відправлення повідомлення через WebSocket
async def send_message(websocket, socketEvent):
    print(socketEvent)
    response = json.dumps(socketEvent) 
    await websocket.send(response)
    print("Sent message to server.")

# Основна функція для прослуховування серверу WebSocket
async def listen_to_server():
    uri = "wss://pc-checker-be.onrender.com/ws"
    
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket server.")

        await websocket.send(json.dumps({ "event": 'join', "clientId": 'pc' }))

        while True:
            print('sdfdsfs')
            message = json.loads(await websocket.recv())
            print(f"Received message: {message}")
            

            if message.get("event") == "getProcess":
                process_list = get_process_list()
                
                print('here')
                
                socketEvent = {
                    "event": "process",
                    "client": "pc",
                    "process": process_list,
                }
                await send_message(websocket=websocket, socketEvent=socketEvent)
                
            elif message.get("event") == "getStatus":
                boot_time_timestamp = psutil.boot_time()
                boot_time = datetime.datetime.fromtimestamp(boot_time_timestamp).strftime("%Y-%m-%d %H:%M:%S")
                
                socketEvent = {
                    "event": "status",
                    "client": "pc",
                    "status": boot_time,
                }
                await send_message(websocket=websocket, socketEvent=socketEvent)
                
            elif message.get("event") == "terminateProcess":
                socketEvent = {
                    "event": "status",
                    "client": "pc",
                }
                if "pid" in message: 
                    pid = message["pid"]
                    status = terminate_process(pid)
                    if status == 'success' : 
                        process_list = get_process_list()
                        socketEvent["event"] = 'event'
                        socketEvent["process"] = 'process_list'
                    else: 
                        socketEvent["status"] = status
                else:
                    socketEvent["status"] = 'fail'
                
                await send_message(websocket=websocket, socketEvent=socketEvent)
                
            elif message.get("event") == "turnOff":
                shutdown_computer()
                socketEvent = {
                    "event": "turnOff",
                    "client": "pc",
                    "status": 'off',
                }
                await send_message(websocket=websocket, socketEvent=socketEvent)

# Запуск програми
async def main():
    await listen_to_server()

if __name__ == "__main__":
    asyncio.run(main())
