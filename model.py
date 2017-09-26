from handler import GraderHandler
from bs4 import BeautifulSoup

class GraderModel:
    def __init__(self):
        self.rows = {}
    def insertRow(self, key, row):
        self.rows[key] = row
    def getRow(self, key):
        return rows[key]



class SolutionPage(GraderModel):
    GRADER_SOLUTION_URL = GraderHandler.GRADER_ROOT_URL + 'solutions.php'

    def __init__(self, handler:GraderHandler):
        GraderModel.__init__(self)
        self.handler = handler

    def parse(self):
        response = self.handler.get(self.GRADER_SOLUTION_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup.prettify())
        table_rows = soup.find_all('table')[1].find_all('tr')
        for t_row in table_rows:
            if len(t_row) == 6:
                lists = t_row.find_all('td', class_='list')
                task_name = lists[0].get_text()

                task_file_raw = lists[1].find_all('a')
                task_file_link = ''
                if len(task_file_raw) > 0:
                    task_file_link = task_file_raw[1].get('href')

                task_grade = lists[2].get_text()
                is_graded = False
                if '%' in task_grade:
                    is_graded = True

                task_comment = lists[3].get_text()
                if 'by' not in task_comment:
                    task_comment = ''

                row = {'task_name': task_name, 'task_file_link': task_file_link,
                'is_graded': is_graded ,'task_grade': task_grade, 'task_comment': task_comment}
                self.insertRow(task_name, row)



if __name__ == '__main__':
    handler = GraderHandler('USERNAME', 'BLABLABLA')
    page = SolutionPage(handler)

    handler.switch_course('IntroCS')
    page.parse()
    print(page.rows)
    handler.switch_course('Programming in C I (Module 2)')
    page.parse()
