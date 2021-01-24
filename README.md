# Python 语言基础项目技术文档

## 一、项目介绍

### 1. 项目标题与简介
项目标题：豆瓣影视数据分析及可视化平台

项目简介：
- 这是一个将豆瓣上影视数据进行整合、分类并可视化的平台。适用于对影视方向热爱并想对数据进行一定研究的人群。豆瓣平台一般是数字的展现，而此平台直观的用**不同可视化类型图表+数字注释**将各类数据展示出来。  
- 其中有如下可视化数据+图表：  
国家电影分布、电影趋势、电影时长占比、评论数前10电影、电影行业近些年的发展状况、电影类型分布情况。  
![结构分布图](https://images.gitee.com/uploads/images/2021/0124/122329_91686d7b_5330597.png "WechatIMG1925.png")

### 2. 问题表述
**用户画象**：用于影视爱好者，特别是对影视分布、发展趋势等有了解倾向的用户。   
**用户使用场景**：在看完一部电影后对此类电影发展势头好奇，打开可视化平台查看；想要了解电影行业近些年的发展状况，以及电影类型分布情况，直观在平台中看到豆瓣电影的数据及各个指标的情况。  
**用户任务**：用户无需过多的操作的操作，打开数据可视化的页面时，页面会自动请求数据，进行渲染图表等操作。  
**用户痛点**：用户不能很好的进行扩展，只能观看后台设定好的图表和样式。  
**产品益点**：对于数据分析的结果非常直观，能很好的了解数据背后的趋势和分布情况，并且对数据探索爱好者能过提供一些数据支撑。  

---

## 二、解决方案

### 1. 项目规划与知识点
项目的后端框架为flask，数据存储为mysql，以及前端的页面展示通过bootstr、html、js、css等进行前端页面的展示，主要实现的功能有登陆、注册、数据可视化、个人信息修改等功能。  
下面是各个功能所需要的基础知识：
![知识图谱](https://images.gitee.com/uploads/images/2021/0124/122350_01a9fa41_5330597.png "WechatIMG1926.png")

### 2. 编程功能的基本描述
- 介绍的功能主要有登陆、注册、数据可视化、个人信息修改：
- 登陆界面
```html
<div style="text-align: center;">
      <label style="text-align: center;font-size:20px;margin-bottom: 20px;">用户登陆</label>
    </div>
    <br>
     <div class="layui-form-item" style="text-align: center">
    <div class="layui-inline">
      <label class="layui-form-label">学号</label>
      <div class="layui-input-inline">
        <input style="width:250px" type="tel" name="username" lay-verify="required|phone" autocomplete="off" class="layui-input" placeholder="输入账号">
      </div>
    </div>
    <div class="layui-inline">
      <label class="layui-form-label">密码</label>
      <div class="layui-input-inline">
        <input style="width:250px" type="password" name="password" lay-verify="email" autocomplete="off" class="layui-input" placeholder="输入密码"><p style="color:red">{{message}}</p>
      </div>
    </div>
    <br>
  </div>
    <div style="text-align: center;margin-bottom: 40px;border-radius: 8px;">
        <div  >
    <button type="submit" class="layui-btn layui-btn-primary layui-btn-sm">登陆</button>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
    <a href="/user/regiest"><button type="button"  class="layui-btn layui-btn-primary layui-btn-sm">注册</button> </a>
 </div>
    </div>
```
- 登陆处理
```python
@blue.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template('login.html',context=None)
    name=request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter(User.phone_number==name).first()
    if not user:
        return render_template('login.html',message='账户不存在')
    else:
        if not user.password==password:
            return render_template('login.html', message='密码不正确')
    resp = make_response(redirect('index'))
    resp.set_cookie('u_id', str(user.id))
    return resp
```

- 注册页面
```html
<div class="layui-form-item" style="text-align: center">
    <div class="layui-inline">
      <label class="layui-form-label">昵称</label>
      <div class="layui-input-inline">
        <input style="width:250px" type="tel" name="name" lay-verify="required|phone" autocomplete="off" class="layui-input" placeholder="输入昵称">
      </div>
    </div>
        <div class="layui-form-item" style="text-align: center">
    <div class="layui-inline">
      <label class="layui-form-label">手机</label>
      <div class="layui-input-inline">
        <input style="width:250px" type="tel" name="phone" lay-verify="required|phone" autocomplete="off" class="layui-input" placeholder="输入手机号">
      </div>
    </div>
            <div class="layui-inline">
      <label class="layui-form-label">密码</label>
      <div class="layui-input-inline">
        <input style="width:250px" type="password" name="password" lay-verify="email" autocomplete="off" class="layui-input" placeholder="设置密码">
      </div>
<p style="color:red">{{message}}</p>
    </div>
  </div>
    <div style="text-align: center;margin-bottom: 40px">
        <div  >
    <button type="submit" class="layui-btn layui-btn-primary layui-btn-sm">注册</button>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
    <a href="/user/login"><button type="button" class="layui-btn layui-btn-primary layui-btn-sm" >返回</button> </a>
 </div>
    </div>
```
- 注册处理
```python
user=User()
user.name=name
user.phone_number=phone
user.password=password
user.user_type=1
db.session.add(user)
db.session.commit()
```
- 数据可视化ajax代码
```js
 $.ajax({
             type: "GET",
             url: "http://127.0.0.1:5000/user/get_data",
             success: function(data){
             var data1=data
                echarts_1();
                echarts_2();
                echarts_3();
                echarts_4();
                echarts_5();
                map();

```

- 数据可视化获取数据
```python
@blue.route('/get_data', methods=['GET', 'POST'])
def get_data():
    data=json.loads(json.dumps(get_dic(), cls=NpEncoder))
    return data

```

- 个人信息修改
```html
<div class="layui-form-item" style="text-align: center">
    <div class="layui-inline">
      <label class="layui-form-label">账户</label>
      <div class="layui-input-inline">
        <input readonly="readonly" style="width:250px" type="tel" name="phone_number" lay-verify="required|phone" autocomplete="off" class="layui-input" value="{{data.score.phone_number}}" placeholder="输入账户">
      </div>
    </div>
        <input style="display:none" name="score_id" value="{{data.score.id}}">
  </div>
        <div class="layui-form-item" style="text-align: center">
    <div class="layui-inline">
      <label class="layui-form-label">密码</label>
      <div class="layui-input-inline">
        <input style="width:250px" type="password" name="password" lay-verify="required|phone" autocomplete="off" class="layui-input" value="{{data.score.password}}">
      </div>
    </div>
            {% if data.message %}
<p style="color:red">{{data.message}}</p>
            {%else %}
            <p style="color:red"></p>
            {% endif %}
  </div>
    <div style="text-align: center;" >
        <div  >
    <button  type="submit" class="layui-btn" id="tj_btn">修改</button>
```

- 个人信息修改处理
```python
@blue.route('/reset_pwd', methods=['GET', 'POST'])
def admin_upreset_pwddate():
    u_id = request.cookies.get('u_id')
    score=User.query.filter(User.id==u_id).first()
    if request.method=='GET':
        return render_template('info_edit.html',data={'score':score,'message':None})
    phone=request.form.get('phone_number')
    password=request.form.get('password')
    score.phone_number=phone
    score.password=password
    db.session.add(score)
    db.session.commit()
    return render_template('info_edit.html', data={'score':score,'message':'修改成功！'})

```

知识点 | HTML表单、HTTP 请求 | 数据库 | 条件判断语句、 for 循环语句 | 字典、列表 | 自定义模块的使用 | Flask 第三方模块的使用
---|---|---|---|---|---|---
学习成本（天） | 2 | 6 | 3 | 4 | 3 | 6 
应用比例 | 8% | 25% | 12.5% | 16% | 12.5% | 25%

### 3. 云端项目部署的基本描述

#### 3.1 页面链接与页面功能介绍
**主要功能**

- 登陆：http://127.0.0.1:5000/user/login
- 注册：http://127.0.0.1:5000/user/regiest
- 可视化图表：http://127.0.0.1:5000/user/index
- 用户管理：http://127.0.0.1:5000/user/user_manager
- 用户搜索：http://127.0.0.1:5000/user/user_manager?keywords=
- 用户删除：http://127.0.0.1:5000/user/admin_delete?u_id=
- 用户编辑：http://127.0.0.1:5000/user/edit_user?u_id=
- 密码修改：http://127.0.0.1:5000/user/reset_pwd
- 退出登陆：http://127.0.0.1:5000/user/login_out

可视化图表中**一个页面嵌套了多个页面**。

#### 3.2 数据流程图
![数据流程图](https://images.gitee.com/uploads/images/2021/0124/122413_64bc0a0f_5330597.png "WechatIMG1927.png")


#### 3.3 云端功能 
主要实现的功能有登陆、注册、数据可视化、个人信息修改等功能，且所有数据都保存于独立数据库mysql。

#### 3.4 部署心得 

1. 项目刚开始开发的时候，文件配置是个大问题，配置了之后初始化项目无法运行，后面经过网上查询得知项目正确的[配置](https://www.cnblogs.com/zhaohuhu/p/9218127.html)方式。

2. 提交表单的时候总是出现[400](https://www.cnblogs.com/vinic-xxm/p/11690070.html)bad request，后面在网上查询得知表单提交数据需要添加csrf_token这个数据才能正确的提交表单，目的是为了解决跨域问题。




## 三、学习/实践心得总结及感谢
通过这次的flask项目实践，让我对python的知识更加了解，在项目编写过程中，我充分的使用了字典，列表，元组等基本的语法和操作，功能逻辑方面可能有些缺陷，但是这次的实践让我收获最大的还是解决问题的方法，当我们遇到问题的时候，可以通过互联网自行解决问题，同时做好记录解决问题的过程，下次遇到同类型问题就能迎刃而解。
