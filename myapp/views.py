import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.serializers import ListSerializer
from rest_framework.views import APIView
from rest_framework.request import Request


# class ParamVersion(object):
#     def determin_version(self,request):
#         version = request.query_params.get('version')
#         return version
#

from rest_framework.versioning import QueryParameterVersioning,URLPathVersioning
# class UsersView(APIView):
#     versioning_class = QueryParameterVersioning
#     def get(self,request,*args,**kwargs):
#         print(request.version)
#         return HttpResponse('用户列表')
from myapp import models
from myapp.utils.serializers.pager import PagerSerializer


class UsersView(APIView):
    def get(self,request,*args,**kwargs):
        self.dispatch()
        # 1.获取版本
        print(request.version)
        # 2.获取版本的对象
        print(request.versioning_scheme)
        # 3. 内置的反向生成url，不需要指定版本，会自动生成，其实是当前url的版本
        u1 = request.versioning_scheme.reverse(viewname='uuu',request=request)
        print(u1)
        # 使用Django内置的反向生成url,必须要指定版本
        u2 = reverse(viewname='uuu',kwargs={'version':1})
        print(u2)
        return HttpResponse('用户列表')


class DjangoView(APIView):
    def get(self,request):
        print(type(request._request))
        from django.core.handlers.wsgi import WSGIRequest

        return HttpResponse('post 和body')


from rest_framework import request, serializers


class ParserView(APIView):
    # parser_classes = [JSONParser,FormParser]
    # JSONParser:表示只能解析content-type:application/json头
    #FormParser：表示只能解析content-type:application/x-www-form-urlencoded头
    def post(self,request,*args,**kwargs):
        """
        解析： 就是把请求体的内容转换成你可以看的格式
        允许用户发送JSON格式数据，可以接收json的那个头发来的数据，也可以接收字典格式的数据
        1，content-type:application/json
        2，{'name':'alex','age':18}
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        """
        只有用到的时候才会解析，这里使用到了data,所以由request.data触发
        解析：
        1.获取用户的请求
        2.获取用户的请求体
        3.根据用户请求头 和 parser_classes = [JSONParser,FormParser]中支持的请求头进行比较
        4.JSONParser符合，就是用JSONParser对象去请求体
        5.将解析的数据赋值给request.data
       """
        print(request.data)
        return HttpResponse('ParserView')



class RolesSerializer(serializers.Serializer):
    # 字段必须和数据库中的字段一致
    id = serializers.IntegerField()
    title = serializers.CharField()




class RolesView(APIView):
    def get(self,request,*args,**kwargs):
        # 方式一：
        # roles = models.Role.objects.all().values('id','title')
        # # 转换成list格式，可以dumps
        # roles = list(roles)
        # # ensure_ascii=False支持中文
        # ret = json.dumps(roles,ensure_ascii=False)


        # 方式二：对于[obj,obj,...][obj,obj,...]数据进行格式化
        # 拿到的是一个querySet格式的对象
        # roles = models.Role.objects.all()
        # # 实例化，many表示里面有多条数据
        # ser = RolesSerializer(instance=roles,many=True)
        # ret = json.dumps(ser.data,ensure_ascii=False)


        # 对单个对象进行序列化
        role = models.Role.objects.all().first()
        ser = RolesSerializer(instance=role, many=False)
        # ser.data  已经是转换完成的结果


        # 只是为了展示出来，序列化
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)

"""
class UserInfoSerializer(serializers.Serializer):
    username = serializers.CharField()
    # source指的就是对应数据库中的那个字段,内部执行一个判断，如果是可执行的就执行，如果不可执行，就直接拿结果
    xxxx = serializers.CharField(source='user_type') # 内部执行的  row.user_type
    oooo = serializers.CharField(source='get_user_type_display')  #row.get_user_type_display()
    password = serializers.CharField()
    gp = serializers.CharField(source='group.id')
    # rls = serializers.CharField(source='roles.all')
    # 当一个表中有choice的时候，可以使用source，ForeignKey的时候也可以使用source，
    # 但是如果有manytomany通过source是做不到那么细的粒度的
    rls = serializers.SerializerMethodField() # 自定义显示,将数据序列化

    def get_rls(self,row):
        '''
        函数名字必须是get开头，字段名称结尾
        :param row: 当前行的对象
        :return: 返回什么页面就会显示什么
        '''
        # 获取到所有的对象列表
        role_obj_list = row.roles.all()
        ret = []
        for item in role_obj_list:
            ret.append({'id':item.id,'title':item.title})
        return ret
"""

# 自定义类
class MyField(serializers.CharField):
    def to_representation(self, value):
        # value是从数据库中取到的值
        print(value)
        # 返回什么，页面就会显示什么
        return 'xxxx'






# 可以混合使用
class UserInfoSerializer(serializers.ModelSerializer):
    '''
    ModelSerializer帮助我们找到数据库中对象的字段，并将其转换成对应的field对象，只是做的简单的转换
    '''
    oooo = serializers.CharField(source='get_user_type_display')  # row.get_user_type_display()
    rls = serializers.SerializerMethodField()  # 自定义显示,将数据序列化
    group = serializers.CharField(source='group.id')
    x1 = MyField(source='username')
    class Meta:
        model = models.UserInfo
        # fields = '__all__'
        fields = ['id','username','password','oooo','rls','group']


    def get_rls(self, row):
        '''
        函数名字必须是get开头，字段名称结尾
        :param row: 当前行的对象
        :return: 返回什么页面就会显示什么
        '''
        # 获取到所有的对象列表
        role_obj_list = row.roles.all()
        ret = []
        for item in role_obj_list:
            ret.append({'id': item.id, 'title': item.title})
        return ret


class UserInfoSerializer(serializers.ModelSerializer):
    # 反向生成url,lookup_url_kwarg指的是url中的那个参数的值
    group = serializers.HyperlinkedIdentityField(view_name='gp',lookup_field='group_id',lookup_url_kwarg='pk')
    class Meta:
        model = models.UserInfo
        # fields = '__all__'
        fields = ['id','username','password','oooo','rls','group']
        # depth = 1 # 表示往里面拿几层数据，默认是0，建议0-3之间

serializers.CharField
class UserinfoView(APIView):
    def get(self,request):
        users = models.UserInfo.objects.all()
        # - 对象，Serializer类处理  self.to_representation（）
        # - QuerySet，是使用ListSerializer类处理  self.to_representation()
        # users要么是一个对象，要么就是QuerySet

        # 1.实例化，一般是将数据封装到对象，__new__()方法返回的是对象,然后执行返回值的__init__
        '''
       many=True ,接下来执行ListSerializer对象的构造方法，
       many=False, 接下来执行UserInfoSerializer对象的构造方法 
       '''
        ListSerializer
        ser = UserInfoSerializer(instance=users,many=True,context={'request':request})
        # 2.调用对象的data属性
        print(ser.data)
        ret = json.dumps(ser.data,ensure_ascii=False)
        return HttpResponse(ret)

    def post(self,request,*args,**kwargs):
        print(request.data)
        return HttpResponse('提交数据')




class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserGroup
        fields = '__all__'


class GroupView(APIView):
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        obj = models.UserGroup.objects.filter(pk=pk).first()
        ser = GroupSerializer(instance=obj,many=False)
        ret = json.dumps(ser.data,ensure_ascii=False)
        return HttpResponse(ret)

#########################验证##################################
# 自定义验证规则
class XValidator(object):
    def __init__(self,base):
        self.base = base
    def __call__(self,value):
        if not value.startswith(self.base):
            message = '标题必须以%s开头'%self.base
            raise serializers.ValidationError(message)

    def set_context(self, serializer_field):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # 执行验证之前调用,serializer_fields是当前字段对象
        pass


class UserGroupSerializer(serializers.Serializer):
    title = serializers.CharField(error_messages={'required':'标题不能为空'},validators=[XValidator('老女人'),])
    def validate_title(self,value):
        print(value)
        # 如果验证不通过
        # from rest_framework import exceptions
        # raise exceptions.ValidationError('看你不顺眼')
        # 验证通过
        return value

class UserGroupView(APIView):
    def post(self,request,*args,**kwargs):
        print(request.data)
        ser = UserGroupSerializer(data=request.data)
        # 数据校验，
        if ser.is_valid():
            print(ser.validated_data)
        else:
            print(ser.errors)
        return HttpResponse('提交数据')

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

class MyCursorPagination(CursorPagination):
    cursor_query_param = 'cursor'
    # 每页显示的个数
    page_size = 2
    ordering = 'id'
    # 每页现实的个数可以自定制
    page_size_query_param = None
    # 每页最多可以显示5个
    max_page_size = None


# 加密之后记住了当前id的最大值和最小值，第二次执行的时候，id就不扫描，直接跳到指定的位置
class Page1View(APIView):
    def get(self,request,*args,**kwargs):
        # 获取所有数据
        roles = models.Role.objects.all()
        # 创建分页对象
        pg = MyCursorPagination()
        # pg = PageNumberPagination()  # 默认的不可以自己设置每页显示的大小
        # 在数据库中获取分页的数据
        page_roles = pg.paginate_queryset(queryset=roles,request=request,view=self)
        # 对数据进行序列化
        ser  =  PagerSerializer(instance=page_roles,many=True)
        print(page_roles)

        # 默认给我们写好了上一页下一页，多少个,这里就必须使用这个，因为页码是加密的，我们不知道页码是多少没法通过页码自己获取
        return pg.get_paginated_response(ser.data)

'''
from rest_framework.generics import GenericAPIView
class View1View(GenericAPIView):
    queryset = models.Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination
    def get(self,request,*args,**kwargs):
        # 获取数据
        roles = self.get_queryset()
        # 分页
        page_roles = self.paginate_queryset(roles)
        # 序列化
        ser = self.get_serializer(instance=page_roles,many=True)

        return Response(ser.data)
'''
'''
from rest_framework.viewsets import GenericViewSet

class View1View(GenericViewSet):
    queryset = models.Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination
    def list(self,request,*args,**kwargs):
        # 获取数据
        roles = self.get_queryset()
        # 分页
        page_roles = self.paginate_queryset(roles)
        # 序列化
        ser = self.get_serializer(instance=page_roles,many=True)
        return Response(ser.data)
'''


from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.mixins import ListModelMixin,CreateModelMixin
# 可以完成增删改查了
class View1View(ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination


from rest_framework.renderers import JSONRenderer,BrowsableAPIRenderer,AdminRenderer,HTMLFormRenderer
class TestView(APIView):
    # renderer_classes = [JSONRenderer,BrowsableAPIRenderer]
    def get(self,request,*args,**kwargs):
        # 获取数据
        roles = self.get_queryset()
        # 分页
        page_roles = self.paginate_queryset(roles)
        # 序列化
        ser = self.get_serializer(instance=page_roles, many=True)

        return Response(ser.data)