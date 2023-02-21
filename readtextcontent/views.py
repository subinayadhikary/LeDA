from datetime import datetime
import json
import os
import re
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from .settings import MEDIA_ROOT, UTILS_ROOT
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
import json
from rouge import Rouge


# Check all the files in media dirs
def __get_all_media_files(path):
    files = []
    for file in os.listdir(path):
        if file.endswith('.txt'):
            files.append(file)
    return files


# Read Tags
def __get_tags(path):
    with open(os.path.join(path, 'tags.txt'), 'r') as file:
        tags = file.read()
    tags = tags.split(',')
    return tags[:-1]


# Get the files according to user permissions
def __get_user_files(user):
    with open(UTILS_ROOT + 'permissions.json') as file:
        files = json.load(file)
    print('='*10, files)
    if files:
        files = files.get(user.username)
        if files:
            return files
    return []


def login(request):
    if request.method == 'POST':
        # Login process of an user
        username=request.POST.get('username')
        password=request.POST.get('password')

        if not username:
            error = 'username'
            msg = 'This field is required.'
            messages.error(request, msg, extra_tags=error)
        elif not password:
            error = 'password'
            msg = 'This field is required.'
            messages.error(request, msg, extra_tags=error)
        elif username and password:
            user = auth.authenticate(request, username=username, password=password)
            if user:
                print('user found')
                auth.login(request, user)
                messages.success(request, 'You have successfully logged in.')
                return redirect('index')
            else:
                print('user not found')
            messages.error(request, 'Invalid username or password.')


    return render(request, 'login.html')


@login_required(login_url='login')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.success(request, 'You have successfully logged out.')
        return render(request, 'login.html')


@login_required(login_url='login')
def index(request):
    # Get the current user instance
    user = request.user
    tags = __get_tags(UTILS_ROOT)

    for dir_path in [MEDIA_ROOT + 'original', MEDIA_ROOT + 'updated']:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

    with open(UTILS_ROOT + 'permissions.json') as file:
        json_data = json.load(file)

    # print(json_data)

    context = {
        'all_files' : [],
        'tags'  : tags,
        'users' : [],
    }

    # If user is logged in and user is admin
    if user.is_authenticated and user.is_superuser:
        # Send all the uploaded file of media foldre
        uploded_files = __get_all_media_files(MEDIA_ROOT + 'updated/')
        #context['all_files'] = uploded_files
    else:
        # If user is normal user
        # Read the permissions file
        uploded_files = __get_user_files(user)
        # context['all_files'] = uploded_files

    for file in uploded_files:
        users = []
        for key, val in json_data.items():
            if file in val:
                if not user.username == key:
                    file_path = MEDIA_ROOT + f'updated/{key}/' + file
                    if os.path.exists(file_path):
                        users.append(key)
        context['all_files'] += [(file, users)]

    for file in uploded_files:
        for key, val in json_data.items():
            if file in val:
                context['users'] += [key]

    print('=>'*5, uploded_files, context['users'])

    return render(request, 'index.html', context=context)


@login_required(login_url='login')
def uploadFile(request):
    # Current Logged In username
    username = request.user.username

    # Upload File
    if request.method == 'POST' and request.FILES.get('textFile', None):
        file = request.FILES['textFile']
        file_name = str(file)
        original_file_path = MEDIA_ROOT + 'original/'
        updated_file_path = MEDIA_ROOT + 'updated/'

         # Checking Same File in List
        if file_name in __get_all_media_files(original_file_path):
            messages.warning(request, 'File with same name exist.')
        else:
            # Save file in media folder under original and updated
            original_fs = FileSystemStorage(original_file_path, original_file_path)
            original_fs.save(file_name, file)

            updated_fs = FileSystemStorage(updated_file_path, updated_file_path)
            updated_fs.save(file_name, file)

            # If file save in computer then display success message
            messages.success(request, 'File uploaded successfully.')

    # Update File Content
    if request.method == "POST" and 'file_name' in request.POST:
        data = request.POST['editor']
        username = request.POST['file_username']

        data = data.replace('&nbsp;', ' ')
        data = data.replace('<br><br>', '')

        file_name = request.POST['file_name']
        if data:
            # Checking current user directory
            user_path = MEDIA_ROOT + 'updated/' + username
            if not os.path.exists(user_path):
                os.mkdir(user_path)

            file_path = user_path + '/' + file_name
            with open(file_path, 'w') as f:
                f.write(data)

        search_file_path = UTILS_ROOT + 'search_file.json'
        with open(search_file_path, 'r') as f:
            json_data = json.load(f)

        # Checking file in search_file.json
        if not json_data.get(file_name):
            json_data.setdefault(file_name, {})

        if not json_data[file_name].get(username):
            json_data[file_name].setdefault(username, {})
        else:
            json_data[file_name][username] = {}


        with open(file_path, 'r') as f:
            contents = f.read()

        soup = BeautifulSoup(contents, 'html5lib')

        spans = soup.findAll('span')

        for span in spans:
            try:
                tag = span['title'].strip()
            except:
                tag = ''

            if tag:
                val = span.text

                json_data[file_name][username].setdefault(val.lower(), [])

                if tag not in json_data[file_name][username][val.lower()]:
                    json_data[file_name][username][val.lower()] += [tag]


        with open(search_file_path, 'w') as f:
            f.write(json.dumps(json_data))

        # If file save in computer then display success message
        messages.success(request, 'File updated successfully.')

    # File Update Notification
    # search_file_path = UTILS_ROOT + 'files.json'
    # with open(search_file_path, 'r') as f:
    #     files_json_data = json.load(f)

    # Checking file in search_file.json
    # if not files_json_data.get(file_name):
    #     files_json_data.setdefault(file_name, {})

    # if not files_json_data[file_name].get(username):
    #     files_json_data[file_name].setdefault(username, {})

    # if not files_json_data[file_name][username].get('count'):
    #     files_json_data[file_name][username].setdefault('count', 0)
    # if not files_json_data[file_name][username].get('previous'):
    #     files_json_data[file_name][username].setdefault('previous', 0)
    # if not files_json_data[file_name][username].get('current'):
    #     files_json_data[file_name][username].setdefault('current', 0)

    # # Get File Size
    # file_size = os.path.getsize(file_path)
    # print('='*10, f'File Size : {file_size}')

    # # Compare Value of previous and current
    # if not files_json_data[file_name][username]['previous'] == files_json_data[file_name][username]['current']:
    #     print('='*10, 'UPDATED FILE', '='*10)

    # Send all the uploaded file of media folder
    uploded_files = __get_all_media_files(MEDIA_ROOT+'updated/')

    context = {
        'all_files' : uploded_files,
    }

    # return redirect(request, 'index.html', context=context)
    return redirect('index')


@login_required(login_url='login')
def readFile(request, file_name):
    # get current user
    user = request.user

    # If user is logged in and user is admin
    if user.is_authenticated and user.is_superuser:
        file_path = MEDIA_ROOT + 'updated/' + file_name
    else:
        file_path = MEDIA_ROOT + f'updated/{user.username}/' + file_name
        if not os.path.exists(file_path):
            file_path = MEDIA_ROOT + 'updated/' + file_name

    # Read file content
    with open(file_path, 'r') as _file:
        contents = _file.read()

    # if '<br>' not in contents:
    #     contents = '<br>'.join(contents)
    n_contents = ''
    for line in contents.splitlines():
        if line:
            n_contents += line + '<br>'
        else:
            n_contents += '<br>'

    return HttpResponse(n_contents)

@login_required(login_url='login')
def readUserFile(request, file_name, username):
    # get current user
    user = request.user

    # If user is logged in and user is admin
    # if user.is_authenticated and user.is_superuser:
    #     file_path = MEDIA_ROOT + 'updated/' + file_name
    # else:
    if username == 'none':
        username = user.username

    file_path = MEDIA_ROOT + f'updated/{username}/' + file_name
    if not os.path.exists(file_path):
        file_path = MEDIA_ROOT + 'updated/' + file_name

    # Read file content
    with open(file_path, 'r') as _file:
        contents = _file.read()

    # if '<br>' not in contents:
    #     contents = '<br>'.join(contents)
    n_contents = ''
    for line in contents.splitlines():
        if line:
            n_contents += line + '<br>'
        else:
            n_contents += '<br>'

    return HttpResponse(n_contents)


@login_required(login_url='login')
def deleteFile(request, file_name):
    # Current Logged In username
    user = request.user

    file_is_found = False
    for (root, dirs, files) in os.walk('.', topdown=True):
        for file in files:
            if file_name == file:
                file_is_found = True
                os.remove(os.path.join(root, file))

    if file_is_found:
        messages.success(request, 'File deleted successfully.')
    else:
        messages.error(request, 'Given file was not found.')

    ## Delete Tag from file
    search_file_path = UTILS_ROOT + 'search_file.json'
    with open(search_file_path, 'r') as f:
        json_data = json.load(f)

    new_json_data = {}
    for key, val in json_data.items():
        if not key == file_name:
            new_json_data[key] = val

    with open(search_file_path, 'w') as f:
        f.write(json.dumps(new_json_data))

    ## Delete File from permission file
    permission_file_path = UTILS_ROOT + 'permissions.json'
    with open(permission_file_path, 'r') as f:
        json_data = json.load(f)

    new_json_data = {}
    for key, files in json_data.items():
        f = []
        for file in files:
            if not file == file_name:
                f.append(file)
        new_json_data[key] = f


    with open(permission_file_path, 'w') as f:
        f.write(json.dumps(new_json_data))


    # Send all the uploaded file of media foldre
    uploded_files = __get_all_media_files(MEDIA_ROOT)

    context = {
        'all_files' : uploded_files,
    }

    return render(request, 'index.html', context=context)


def addTag(request, tag_name):
    file_path = UTILS_ROOT + 'tags.txt'
    tag_name_found = False

   # Read file content
    with open(file_path, 'r') as _file:
        tags = _file.read()

    file = open(file_path, 'w')
    for tag in tags.split(',')[:-1]:
        if tag_name == tag:
            # Remove Tag
            tag_name_found = True
            continue
        else:
            # Add Tag
            file.write(tag+',')

    if not tag_name_found:
        file.write(tag_name+',')

    file.close()
    # with open(file_path, 'a') as _file:
    #     _file.write(tag_name+',')


    tags = tags.split(',')[:-1]
    return HttpResponse(tags)


@login_required(login_url='login')
def searchFile(request):
    user = request.user
    tag_name = request.GET.get('search_text').lower()

    if not tag_name:
        return redirect('index')

    tags = __get_tags(UTILS_ROOT)
    context = {
        'tags'  : tags
    }

    # if user.is_authenticated and user.is_superuser:
    search_file_path = UTILS_ROOT + 'search_file.json'
    files_name = []
    keys = []

    with open(search_file_path, 'r') as f:
        json_data = json.load(f)

    for key, val in json_data.items():
        print(key, val)
        for key1, val1 in val.items():
            for val2 in val1.values():
                temp = [i.lower() for i in val2]
                if tag_name in temp and key not in keys:
                    keys.append(key)
                    files_name.append((key, [key1]))

    context['all_files'] = files_name
    # else:
    #     _files = __get_user_files(user)
    #     files_name = []
    #     for file in _files:
    #         f_name = MEDIA_ROOT + f'updated/{file}'

    #         with open(f_name, 'r') as f:
    #             data = f.read()

    #         search_pattern = '(?:title=")(.\w+)'
    #         res = re.findall(search_pattern, data)

    #         if tag_name in res:
    #             files_name.append(file)

        # context['all_files'] = files_name
        # context['all_files'] += [(files_name, [])]

    return render(request, 'index.html', context=context)



'''
===================== Compare File ================
'''

def cal_sim(s1,s2):   # For calculating rouge-l score
    ROUGE = Rouge()
    k=ROUGE.get_scores(s1,s2)[0]
    score=k['rouge-l']['f']
    return score

def compareFile(file_name):
    file_path = UTILS_ROOT + 'search_file.json'
    json_data=open(file_path)
    jdata = json.load(json_data)
    correct,partial,missing=0,0,0
    for k2, v2 in jdata.items():
        if(k2==file_name):
            d1 = dict(list(v2.items())[len(v2)//2:])
            d2 = dict(list(v2.items())[:len(v2)//2])
            for k,v in d1.items():
                for k1,v1 in d2.items():
                    for key,value in v1.items():
                        for key1,value1 in v.items():
                            score=cal_sim(key,key1)
                            if (score >0.8):
                                if(value==value1):
                                    correct=correct+1
                                else:
                                    missing=missing+1
                            elif((score>0.4)and (score<0.8)):
                                if(value==value1):
                                  partial=partial+1
                                else:
                                   missing=missing+1
            recall=(correct+0.5*partial)/(correct+partial+missing+0.1)
            precision=(correct+0.5*partial)/(correct+partial+missing+0.1)
            try:
                f_score=(2*recall*precision)/(recall+precision)
                f_score=round(f_score,2)
            except ZeroDivisionError:
                f_score = 0

            print('='*10, f_score)
            return f_score


@login_required(login_url='login')
def compare(request, file_name):
    res = compareFile(file_name)
    return HttpResponse(res)