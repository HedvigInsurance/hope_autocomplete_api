# HOPE Autocomplete service

# Starting
 ```bash
> docker-compose up
``` 

# Add messages
```bash
 > curl -XPOST -H 'Content-type: application/json' -d @hope_replies.json  http://localhost:5000/v0/messages/
``` 

# Autocomplete query
```bash
 > curl http://localhost:5000/v0/messages/autocomplete?query=tac 2>/dev/null | jq

[
  {
    "score": 22.034869999999998,
    "text": "Tackar!"
  },
  {
    "score": 6.5813171666666666,
    "text": "Tackar för det!"
  },
  .
  .
  .
]

```
