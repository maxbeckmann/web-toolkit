from urllib.parse import urlparse, parse_qs

def get_url_parameter(url, parameter_name):
    # Parse the URL
    parsed_url = urlparse(url)
    # Parse the query parameters
    query_params = parse_qs(parsed_url.query)
    # Retrieve the specified parameter, return None if not found
    return query_params.get(parameter_name, [None])[0]