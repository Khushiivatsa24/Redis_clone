import io
from resp import parse_command

fake_input = b"*2\r\n$3\r\nGET\r\n$3\r\nfoo\r\n"
reader = io.BytesIO(fake_input)

result = parse_command(reader)
print(result)