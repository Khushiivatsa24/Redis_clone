from resp import parse_command, encode_simple_string, encode_bulk_string, encode_error

import socket
import threading
import time

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
            expiry = None

            if len(args) > 3:
                if args[3].upper() == "PX":
                   ms = int(args[4])
                   expiry = time.time() + (ms / 1000)
                else:
                   reply = encode_error(f"unsupported option {args[3]}")
                   conn.sendall(reply)
                   continue
            
            with lock:
                store[key] = (value, expiry)

            reply = encode_simple_string("OK")
            conn.sendall(reply)
        
        elif command == "GET":
            key = args[1]
            if store.get(key) is None:
                reply = encode_bulk_string(None)
            else:
                value, expiry = store[key]

                if expiry is not None and time.time() > expiry:
                    with lock:
                        del store[key]
                    reply = encode_bulk_string(None)
                else:
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
    