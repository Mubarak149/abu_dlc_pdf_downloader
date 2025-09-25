from urllib.parse import urlparse, parse_qs
import urllib.parse

# Function to extract base_url and file_path from the full URL
def parse_pdf_url(pdf_url):
    # Parse the URL
    parsed_url = urlparse(pdf_url)
    
    # Extract the query parameters (file path is passed in the query string)
    query_params = parse_qs(parsed_url.query)
    
    # Extract the file path from the query parameters
    file_path = query_params.get('file', [None])[0]
    
    # Construct the base URL
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    return base_url, file_path


def convert_link(encoded_url):
    """
    Converts URL-encoded characters in a given link into their decoded format.
    
    Args:
        encoded_url (str): The original URL with encoded characters.
        
    Returns:
        str: The decoded URL.
    """
    # Decode the URL using urllib.parse
    decoded_url = urllib.parse.unquote(encoded_url)
    return decoded_url

