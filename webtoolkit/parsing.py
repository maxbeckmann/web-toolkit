from io import StringIO
import requests

def parse_http_request(byte_string):
    byte_string= byte_string.lstrip()
    # Use a BytesIO object to mimic a file for reading lines
    request_io = StringIO(byte_string)

    # Read the request line
    request_line = request_io.readline().strip()
    method, path, http_version = request_line.split()

    # Read headers
    headers = dict()
    raw_header_line = request_io.readline()
    while raw_header_line:
        try:
            key, value = raw_header_line.split(":", 1)
            key = key.strip()
            value = value.strip()
            headers[key] = value
            raw_header_line = request_io.readline()
        except ValueError:
            print("Failed to parse headers. Did you remember to add an empty line at the end?")
            exit()

    # Read body if present
    body = request_io.read().strip()

    if body == "":
        body = None

    return method, path, headers, body

def strip_unnecessary_whitespace(request_str):
    result = ""
    request_str= request_str.lstrip()
    request_io = StringIO(request_str)
    for line in request_io.readlines():
        result += line.strip() + "\n"
    
    return result

def carve_string(text, before, after):
    start_split = text.split(before)[1]
    substring = start_split.split(after)[0]
    return substring

def format_head(response):
    formatted_response = []
    
    # Adding the status line (assuming HTTP/1.1)
    formatted_response.append(f"HTTP/1.1 {response.status_code} {response.reason}")

    # Adding headers
    for key, value in response.headers.items():
        formatted_response.append(f"{key}: {value}")
    
    return formatted_response

def format_response(response):
    # Prepare the formatted response as a string
    formatted_response = []

    formatted_response += format_head(response)
    
    # Adding a blank line to separate headers from the body
    formatted_response.append("")
    
    # Adding the body of the response
    formatted_response.append(response.text)

    return formatted_response

def format_request(request):
    formatted_request = []
    
    # Adding request line
    formatted_request.append(f"{request.method} {request.url} HTTP/1.1")
    
    # Adding headers
    for key, value in request.headers.items():
        formatted_request.append(f"{key}: {value}")
    
    # Adding the request body if it exists
    if request.body:
        formatted_request.append("")
        formatted_request.append(request.body.decode() if isinstance(request.body, bytes) else request.body)
    
    return formatted_request