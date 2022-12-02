### Threebot Authenticator

referes to the threefold connect server. it is expected to listen on port 5000.

Run with this command:

```bash
 cd 3bot/ && uwsgi --socket 0.0.0.0:5000 --protocol=http -w app:app
```
