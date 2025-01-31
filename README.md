# PC Checker WebSocket Client

This Python script connects to a WebSocket server to provide system monitoring and control functionalities. It allows the server to:

1. Retrieve the list of running processes
2. Terminate specific processes by PID
3. Check the system's boot time
4. Shut down the computer

## Features
- WebSocket communication with a remote server
- Process management using `psutil`
- System shutdown based on operating system
- JSON message handling for WebSocket events

## Prerequisites
- Python 3.7+
- `psutil` library
- `websockets` library

Install the required libraries:
```bash
pip install psutil websockets
```

## Usage
To run the script, execute:
```bash
python script_name.py
```
Replace `script_name.py` with the actual name of the script file.

## WebSocket Events
- getProcess: Returns a list of non-system processes.
- getStatus: Sends the system's boot time.
- terminateProcess: Terminates a process by its PID.
- turnOff: Shuts down the computer.

## Important Functions
- `get_process_list()`: Fetches a list of running processes excluding system processes.
- `terminate_process(pid)`: Terminates a process given its PID.
- `shutdown_computer()`: Shuts down the computer based on OS.


