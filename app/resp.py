
def read_line(reader):
    """Read a line and strip the trailing \r
    n."""
    line = reader.readline()
    return line.rstrip(b"\r\n")

def parse_command(reader):
    first_line = reader.readline()
    first_line = first_line.rstrip(b"\r\n")
    

    if not first_line:
        return None
    num_pieces = int(first_line[1:])

    pieces = []
    for _ in range(num_pieces):
        len_line = reader.readline().rstrip(b"\r\n")
        piece_len = int(len_line[1:])

        piece_bytes = reader.read(piece_len)

        reader.read(2)

        pieces.append(piece_bytes.decode())
    
    return pieces

def encode_simple_string(s):
    return("+" + s + "\r\n").encode()



def encode_bulk_string(s):
    if s is None:
        return b"$-1\r\n"
    return(f"${len(s)}" + "\r\n" + s + "\r\n").encode()

def encode_error(msg):
    return f"-ERR {msg}\r\n".encode()