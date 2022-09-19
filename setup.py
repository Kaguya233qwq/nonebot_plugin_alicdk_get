from setuptools import setup

setup(
    name='包的名字',
    version='1.0',
    author='neet姬辉夜大人',
    author_email='1435608435@qq.com',
    url='https://github.com/Kaguya233qwq/nonebot2-plugin-AliCDK-get',
    description='基于nonebot2与Aligo的阿里云盘兑换码自动获取和兑换插件',
    long_description='1.pip命令安装本插件。'
                     '2.第一次启动会弹出二维码，请使用阿里云盘app授权登录。'
                     '3.设置定时任务执行时间间隔，可根据自己的需求修改'
                     '4.修改接收bot消息的群号，兑换成功将会通知您'
                     '5.守株待兔。',
    packages=['nonebot-plugin-AliCDK-get', ''],
    install_requires=['aligo', 'nonebot_plugin_apscheduler', 'httpx'])
