class Response:
    def __init__(
        self, status_code: int, headers: dict, cookies: dict, text: str = None
    ):
        self.status_code = status_code
        self.response_headers = headers
        self.response_cookies = cookies
        self.text = text
