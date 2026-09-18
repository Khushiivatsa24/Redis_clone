import io
from resp import parse_command
from snapshot import save_snapshot, load_snapshot

fake_input = b"*2\r\n$3\r\nGET\r\n$3\r\nfoo\r\n"
reader = io.BytesIO(fake_input)

result = parse_command(reader)
print(result)

fake_store = {"foo": ["bar", None], "baz": ["qux", 1234567890.0]}

save_snapshot(fake_store)
restored = load_snapshot()

print(restored)
print(restored == fake_store)