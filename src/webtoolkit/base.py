import requests
from .parsing import strip_unnecessary_whitespace, parse_http_request, carve_string, format_head, format_response, format_request
from .url_parsing import get_url_parameter

# for convenience, to avoid importing it separately
from requests import Session

class Request(requests.Request):
    def __init__(self, host=None, protocol="https", auth=None, **kwargs):
        if self.__doc__ is None:
            raise ValueError(f"Missing request template for {type(self).__name__}")
        
        template = strip_unnecessary_whitespace(self.__doc__)
        method, path, headers, body = parse_http_request(template)
        
        host = headers["Host"] if host is None else host
        url = f"{protocol}://{host}{path}"
        super().__init__(method=method, url=url, headers=headers, data=body, auth=auth)

        # update request arguments
        self.initialize_arguments(kwargs)

    def get_template_arguments(self):
        arguments = {
            name: argument_definition
            for cls in self.__class__.__mro__
                for name, argument_definition in cls.__dict__.items()
                    if Argument.is_argument_type(argument_definition)
        }
        return arguments

    def initialize_arguments(self, kwargs):
        self._template_arguments = self.get_template_arguments()
        
        for name, argument_definition in self._template_arguments.items():
            value = argument_definition.get_value(self, kwargs.get(name, None))
            setattr(self, name, value)
        
        for name in kwargs:
            if name not in self.__dict__:
                raise TypeError(f"{name} is not a valid argument for {type(self).__name__}")
    
    def __str__(self):
        req = self.prepare()
        self.apply_arguments(req)
        formatted_req = format_request(req)
        return "\n".join(formatted_req)
    
    def __repr__(self):
        class_name = self.__class__.__name__
        args = ', '.join(f"{name}={getattr(self, name)!r}" for name in self.get_template_arguments())
        return f"{class_name}({args})"

    def apply_arguments(self, request):
        # remove the Content-Length header so requests will caluclate the correct length
        request.headers.pop('Content-Length', None)

        for arg_name, arg in self._template_arguments.items():
            value = getattr(self, arg_name)
            arg.apply_value(request, value)


    def send(self, session=None, **kwargs):
        req = self.prepare()

        self.apply_arguments(req)

        resp = None
        if session is None:
            session = requests.Session()
        
        kwargs["allow_redirects"] = kwargs.get("allow_redirects", False) # override default behaviour to not follow redirects

        resp = session.send(req, **kwargs)
        
        # make the result the Request-specific Response type
        resp.__class__ = self.__class__.Response
        return resp
    
    # Request-specific response type to define HTTP-Transaction specific response parsing
    class Response(requests.Response):
            
            def get_template_arguments(self):
                arguments = {
                    name: argument_definition
                    for cls in self.__class__.__mro__
                        for name, argument_definition in cls.__dict__.items()
                            if Argument.is_argument_type(argument_definition)
                }
                return arguments
            
            def __getattribute__(self, name):
                # early exit to avoid recursion during building the template argument list
                attr = super().__getattribute__(name)
                if isinstance(attr, Argument):
                    template_arg: Argument = attr
                    value = template_arg.extract_response_value(self)
                    return value
                return attr
            
            def carve(self, before, after):
                return carve_string(self.text, before, after)
            
            def __str__(self) -> str:
                lines = format_response(self)
                # Join all parts into a single string with new lines
                return "\n".join(lines)
            
            def __repr__(self):
                class_name = self.__class__.__name__
                args = ', '.join(f"{name}={getattr(self, name)!r}" for name in self.get_template_arguments())
                return f"{class_name}({args})"
            
            @property
            def head(self) -> str:
                lines = format_head(self)
                return "\n".join(lines)

class Argument:
    @classmethod
    def is_argument_type(cls, obj):
        return isinstance(obj, cls)
    
    def get_value(self, request: Request, value=None):
        return value
    
    def apply_value(self, request: requests.PreparedRequest, value):
        raise NotImplementedError()

class Header(Argument):
    def __init__(self, name):
        self.name = name

    def get_value(self, request, value=None):
        if value:
            return value
        else:
            return request.headers[self.name]
    
    def extract_response_value(self, response):
        return response.headers[self.name]
    
    def apply_value(self, request: requests.PreparedRequest, value):
        request.headers[self.name] = value

class Bearer(Header):
    def __init__(self):
        super().__init__("Authorization")
    
    def extract_response_value(self, response):
        header: str = super().extract_response_value(response)
        splits = header.split()
        assert splits[0] == "Bearer"
        return splits[1]

    def apply_value(self, request, value):
        return super().apply_value(request, f"Bearer {value}")

from jsonpath_ng import parse
import json

class JsonBodyValue(Argument):
    def __init__(self, expression):
        super().__init__()
        self.expression = parse(expression)

    def get_value(self, request: Request, value=None):
        if value:
            return value
        else:
            data = json.loads(request.data)
            matches = self.expression.find(data)
            return matches[0].value
    
    def extract_response_value(self, response):
        data = response.json()
        matches = self.expression.find(data)
        return matches[0].value

    def apply_value(self, request: requests.PreparedRequest, value):
        data = json.loads(request.body)
        matches = self.expression.find(data)
        path = matches[0].path
        path.update(data, value)
        request.body = json.dumps(data)
        

from yarl import URL

class GetParameter(Argument):
    def __init__(self, name):
        self.name = name

    def get_value(self, request: Request, value=None):
        if value:
            return value
        else:
            return get_url_parameter(request.url, self.name)
    
    def apply_value(self, request: requests.PreparedRequest, value):
            url = URL(request.url)
            result = url.update_query(**{self.name: value})
            request.url = str(result)

from urllib.parse import parse_qs, urlencode

class FormParameter(Argument):
    def __init__(self, name):
        self.name = name
    
    def get_value(self, request: Request, value=None):
        if value:
            return value
        else:
            form_params = parse_qs(request.data)
            results = form_params[self.name]
            assert len(results) == 1, "everything else would be strange. Let's check to avoid making unjustified assumptions"
            return results[0]
    
    def apply_value(self, request: requests.PreparedRequest, value):
        form_params = parse_qs(request.body)
        form_params[self.name] = value
        updated_body = urlencode(form_params, doseq=True)
        request.body = updated_body

from requests.cookies import RequestsCookieJar
from http.cookies import SimpleCookie

class CookieArgument(Argument):
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    def get_value(self, request: Request, value=None):
        if value:
            return value
        else:
            return request.cookies[self.name]
    
    def apply_value(self, request: requests.PreparedRequest, value):
        existing_cookie_header = request.headers.get('Cookie', '')
        
        cookies = SimpleCookie(existing_cookie_header)
        cookies[self.name] = value
        
        cookie_strings = []
        for cookie_name, morsel in cookies.items():
            cookie_strings += [f"{cookie_name}={morsel.value}"]
        
        updated_cookie_header = "; ".join(cookie_strings)
        request.headers['Cookie'] = updated_cookie_header

from lxml import etree

class XmlBodyValue(Argument):
    def __init__(self, xpath_query):
        super().__init__()
        self.query = xpath_query

    def get_value(self, request: Request, value=None):
        if value:
            return value
        else:
            tree = etree.XML(request.data.encode())
            matches = tree.xpath(self.query)
            return matches[0].text
    
    def extract_response_value(self, response: requests.Response):
        data = response.text.encode()
        tree = etree.XML(data)
        matches = tree.xpath(self.query)
        return matches[0].text

    def apply_value(self, request: requests.PreparedRequest, value):
        data = request.body.encode()
        tree = etree.XML(data)
        matches = tree.xpath(self.query)
        matches[0].text = value
        request.body = etree.tostring(tree, encoding="utf-8", xml_declaration=True)

class LambdaArgument(Argument):
    def __init__(self, callable):
        super().__init__()
        self.callable = callable
    
    def get_value(self, request: Request, value=None):
        if value:
            return value
        else:
            return None
    
    def apply_value(self, request: requests.PreparedRequest, value):
        return self.callable(request, value)
    