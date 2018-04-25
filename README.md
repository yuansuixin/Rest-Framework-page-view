Rest-Framework部分自定义组件解析
======

## 分页

- 分页，看第n页，每页显示n条数据

- 分页，在n个位置，向后查看n条数据

- 加密分页，上一页和下一页



## 视图

- 之前，View

- 现在，APIView


- 无用  GenericAPIView


- 多继承`class GenericViewSet(ViewSetMixin, generics.GenericAPIView):`  GenericViewSet重写了`as_view（）`方法

- ModelViewSet


##### 总结
- 增删改查  ModelViewSet
- 增删  CreateModelMixin,DestroyModelMixin,GenericViewSet
- 复杂的逻辑  GenericViewSet或APIView

- 权限
    - 使用到mixins.RetrieveModelMixin的时候，会执行源码中的retrieve（），在这里面调用了get_object（）
    - 根据层级找上去，我们会在GenericAPIView类中找到get_object（），在这个方法里调用check_object_permissions（）来判断这个对象是否有权限，照比我们之前对所有的权限来说，更细粒度了
    - 在这个方法里，调用get_permissions（）方法，循环拿到permission，调用has_object_permission（）
    - 只有调用get_object（）的时候has_object_permission（）才会被调用，不然永远不会调用
```
    GenericAPIView.get_object
       check_object_permissions
	       has_object_permission
```


## 路由

- ` url(r'^(?P<version>[v1|v2]+)/users/$',views.UsersView.as_view(),name='uuu')`
- ` url(r'^(?P<version>[v1|v2]+)/view1/$',views.View1View.as_view({'get':'list','post':'create'})),`

- 根据传入的url不同，渲染器渲染的也不同，一个url可以写成4个


- 自动生成路由


## 渲染器

- 视图里面可以添加renderer_classes,也可以在配置中添加


[中文文档详细解析](https://yuansuixin.github.io/2018/05/01/rest-viewset/ "详细解析")













