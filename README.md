To use this for an engagement, 
- create an engagement poetry project, 
- clone this repository next to the engagement project folder and
- add the cloned repo as dependency. 

This boils down to:
```
poetry new engagement
git clone git@github.geo.conti.de:uig55702/web-toolkit.git
cd engagement
poetry add --editable ../web-toolkit
```

Now you can use the `web-toolkit`, make changes to it and eventually commit them back. 

To create a request to google.com you may do:
```
from web import Request, RequestParameter

class InitialRequest(Request):
    """
    GET / HTTP/1.1
    Host: google.com
    Sec-Ch-Ua: "Not/A)Brand";v="8", "Chromium";v="126"
    Sec-Ch-Ua-Mobile: ?0
    Sec-Ch-Ua-Platform: "Windows"
    Accept-Language: de-DE
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
    Sec-Fetch-Site: none
    Sec-Fetch-Mode: navigate
    Sec-Fetch-User: ?1
    Sec-Fetch-Dest: document
    Accept-Encoding: gzip, deflate, br
    Priority: u=0, i
    Connection: keep-alive
    """
```