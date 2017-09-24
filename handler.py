from grader import GraderRequester
from bs4 import BeautifulSoup

class GraderHandler(GraderRequester):
    CHANGE_COURSE_URL = GraderRequester.GRADER_ROOT_URL + 'index.php?change_course=1'

    def __init__(self, username, password):
        GraderRequester.__init__(self, username, password)
        #override initializer
        if self.login():
            self.loadCourse()
            self.loadTask()

    def loadCourse(self):
        r = self.get(self.CHANGE_COURSE_URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        options = soup.find_all('option')
        result = {}
        for option in options:
            key = option.get_text()
            value = int(option.get('value'))
            result[key] = value
        self.course_dic = result

    def loadTask(self):
        r = self.get(self.GRADER_INDEX_URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        options = soup.find_all('option')
        result = {}
        for option in options:
            key = option.get_text()
            value = int(option.get('value'))
            result[key] = value
        self.task_dic = result

    @property
    def courses(self):
        return list(self.course_dic.keys())

    @property
    def tasks(self):
        return list(self.task_dic.keys())

    def switch_course(self, course_name):
        if not course_name in self.course_dic:
            return False
        headers = {'Referer': self.CHANGE_COURSE_URL,}
        files = {'active_course': (None, str(self.course_dic[course_name])), 'submit': (None, 'Next'),}
        result = self.post(self.GRADER_INDEX_URL, files=files, headers=headers)
        self.loadTask()



if __name__ == '__main__':
    handler = GraderHandler('YOUR_USERNAME', 'YOUR_PASSWORD!')
    handler.switch_course('IntroCS')
    print(handler.tasks)
    handler.switch_course('Programming in C I (Module 2)')
    print(handler.tasks)
