from django.db import models


class Room(models.Model):
    room_id = models.CharField(max_length=10, unique=True)  # 设置机房id唯一
    ad_id = models.ForeignKey('Administrator', on_delete=models.CASCADE, to_field='ad_id')  # 设置外键，与管理员模型关联


class Student(models.Model):
    student_id = models.CharField(max_length=10, unique=True)  # 设置学生id唯一
    student_name = models.CharField(max_length=100)
    student_money = models.DecimalField(max_digits=10, decimal_places=2)  # 设置账户余额为十进制数
    password = models.CharField(max_length=20)


class Administrator(models.Model):
    ad_id = models.CharField(max_length=10, unique=True)  # 设置管理员id唯一
    ad_name = models.CharField(max_length=100)
    password = models.CharField(max_length=20)


class Computer(models.Model):
    com_id = models.CharField(max_length=10, unique=True)  # 设置电脑id唯一
    room_id = models.ForeignKey('Room', on_delete=models.CASCADE, to_field='room_id')  # 设置外键，与机房模型关联


class Record(models.Model):
    record_id = models.CharField(max_length=30, unique=True)  # 设置记录id唯一
    student_id = models.ForeignKey('Student', on_delete=models.CASCADE, to_field='student_id')  # 设置外键，与学生模型关联
    com_id = models.ForeignKey('Computer', on_delete=models.CASCADE, to_field='com_id')  # 设置外键，与电脑模型关联
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # 在前端发出请求前为空值
    type_id = models.ForeignKey('Type', on_delete=models.CASCADE, null=True,
                                blank=True, to_field='type_id')  # 设置外键，与类型模型关联，在分类删除时将之前的记录都设置为特定值
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)  # 在输入end_time前为空值


class Type(models.Model):
    type_id = models.CharField(max_length=10, unique=True)  # 设置类型id唯一
    type_name = models.CharField(max_length=100)
