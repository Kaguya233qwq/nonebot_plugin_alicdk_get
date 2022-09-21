import setuptools

with open("README.md", "r", encoding="utf-8", errors="ignore") as f:
    long_description = f.read()
setuptools.setup(
    name='nonebot-plugin-alicdk-get',
    version='1.0',
    author='Kaguya233qwq',
    author_email='1435608435@qq.com',
    keywords=["pip", "nonebot2", "nonebot", "alidrive", "nonebot_plugin"],
    url='https://github.com/Kaguya233qwq/nonebot_plugin_alicdk_get',
    description='''nonebot2 plugin alicdk get''',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    platforms="any",
    install_requires=[
        'aligo>=5.4.0', 'nonebot_plugin_apscheduler', 'httpx',
        'nonebot2>=2.0.0-beta.1', 'nonebot-adapter-onebot>=2.0.0-beta.1'
    ])
