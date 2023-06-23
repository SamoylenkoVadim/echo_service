## Examples

<details>
  <summary><span style="font-size: 21px; font-weight: bold;">List endpoints</span></summary>
  <markdown>

<span style="font-size: 16px; font-weight: bold;">Request</span>
```commandline
    GET /endpoints HTTP/1.1
    Accept: application/vnd.api+json
```

<span style="font-size: 16px; font-weight: bold;">Expected response</span>

```commandline
    HTTP/1.1 200 OK
    Content-Type: application/vnd.api+json

    {
        "data": [
            {
                "type": "endpoints",
                "id": "12345",
                "attributes": [
                    "verb": "GET",
                    "path": "/greeting",
                    "response": {
                      "code": 200,
                      "headers": {},
                      "body": "\"{ \"message\": \"Hello, world\" }\""
                    }
                ]
            }
        ]
    }
```

  </markdown>
</details>

<details>
  <summary><span style="font-size: 21px; font-weight: bold;">Create endpoint</span></summary>
  <markdown>

<span style="font-size: 16px; font-weight: bold;">Request</span>
```commandline
    POST /endpoints HTTP/1.1
    Content-Type: application/vnd.api+json
    Accept: application/vnd.api+json

    {
        "data": {
            "type": "endpoints",
            "attributes": {
                "verb": "GET",
                "path": "/greeting",
                "response": {
                  "code": 200,
                  "headers": {},
                  "body": "\"{ \"message\": \"Hello, world\" }\""
                }
            }
        }
    }
```


<span style="font-size: 16px; font-weight: bold;">Expected response</span>
```commandline
    HTTP/1.1 201 Created
    Location: http://example.com/greeting
    Content-Type: application/vnd.api+json

    {
        "data": {
            "type": "endpoints",
            "id": "12345",
            "attributes": {
                "verb": "GET",
                "path": "/greeting",
                "response": {
                  "code": 200,
                  "headers": {},
                  "body": "\"{ \"message\": \"Hello, world\" }\""
                }
            }
        }
    }
```

  </markdown>
</details>

<details>
  <summary><span style="font-size: 21px; font-weight: bold;">Update endpoint</span></summary>
  <markdown>

<span style="font-size: 16px; font-weight: bold;">Request</span>
```commandline
    PATCH /endpoints/12345 HTTP/1.1
    Content-Type: application/vnd.api+json
    Accept: application/vnd.api+json

    {
        "data": {
            "type": "endpoints",
            "id": "12345"
            "attributes": {
                "verb": "POST",
                "path": "/greeting",
                "response": {
                  "code": 201,
                  "headers": {},
                  "body": "\"{ \"message\": \"Hello, everyone\" }\""
                }
            }
        }
    }
```


<span style="font-size: 16px; font-weight: bold;">Expected response</span>
```commandline
    HTTP/1.1 200 OK
    Content-Type: application/vnd.api+json

    {
        "data": {
            "type": "endpoints",
            "id": "12345",
            "attributes": {
                "verb": "POST",
                "path": "/greeting",
                "response": {
                  "code": 201,
                  "headers": {},
                  "body": "\"{ \"message\": \"Hello, everyone\" }\""
                }
            }
        }
    }
```

  </markdown>
</details>

<details>
  <summary><span style="font-size: 21px; font-weight: bold;">Delete endpoint</span></summary>
  <markdown>

<span style="font-size: 16px; font-weight: bold;">Request</span>
```commandline
    DELETE /endpoints/12345 HTTP/1.1
    Accept: application/vnd.api+json
```

<span style="font-size: 16px; font-weight: bold;">Expected response</span>
```commandline
    HTTP/1.1 204 No Content
```

  </markdown>
</details>

<details>
  <summary><span style="font-size: 21px; font-weight: bold;">Error response</span></summary>
  <markdown>

In case client makes unexpected response or server encountered an internal problem, Echo should provide proper error response.<br/>

<span style="font-size: 16px; font-weight: bold;">Request</span>
```commandline
    DELETE /endpoints/1234567890 HTTP/1.1
    Accept: application/vnd.api+json
```

<span style="font-size: 16px; font-weight: bold;">Expected response</span>

```commandline
    HTTP/1.1 404 Not found
    Content-Type: application/vnd.api+json

    {
        "errors": [
            {
                "code": "not_found",
                "detail": "Requested Endpoint with ID `1234567890` does not exist"
            }
        ]
    }
```

  </markdown>
</details>
