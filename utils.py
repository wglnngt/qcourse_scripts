import requests
import json
import os
import subprocess


def get_course_from_api(cid=None):
    # 获取课程信息
    if cid is None:
        print('请输入cid！')
    url = 'https://ke.qq.com/cgi-bin/course/basic_info?cid=' + str(cid)
    response = requests.get(url).json()
    name = response.get('result').get('course_detail').get('name').replace('/', '／').replace('\\', '＼')
    with open(name+'.json', 'w') as f:
        f.write(json.dumps(response))
    return name


def get_terms(filename):
    # 从json文件内获取学期信息
    with open(filename, 'r') as f:
        course_info = json.loads(f.read())
    terms = course_info.get('result').get('course_detail').get('terms')
    return terms


def get_chapters(filename, term_index):
    # 从json文件内获取章节信息
    with open(filename, 'r') as f:
        course_info = json.loads(f.read())
    chapters = course_info.get('result').get('course_detail').get('terms')[term_index].get('chapter_info')[0].get('sub_info')
    return chapters


def get_courses_from_chapter(chapter):
    return chapter.get('task_info')


def get_course_url(course):
    # 传入课程字典，拼接成课程链接
    cid = course.get('cid')
    term_id = course.get('term_id')
    course_id = course.get('taid')
    url = 'https://ke.qq.com/webcourse/{}/{}#taid={}'.format(cid, term_id, course_id)
    return url


def get_all_urls(filename, term_index):
    chapters = get_chapters(filename, term_index)
    result = {}
    for chapter in chapters:
        chapter_name = chapter.get('name')
        courses = get_courses_from_chapter(chapter)
        chapter_info = {}
        for course in courses:
            chapter_info.update({course.get('name'): get_course_url(course)})
        result.update({chapter_name: chapter_info})
    return result


def print_menu(menu):
    for item in menu:
        print(str(menu.index(item))+'. '+item)


def ts2mp4(file):
    ffmpeg = os.path.join(os.getcwd(), 'ffmpeg.exe')
    basename = os.path.basename(file).split('.')[0]
    file_dir = os.path.split(file)[0]
    output = os.path.join(file_dir, basename)
    cmd = ffmpeg + " -i \"" + file + "\" -c copy \"" + output + "\".mp4"
    # os.system(cmd)
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    os.remove(file)

def m3u82mp4(url, file):
    m3u8dl = os.path.join(os.getcwd(), 'm3u8dl.exe')
    basename = os.path.basename(file)
    file_dir = os.path.split(file)[0]
    output = os.path.join(file_dir, basename)
    cmd = m3u8dl + " \"" + url + "\" --workDir \"" + file_dir + "\" --saveName " + basename + " --enableDelAfterDone"
    os.system(cmd)
    #subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def choose_term(filename):
    terms = get_terms(filename)
    term_index = 0
    if len(terms) > 1:
        print_menu([i.get('name') for i in terms])
        term_index = input('请选择学期：')
    return int(term_index)
