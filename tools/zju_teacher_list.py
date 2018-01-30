import urllib2

from bs4 import BeautifulSoup

#from www.models import Teacher, College
HOST = 'http://person.zju.edu.cn'


def fetch_colleges_from_zju():
    '''
    :return: a colleges list
    [
        {
            'url': '',
            'title': '',
            'page_count': 0
        }
    ]
    '''
    url = HOST + '/dept-person-5-501000.html'
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    a_tags = soup.select('.hangju2')
    results = [{
        'url': a.get('href'),
        'title': a.get('title'),
        } for a in a_tags if 'dept-person' in a.get('href')
    ]
    for college in results:
        url = HOST + college['url']
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html)
        page_count = soup.select('#form1')[0].find('font', color='#FF9900').get_text()
        college['page_count'] = int(page_count)
    return results


def fetch_teacher_list(url):
    '''

    :param url: url of the teacher list page
    :return: a teachers list
    [
        {
            'name': ''
        }
    ]
    '''
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    a_tags = soup.select('zhishi')

    teachers = []
    for a in a_tags:
        teacher = {}
        teacher['name'] = a.get_text()
        teachers.append(teacher)


def fetch_all_teacher_list():
    colleges = fetch_colleges_from_zju()


if __name__ == '__main__':
    fetch_all_teacher_list()