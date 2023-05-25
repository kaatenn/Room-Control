# 项目名称 - 环境部署教程

本篇教程提供了如何在你的本地或服务器上部署项目的详细步骤。该项目是基于Node.js和Python等语言开发的，并使用Vue、Django等框架

## 环境要求

在执行本教程中的步骤之前，确保你已经准备好了以下环境：

- npm：确保你已经安装了版本为 9.6.5 的 npm；
- Python：确保你已经安装了版本为 3.9.13 的 Python。

1. **克隆项目到本地**
   `git clone https://github.com/kaatenn/Room-Controll.git`
2. **安装依赖包**
   1. 首先进入controll_front目录（别问为什么control拼错了，原来的项目目录叫controller，忘记多删一个l了，懒得改了），执行`npm install`
   2. 可以的话请使用yarn执行上述操作
   3. 进入controll_back
   4. 执行`pip install -r requirements.txt`
3. **启动项目**
   1. 执行`npm run dev`打开前端页面
   2. 执行`python manage.py runserver 8000`即可运行后端

## 测试

在启动项目后，可以通过以下 URL 来访问项目：

- http://localhost:80

## 注意事项

- 在添加环境变量时，请根据实际情况设置变量名和变量值；
- 在实际使用时，请修改项目名称和相关信息。