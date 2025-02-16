from webtoolkit.base import Request, LambdaArgument, Session, JsonBodyValue, GetParameter, FormParameter, CookieArgument, XmlBodyValue

class ExampleRequest(Request):
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

    class Response(Request.Response):
        
        @property
        def location(self):
            return self.headers["Location"]

def main():
    q0 = ExampleRequest()
    r0 = q0.send()

    print(q0)
    print(r0)

    print(r0.location)
    

if __name__ == "__main__":
    main()