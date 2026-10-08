# redis-clone

Built my own Redis server from scratch in Python, to understand how networking works under the hood.

It speaks the real RESP protocol, so `redis-cli` and other real Redis clients can talk to it directly.

## What it can do

- `PING`
- `ECHO <message>`
- `SET <key> <value>` (with optional expiry — `PX <milliseconds>`)
- `GET <key>`
- `SAVE` — saves everything to disk
- Reloads saved data automatically when the server restarts
- Handles multiple clients at once (threading + locking)

## Run it

```bash
git clone https://github.com/Khushiivatsa24/<repo-name>.git
cd <repo-name>
python server.py
```

Then, in another terminal:

```bash
redis-cli -p 6380 PING
redis-cli -p 6380 SET foo bar
redis-cli -p 6380 GET foo
```



