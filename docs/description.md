The purpose of Echo is to serve ephemeral/mock endpoints created with parameters specified by clients.

## Technical specification

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

The Echo service works as follows:

* The server MUST implement `GET /endpoints` endpoint to return a list of mock endpoints created by clients (using `POST /endpoints` endpoint) or an empty array if no mock endpoints are defined yet.
  * The server MUST implement `POST /endpoints` endpoint to create a mock endpoint according to data from the payload. The server SHOULD validate received data.
  * The server MUST implement `PATCH /endpoints{/:id}` endpoint to updates the existing mock endpoint according to data from the payload. The server SHOULD NOT accept invalid data or update non-existing mock endpoints. If requested mock endpoint doesn't exist, the server MUST respond with `404 Not found`.
  * The server MUST implement `DELETE /endpoints{/:id}` endpoint to delete the requested mock endpoint. If requested mock endpoint doesn't exist, the server MUST respond with `404 Not found`.
  * The server MUST serve all mock endpoints as defined by clients. Mock endpoints MUST be available over HTTP. Example: if there is a mock endpoint `POST /foo/bar/baz`, it MUST be available only for `POST` requests at `/foo/bar/baz` path. It SHALL NOT be available via `GET /foo/bar/baz` or even `POST /foo/bar` because these are different endpoints. Basically Echo works like "what you define is what you get".
  * It's RECOMMENDED to validate incoming requests as might contain invalid data.
  * The server MAY implement authentication for `/endpoints`.
  * You MAY implement additional functionality if you have time or will to show your skills.

The server operates on _Endpoint_ entities:

    Endpoint {
      id    String
      verb  String
      path  String

      response {
        code    Integer
        headers Hash<String, String>
        body    String
      }
    }

  * `id` (required), a string value that uniquely identifies an Endpoint
    * `verb` (required), a string value that may take one of HTTP method names. See [RFC 7231](https://tools.ietf.org/html/rfc7231#section-4.3)
    * `path` (required), a string value of the path part of URL
    * `response` (required), an object with following attributes:
      * `code` (required), an integer status code returned by Endpoint
      * `headers` (optional), a key-value structure where keys represent HTTP header
      names and values hold actual values of these headers returned by Endpoint
      * `body` (optional), a string representation of response body returned by
      Endpoint
