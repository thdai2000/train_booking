"""
订票系统-数据库类型定义部分
使用数据库 mysql
--------------------------------
定义数据类型：1、车次 2、车票
"""

from django.db import models


class Train(models.Model):
    id = models.AutoField(primary_key=True)
    num = models.CharField(max_length=10, verbose_name=u"车次号", default='K100')
    name = models.CharField(max_length=30, verbose_name=u"出发站-到达站", default='')
    time = models.CharField(max_length=20, verbose_name=u"出发时间", default='')
    seats = models.IntegerField(verbose_name=u"剩余座位", default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "车票信息"
        verbose_name_plural = verbose_name


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10, verbose_name=u"乘客名称", default='')
    train = models.ForeignKey(Train, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        try:
            return self.name
        except Ticket.DoesNotExist:
            return self.name

    class Meta:
        verbose_name = "乘客信息"
        verbose_name_plural = verbose_name