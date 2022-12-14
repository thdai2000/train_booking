"""
订票系统-视图逻辑定义部分
分别包括：信息显示view、预订车票view以及查询取消view
--------------------------------
"""

from django.shortcuts import render, redirect
from .models import Train, Ticket
from django.views import View
from .forms import PersonForm, TicketForm, AddForm, DeleteForm, NumForm
from django.http import HttpResponseRedirect
from django.urls import reverse


# 首页显示信息view，将所有的信息传递给主页并进行显示
def userview(request):
    # 获取数据库中所有的信息
    trains = Train.objects.all()
    tickets = Ticket.objects.all()
    ticket_form = TicketForm()
    person_form = PersonForm()
    # add_form = AddForm()
    # delete_form = DeleteForm()
    # 打包为dic
    content = {
        'trains': trains,
        'tickets': tickets,
        'ticket_form': ticket_form,
        'person_form': person_form,
    }
    return render(request, 'booking_system.html', context=content)


def adminview(request):
    trains = Train.objects.all()
    add_form = AddForm()
    delete_form = DeleteForm()
    # 打包为dic
    content = {
        'trains': trains,
        'add_form': add_form,
        'delete_form': delete_form,
    }
    return render(request, 'admin_system.html', context=content)


# 增加trains元组的视图，只允许管理人员访问该视图
def addview(request):
    if request.method == 'POST':
        add_form = AddForm(request.POST)
        delete_form = DeleteForm()
        trains = Train.objects.all()

        content = {
            'trains': trains,
            'add_form': add_form,
            'delete_form': delete_form,
            'adding_message': '',
        }

        if add_form.is_valid():
            if not Train.objects.filter(num=request.POST['num']):
                message = '添加成功！'
                train = Train.objects.create()
                train.num = request.POST['num']
                train.name = request.POST['name']
                train.time = request.POST['time']
                train.seats = request.POST['seats']
                train.save()
            else:
                message = '该车次已存在，添加失败！'
            content['adding_message'] = message
        return render(request, 'admin_system.html', context=content)

    else:
        return HttpResponseRedirect(reverse(adminview))


def deleteview(request):
    if request.method == 'POST':
        delete_form = DeleteForm(request.POST)
        add_form = AddForm()
        trains = Train.objects.all()

        content = {
            'trains': trains,
            'add_form': add_form,
            'delete_form': delete_form,
            'adding_message': '',
        }

        if delete_form.is_valid():

            if Train.objects.get(num=request.POST['num']):
                message = '删除成功！'
                train = Train.objects.get(num=request.POST['num'])
                train.delete()
            else:
                message = '无该车次，删除失败！'

            content['delete_message'] = message

        return render(request, 'admin_system.html', context=content)

    else:

        return HttpResponseRedirect(reverse(adminview))


# 预订车票功能view
def bookingview(request):
    # 页面中有信息传递进来，此时method==POST
    if request.method == 'POST':
        # 将获取的信息进行Form处理
        trains = Train.objects.all()
        tickets = Ticket.objects.all()
        ticket_form = TicketForm(request.POST)
        person_form = PersonForm()
        # add_form = AddForm()
        # delete_form = DeleteForm()

        content = {
            'trains': trains,
            'tickets': tickets,
            'ticket_form': ticket_form,
            'person_form': person_form,
            'booking_message': ''
        }
        # 判断post过来的信息是否正确
        if ticket_form.is_valid():
            train = Train.objects.get(num=request.POST['train_num'])

            flag = 0
            # 确保该乘客没有重复购买
            if Ticket.objects.filter(name=request.POST['name']):
                for ticket in Ticket.objects.filter(name=request.POST['name']):
                    if ticket.train.num == request.POST['train_num']:
                        flag = 1
                        break

            if flag == 1:
                message = '您已购买过此车票，请勿重复购买！'
            else:
                if train.seats >= 1:
                    message = '购买成功！'
                    train.seats -= 1
                    train.save()
                    ticket = Ticket.objects.create()
                    ticket.name = request.POST['name']
                    ticket.train = Train.objects.get(num=request.POST['train_num'])
                    ticket.save()
                else:
                    message = '该车次暂无座位！'

            content['booking_message'] = message

        return render(request, 'booking_system.html', context=content)

    else:

        return HttpResponseRedirect(reverse(userview))


# 查询订单、删除订单操作view
# 此view与之前的view不同，为class view
# 使用class view中的类变量进行表单间信息的传递
class QueryView(View):
    # 此处定义一个类变量，类变量的内存只存在一份，在所有类实例中会共享此参数
    temp = None

    def get(self,request):
        # get操作返回主页即可
        return HttpResponseRedirect(reverse(userview))

    def post(self,request):
        if request.POST.get('submit') == 'find':
            trains = Train.objects.all()
            tickets = Ticket.objects.all()
            ticket_form = TicketForm()
            person_form = PersonForm(request.POST)
            num_form = NumForm()

            content = {
                'trains': trains,
                'tickets': tickets,
                'ticket_form': ticket_form,
                'person_form': person_form,
                'num_form': num_form,
                'query_message': '',
                'show': 0,
            }

            if Ticket.objects.filter(name=request.POST['name']):
                # 根据传递来的post信息，过滤获得此ticket
                tickets = Ticket.objects.filter(name=request.POST['name'])
                content['show'] = 1       # flag，若为1则在页面中显示已经查询到的信息
                content['tickets'] = tickets
                content['query_message'] = '查询成功！'
                # 将查询信息保存到类变量中
                QueryView.temp = request.POST['name']
                return render(request, 'booking_system.html', context=content)

            else:
                content['query_message'] = '未找到该用户！'
                return render(request, 'booking_system.html', context=content)

        else:
            if request.POST.get('submit') == 'yes':
                trains = Train.objects.all()
                tickets = Ticket.objects.filter(name=QueryView.temp)
                ticket_form = TicketForm()
                person_form = PersonForm()
                num_form = NumForm(request.POST)

                content = {
                    'trains': trains,
                    'tickets': tickets,
                    'ticket_form': ticket_form,
                    'person_form': person_form,
                    'num_form': num_form,
                    'cancel_message': '',
                }
                # 取消订单后
                flag = 0

                for ticket in tickets:
                    if ticket.train.num == request.POST['num']:
                        train = Train.objects.get(num=ticket.train.num)
                        train.seats += 1 # 座位归还
                        train.save()
                        ticket.delete()  # 删除此人购买信息
                        flag = 1
                        content['cancel_message'] = '取消订单成功！'
                        break

                if flag == 0:
                    content['cancel_message'] = '未找到该订单！'

                return render(request, 'booking_system.html', context=content)

            elif request.POST.get('submit') == 'no':
                    return HttpResponseRedirect(reverse(userview))



