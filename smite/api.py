import requests, hashlib, json, threading, time
from datetime import datetime

class SmiteAPI:
    # Default values
    DEFAULT_BASE_URL = "http://api.smitegame.com/smiteapi.svc"
    DEFAULT_RESPONSE_TYPE = "Json"
    DEFAULT_PLATFORM = "pc"
    DEFAULT_LANGUAGE = 1
    DEFAULT_ENCODING = "UTF-8"
    DEFAULT_UTC_FORMAT = "%Y%m%d%H%M%S"

    # Session method values
    CREATE_SESSION_METHOD = "createsession"
    CREATE_SESSION_FIELD = "session_id"
    CREATE_SESSION_DELAY = 900

    def __init__(self, dev_id, auth_key, base_url=DEFAULT_BASE_URL, response_type=DEFAULT_RESPONSE_TYPE, platform=DEFAULT_PLATFORM, language=DEFAULT_LANGUAGE):
        self.dev_id = dev_id
        self.auth_key = auth_key
        self.base_url = base_url
        self.response_type = response_type
        self.platform = platform
        self.language = language
        self.__session_token = None
        self.__session_thread = None

    def __threaded_get_session_token(self, delay):
        while True:
            self.get_session_token()
            time.sleep(delay)

    def __get_utc_date(self):
        """Return a UTC date string"""

        return datetime.utcnow().strftime(SmiteAPI.DEFAULT_UTC_FORMAT)

    def __create_signature(self, method):
        """Return a MD5 string signature

        Create a Smite API signature based on keys and
        called API method
        """

        signature = f"{self.dev_id}{method}{self.auth_key}{self.__get_utc_date()}"
        return hashlib.md5(signature.encode(SmiteAPI.DEFAULT_ENCODING)).hexdigest()

    def __create_endpoint(self, method, params=[]):
        """Return a built endpoint URL for the smite API"""

        params_string = f"/{'/'.join(params)}/" if len(params) > 0 else "/"
        signature = self.__create_signature(method)
        endpoint = f"{self.base_url}/{method}{self.response_type}/{self.dev_id}/{signature}/{self.__session_token}/{self.__get_utc_date()}{params_string}{self.language}"
        return endpoint

    def get_session_token(self):
        """Return and stores a session token
        
        Those tokens are valid for 15 minutes
        """

        signature = self.__create_signature(SmiteAPI.CREATE_SESSION_METHOD)
        endpoint = f"{self.base_url}/{SmiteAPI.CREATE_SESSION_METHOD}{self.response_type}/{self.dev_id}/{signature}/{self.__get_utc_date()}"
        res = requests.get(endpoint)
        json_body = json.loads(res.content.decode(SmiteAPI.DEFAULT_ENCODING))
        self.__session_token = json_body[SmiteAPI.CREATE_SESSION_FIELD]
        return json_body[SmiteAPI.CREATE_SESSION_FIELD]

    def create_session_token_thread(self, delay=CREATE_SESSION_DELAY):
        """Creates a thread to retrieve a valid session token every <delay> seconds"""

        if self.__session_thread == None:
            thread = threading.Thread(target=self.__threaded_get_session_token, args=(delay,))
            thread.daemon = True
            self.__session_thread = thread
            thread.start()

    def call_generic_method(self, method, params=[], raw=False):
        """Return a Smite API response as string
        
        Calls the specified method and returns
        its response
        """

        if self.__session_token == None:
            # Attempt to get session token first
            self.get_session_token()

        res = requests.get(self.__create_endpoint(method, params))
        data = res.content.decode(SmiteAPI.DEFAULT_ENCODING)
        if not raw:
            data = json.loads(data)
        return data

if __name__ == "__main__":
    pass