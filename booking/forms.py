"""
订票系统-表单处理部分
--------------------------------
"""

from django import forms
from .models import Ticket


# 车次信息填写Form
class AddForm(forms.Form):
    num = forms.CharField(label='num', max_length=10, error_messages={'required': '请填写您车次号',
                                                                        'max_length': '车次号过长'})
    name = forms.CharField(label='name', max_length=30, error_messages={'required': '请填写列车出发站-到达站',
                                                                        'max_length': '出发站-到达站过长'})
    # time = forms.DateTimeField(label='time', widget=forms.DateInput(format='%d/%m/%Y %h:%i'))
    time = forms.CharField(label='time', max_length=20, error_messages={'required': '请填写发车时间',
                                                                        'max_length': '字符串过长'})
    seats = forms.IntegerField(label='seats')


# 车次删除信息填写Form
class DeleteForm(forms.Form):
    num = forms.CharField(label='num', max_length=10, error_messages={'required': '请填写您车次号',
                                                                        'max_length': '车次号过长'})


# 预订车票填写信息Form
class TicketForm(forms.Form):
    name = forms.CharField(label='name', error_messages={'required': '请填写您的姓名'})
    train_num = forms.CharField(label='ticket_num', max_length=10, error_messages={'required': '车票编号输入不正确'})


# 查询信息填写Form
class PersonForm(forms.Form):
    name = forms.CharField(label='name', max_length=10, error_messages={'required': '请填写您的姓名',
                                                                        'max_length': '名字太长了'})


class NumForm(forms.Form):
    num = forms.CharField(label='num', max_length=10, error_messages={'required': '请填写车次号',
                                                                      'max_length': '车次号过长'})

