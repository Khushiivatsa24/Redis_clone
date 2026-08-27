from resp import parse_command, encode_simple_string, encode_bulk_string

import socket
import threading

def handle_client(conn, store, lock):
    reader = conn.makefile("rb")


    while True:
        args = parse_command(reader)
        if args is None:
            break
        command = args[0].upper()

        if command == "PING":
          reply = encode_simple_string("PONG")
          conn.sendall(reply)
        elif command == "ECHO":
          reply = encode_bulk_string(args[1])
          conn.sendall(reply)
        
        
        elif command == "SET":
            key = args[1]
            value = args[2]
            reply = encode_simple_string("OK")
            with lock:
                store[key] = value
            conn.sendall(reply)
        
        elif command == "GET":
            key = args[1]
            with lock:
                value = store.get(key)
            reply = encode_bulk_string(value)
            conn.sendall(reply)
    conn.close() 

def main():
    server_socket = socket.create_server(("localhost", 6380), reuse_port=True)
    print("Listening on port 6380")
    store = {}
    lock = threading.Lock()
    while True:
        conn, addr = server_socket.accept() # blocks until a client connects
        thread = threading.Thread(target=handle_client, args=(conn, store, lock))
        thread.start()

       
        # for now, just accept and close


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down")
    