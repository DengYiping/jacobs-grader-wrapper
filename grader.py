import requests as r
import urllib.parse as parse

class GraderRequester:
    GRADER_ROOT_URL = 'https://grader.eecs.jacobs-university.de/'
    GRADER_LOGIN_URL = GRADER_ROOT_URL + 'login.php'
    GRADER_INDEX_URL = GRADER_ROOT_URL + 'index.php'

    def __init__(self, username, password):
        """
        A module to help you make request on grader system from Jacobs University Bremen
        Parameter: username: str, password: str
        Return: None
        """
        self.username = username
        self.password = password
        self.session = r.Session()

    def login(self):
        """
        Login into grader system.
        Parameter: None
        Return: Boolean (if successfull, return True)
        """
        self.session.get(self.GRADER_LOGIN_URL)
        post_form = {'username': self.username, 'pass': self.password, 'login': 'Sign in',}
        post_encoded = parse.urlencode(post_form)
        #build and encode the form body
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Referer': self.GRADER_LOGIN_URL,}
        # add headers
        login_result = self.session.post(self.GRADER_LOGIN_URL, data = post_encoded, headers = headers)
        if login_result.url == self.GRADER_INDEX_URL:
            return True
        else:
            return False

    @property
    def get(self):
        return self.session.get

    @property
    def post(self):
        return self.session.post
