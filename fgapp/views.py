from django.shortcuts import render
from .models import users, todayfg,todayfg_old
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse,HttpResponseRedirect
import datetime
import os
from os import path
import openpyxl
import locale
from openpyxl import Workbook

locale.setlocale( locale.LC_ALL, '' )

#view for login page
def login(request):
    try:
        request.session.get('user')
        a = request.session['user']
        return render(request, 'home.html',{'user': a })

    except:
        return render(request, 'user_login.html')


def home(request):
    #check if user is already signed in
    try:
        request.session.get('user')
        a = request.session['user']

        return render(request, 'home.html',{'user': a })

    except:
        #check if login form has been submitted
        if 'name' in request.POST:
            username = request.POST['name']
            pwd = request.POST['password']
            try:
                dbline = users.objects.get(name = username)
                dbpass = dbline.password

                if dbpass == pwd:
                        request.session['user'] = username
                        return render(request, 'home.html', { 'user' : username })

                else:
                    return HttpResponse('Wrong password')

            except NameError:
                return HttpResponse('User not in DB')
        #send to login page
        else:
            return login(request)

def logout(request):
    request.session.delete()
    return login(request)

def upload(request):
    if request.method == 'POST' and request.FILES['todayfg']:
        x = datetime.datetime.now()
        current_day = str(x.day)

        if str(path.exists('./files/fg/TVT/TVT ' + current_day + '.xlsx' )) == 'True':
            os.remove("./files/fg/TVT/TVT " + current_day + ".xlsx" )
            myfile = request.FILES['todayfg']
            fs = FileSystemStorage()
            fs.save('./files/fg/TVT/TVT ' + current_day + '.xlsx', myfile)
            uploaded_file_url = './files/fg/TVT/TVT ' + current_day + '.xlsx'
            return HttpResponseRedirect('/upload_model/')

        else:
            yest_date = str(x.day-1)
            try:
                os.remove("./files/fg/TVT/ydaytvt.xlsx")
                os.rename("./files/fg/TVT/TVT "+ yest_date +".xlsx", "./files/fg/TVT/ydaytvt.xlsx")
            except:
                a = 10
            myfile = request.FILES['todayfg']
            fs = FileSystemStorage()
            current_day = str(x.day)
            filename = fs.save('./files/fg/TVT/TVT ' + current_day + '.xlsx', myfile)
            uploaded_file_url = fs.url(filename)
            return HttpResponseRedirect('/upload_model/')


def upload_to_model(request):

    todayfg_old.objects.all().delete()

    dump_new = todayfg.objects.all()

    for item in dump_new:
        old_var = todayfg_old()
        old_var.matno = item.matno
        old_var.matdes = item.matdes
        old_var.plant = item.plant
        old_var.batch = item.batch
        old_var.qty = item.qty
        old_var.value1 = item.value1
        old_var.age = item.age
        old_var.cus_name = item.cus_name
        old_var.platform = item.platform
        old_var.kam_name = item.kam_name
        old_var.log_des_advice = item.log_des_advice
        old_var.kam_qty_clear = item.kam_qty_clear
        old_var.kam_remarks = item.kam_remarks
        old_var.kam_des_date = item.kam_des_date
        old_var.kam_des_adv = item.kam_des_adv
        old_var.concat = item.concat
        old_var.save()

    todayfg.objects.all().delete()

    x = datetime.datetime.now()
    y = str(x.day)
    file_path = './files/fg/TVT/TVT '+ y + '.xlsx'
    re_wb = Workbook()
    ref_wb = openpyxl.load_workbook(file_path,data_only=True)

    #ws_name = str(x.day) + str(x.month)+str(x.year)
    ws_name = '23.12.2020'
    ws = ref_wb[ws_name]

    rows_all = tuple(ws.rows)

    i = 2

    for row in rows_all:
        a = todayfg()
        try:
            a.matno = str(rows_all[i][0].value)
            a.matdes = str(rows_all[i][1].value)
            a.plant = str(rows_all[i][2].value)
            a.batch = str(rows_all[i][5].value)
            a.qty = int(rows_all[i][7].value)
            a.value1 = int(rows_all[i][9].value)
            a.age = int(rows_all[i][10].value)
            a.cus_name = str(rows_all[i][11].value)
            a.platform = str(rows_all[i][12].value)
            a.kam_name = str(rows_all[i][13].value)
            a.log_des_advice = str(rows_all[i][14].value)
            a.log_des_advice = a.log_des_advice.lower()
            a.log_remarks = 'No Remarks'

            batch_check = a.batch

            try:
                b = todayfg_old.objects.get(batch=batch_check)
                a.kam_qty_clear = b.kam_qty_clear
                a.kam_remarks = b.kam_remarks
                a.kam_des_date = b.kam_des_date
                a.kam_des_adv = b.kam_des_adv
                a.concat = str(a.batch) + str(a.qty)
                a.save()
                i = i+1

            except:
                a.kam_qty_clear = 'Not Fixed'
                a.kam_remarks = 'No Remarks'
                a.kam_des_date = 'Not Mentioned'
                a.kam_des_adv = a.log_des_advice
                a.concat = str(a.batch) + str(a.qty)
                a.save()
                i = i + 1
        except:
            break
    return viewfg(request)

def viewfg(request):

    all_items = todayfg.objects.all()
    return render(request, 'viewfg.html',{'rows123': all_items})


#add KAM's comments
def kam_comm(request):
    comment = request.POST['kam_comm']
    obj_id = request.POST['obj_id']
    a = todayfg.objects.get(id=obj_id)
    a.kam_remarks = comment
    a.save()
    return viewfg(request)


#add KAM's dispatch date
def kam_des_date(request):
    des_date = request.POST['kam_des_date']
    obj_id = request.POST['obj_id']
    a = todayfg.objects.get(id=obj_id)
    a.kam_des_date = des_date
    a.save()
    return viewfg(request)

#add KAM's dispatch advice
def kam_des_adv(request):
    des_adv = request.POST['adv']
    obj_id = request.POST['obj_id']
    qty_clear = request.POST['kam_qty']
    a = todayfg.objects.get(id=obj_id)
    a.kam_des_adv = des_adv
    if des_adv == "yes":
       a.kam_qty_clear = a.qty
    if des_adv == "no":
        a.kam_qty_clear = 0
    if des_adv == "part":
        a.kam_qty_clear = qty_clear
    a.save()
    return viewfg(request)

def overall_filter(request):

    filter_all = {}

    if not request.POST['plt'] == 'Platform':
        filter_all = {'platform': request.POST['plt']}
    if not request.POST['des_adv'] == 'Clearance (Logistics)':
        filter_all['log_des_advice'] = request.POST['des_adv']

    all_items = todayfg.objects.filter(**filter_all)
    return render(request, 'viewfg.html', {'rows123': all_items, 'filters':filter_all})


#KAM wise summary
def kam_summary(request):

    dict = {}

    try:
        x = request.POST['dtfilter']
    except:
        x = int(90)

    kams = todayfg.objects.order_by('kam_name').values('kam_name').distinct()
    j = 0
    overall_value = 0
    overall_log_yes = 0
    overall_log_no = 0
    overall_kam_yes = 0
    overall_kam_no = 0
    for kam in kams:
        items = todayfg.objects.filter(kam_name = kams[j]['kam_name'])
        value = 0
        value_log_yes = 0
        value_log_no = 0
        value_kam_yes = 0
        value_kam_no = 0

        i = 0
        for item in items:
            item.age = int(item.age)
            x = int(x)
            if item.age <= x:
                try:
                    value = value + float(item.value1)
                    if item.log_des_advice == 'yes':
                        value_log_yes = value_log_yes + float(item.value1)
                    if item.log_des_advice == 'no':
                        value_log_no = value_log_no + float(item.value1)
                    if item.kam_des_adv == 'yes':
                        value_kam_yes = value_kam_yes + float(item.value1)
                    if item.kam_des_adv == 'no':
                        value_kam_no = value_kam_no + float(item.value1)
                    if item.kam_des_adv == 'part':
                        #value_kam_no = value_kam_no + float(item.value1)
                        price = item.value1/item.qty
                        val = price * item.kam_qty_clear
                        value_kam_yes = value_kam_yes + val

                except:
                    continue
            i = i+1
        value = int(value)
        value = value / 100000
        value = round(value,1)
        overall_value = overall_value + value
        overall_value = round(overall_value, 1)

        value_log_yes = value_log_yes / 100000
        value_log_yes = round(value_log_yes, 1)
        overall_log_yes = overall_log_yes + value_log_yes
        overall_log_yes = round(overall_log_yes, 1)

        value_kam_yes = value_kam_yes / 100000
        value_kam_yes = round(value_kam_yes, 1)
        overall_kam_yes = overall_kam_yes + value_kam_yes
        overall_kam_yes = round(overall_kam_yes, 1)

        value_log_no = value_log_no / 100000
        value_log_no = round(value_log_no, 1)
        overall_log_no = overall_log_no + value_log_no
        overall_log_no = round(overall_log_no, 1)

        value_kam_no = value_kam_no / 100000
        value_kam_no = round(value_kam_no, 1)
        overall_kam_no = overall_kam_no + value_kam_no
        overall_kam_no = round(overall_kam_no, 1)

        dict[kams[j]['kam_name']] = {"total_value": value, "value_log_yes": value_log_yes, "value_log_no": value_log_no, "value_kam_yes":value_kam_yes, "value_kam_no":value_kam_no}

        j = j + 1

    dict_items = dict.items()

    overall = {'Total FG value': overall_value, 'Dispatch Advice Available(Log)': overall_log_yes, 'Dispatch Advice Available(KAM)': overall_kam_yes}
    overall = overall.items()

    return render(request, 'kamsum.html',{'dict':dict_items, 'overall':overall, 'age' : x})

#Customer wise summary
def cus_summary(request):


    dict = {}

    try:
        x = request.POST['dtfilter']
    except:
        x = int(90)

    cuss = todayfg.objects.order_by('cus_name').values('cus_name').distinct()
    j = 0
    overall_value = 0
    overall_log_yes = 0
    overall_log_no = 0
    overall_kam_yes = 0
    overall_kam_no = 0
    for cus in cuss:
        items = todayfg.objects.filter(cus_name = cuss[j]['cus_name'])
        value = 0
        value_log_yes = 0
        value_log_no = 0
        value_kam_yes = 0
        value_kam_no = 0

        i = 0
        for item in items:
            item.age = int(item.age)
            x = int(x)
            if item.age <= x:
                try:
                    value = value + float(item.value1)
                    if item.log_des_advice == 'yes':
                        value_log_yes = value_log_yes + float(item.value1)
                    if item.log_des_advice == 'no':
                        value_log_no = value_log_no + float(item.value1)
                    if item.kam_des_adv == 'yes':
                        value_kam_yes = value_kam_yes + float(item.value1)
                    if item.kam_des_adv == 'no':
                        value_kam_no = value_kam_no + float(item.value1)
                    if item.kam_des_adv == 'part':
                        #value_kam_no = value_kam_no + float(item.value1)
                        price = item.value1/item.qty
                        val = price * item.kam_qty_clear
                        value_kam_yes = value_kam_yes + val

                except:
                    continue
            i = i+1
        value = int(value)
        value = value / 100000
        value = round(value,1)
        overall_value = overall_value + value
        overall_value = round(overall_value, 1)

        value_log_yes = value_log_yes / 100000
        value_log_yes = round(value_log_yes, 1)
        overall_log_yes = overall_log_yes + value_log_yes
        overall_log_yes = round(overall_log_yes, 1)

        value_kam_yes = value_kam_yes / 100000
        value_kam_yes = round(value_kam_yes, 1)
        overall_kam_yes = overall_kam_yes + value_kam_yes
        overall_kam_yes = round(overall_kam_yes, 1)

        value_log_no = value_log_no / 100000
        value_log_no = round(value_log_no, 1)
        overall_log_no = overall_log_no + value_log_no
        overall_log_no = round(overall_log_no, 1)

        value_kam_no = value_kam_no / 100000
        value_kam_no = round(value_kam_no, 1)
        overall_kam_no = overall_kam_no + value_kam_no
        overall_kam_no = round(overall_kam_no, 1)

        dict[cuss[j]['cus_name']] = {"total_value": value, "value_log_yes": value_log_yes, "value_log_no": value_log_no, "value_kam_yes":value_kam_yes, "value_kam_no":value_kam_no}

        j = j + 1

    dict_items = dict.items()

    overall = {'Total FG value': overall_value, 'Dispatch Advice Available(Log)': overall_log_yes, 'Dispatch Advice Available(KAM)': overall_kam_yes}
    overall = overall.items()

    return render(request, 'cussum.html',{'dict':dict_items, 'overall':overall, 'age' : x})

#KAM specific details
def kam_det(request):

    kam = request.GET['kam']
    all_items = todayfg.objects.filter(kam_name= kam)
    return render(request, 'viewfg.html', {'rows123': all_items})

#Customer specific details
def cus_det(request):

    cus = request.GET['cus']
    all_items = todayfg.objects.filter(cus_name= cus)
    return render(request, 'viewfg.html', {'rows123': all_items})












