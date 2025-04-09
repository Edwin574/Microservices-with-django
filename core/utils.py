import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def retry_request(url, retries=3, backoff_factor=2):
    """
    Sends a GET request with retry logic.
    """
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=(500, 502, 504),  # HTTP status codes to retry
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    return session.get(url)