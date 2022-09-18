from typing import Any, Union
import httpx

from nonebot import require

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
from nonebot import get_bot
from aligo import Aligo, ShareFileSaveToDriveRequest
from nonebot import logger, on_command
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.internal.matcher import Matcher

ali = Aligo()  # 第一次使用，会弹出二维码，供扫描登录

GetCode = on_command("福利码")


class GetAlippChan:
    def __init__(self):
        self.url = 'https://api.aliyundrive.com/adrive/v1/timeline/homepage/list_message'
        self.list_url = 'https://api.aliyundrive.com/adrive/v3/file/list'
        self.token_url = 'https://api.aliyundrive.com/v2/share_link/get_share_token'
        self.oauth_url = 'https://aip.baidubce.com/oauth/2.0/token'
        self.ocr_url = 'http://tools.bugscaner.com/api/orc/'
        self.headers = {
            'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0)'
                ' Gecko/20100101 Firefox/75.0'
        }
        self.json_timeline = {
            "user_id": "ec11691148db442aa7aa374ca707543c",  # 阿里盘盘酱的用户ID
            "limit": 50,
            "order_by": "created_at",
            "order_direction": "DESC",
        }

    async def check(self) -> Union[str, None]:
        """判断阿里盘盘酱最新一条分享动态是否含有今日的掉落福利码，
        是则执行兑换任务，且兑换成功后不再执行兑换。否则不执行"""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                url=self.url,
                headers=self.headers,
                json=self.json_timeline
            )
            results = json.loads(resp.text)
            item = results['items'][0]  # 选择最新一条分享记录
            recent_action = item['display_action']
            content = item['content']
            share_id = content['share_id']
            parent_file_id = content['file_id_list'][0]
            if '掉落福利' in recent_action:
                logger.info('福利已找到，正在解析')
                share_token = self.get_share_token(
                    share_id=share_id
                )
                file_id = await self.get_file_id(
                    parent_file_id=parent_file_id,
                    share_id=share_id,
                    share_token=share_token
                )
                img_path = await self.download_file(
                    share_id=share_id,
                    file_id=file_id,
                    share_token=share_token
                )
                return img_path
            else:
                return None

    def get_share_token(
            self,
            share_id: str,
            share_pwd: str = ''
    ) -> str:
        """获取分享token，用于作为获取重定向链接的请求头参数"""

        json_share = {
            'share_id': share_id,
            'share_pwd': share_pwd
        }
        resp = httpx.post(
            url=self.token_url,
            headers=self.headers,
            json=json_share
        )
        token_json = json.loads(resp.text)
        share_token = token_json['share_token']
        logger.success('获取福利码分享token成功')
        return share_token

    async def get_file_id(
            self,
            parent_file_id: str,
            share_id: str,
            share_token: str
    ) -> str:
        """获取文件重定向链接"""
        async with httpx.AsyncClient() as client:
            json_filelist = {
                'parent_file_id': parent_file_id,
                'share_id': share_id
            }
            headers_filelist = {
                'user-agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64;'
                    ' x64; rv:75.0) Gecko/20100101 Firefox/75.0',
                'x-share-token': share_token
            }
            resp = await client.post(
                url=self.list_url,
                headers=headers_filelist,
                json=json_filelist
            )
            items = json.loads(resp.text)['items']
            file_id = items[0]['file_id']
            return file_id

    @staticmethod
    async def redirect(redirect_url: str) -> str:
        """进行重定向，获取文件真实下载链接 (暂时用不到)"""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                url=redirect_url
            )
            location = resp.headers['location']
            logger.success("获取文件真实下载链接成功")
            return location

    @staticmethod
    async def download_file(
            share_id: str,
            file_id: str,
            share_token: Any
    ) -> str:
        """将福利码图片保存到网盘并下载到本地"""
        body = ShareFileSaveToDriveRequest(
            share_id=share_id,
            file_id=file_id
        )
        save = ali.share_file_saveto_drive(
            body=body,
            share_token=share_token
        )
        the_file = save.file_id
        result = ali.download_file(
            file_id=the_file,
            local_folder='福利码'
        )  # 调用aligo下载福利码图片
        logger.success('福利码保存成功|%s' % result)
        return result  # 返回福利码本地路径

    async def ocr(self, filepath):
        """调用在线文字识别接口"""
        filename = '福利码.png'
        files = {
            'file': (filename, open(filepath, 'rb'), 'image/jpeg')
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                url=self.ocr_url,
                headers=self.headers,
                files=files
            )
            json_str = json.loads(resp.text)
            content = json_str['infos']
            cdk = re.findall('福利码：(阿里盘盘酱[\w]{5})', content)[0]
            return cdk


@GetCode.handle()
async def give_me(matcher: Matcher):
    state = await GetAlippChan().check()
    if '福利码' in state:
        cdk = await GetAlippChan().ocr(state)
        await matcher.send(MessageSegment.image('file:///' + state))
        await matcher.send(cdk)
        results = ali.rewards_space(cdk).message
        await matcher.send("操作成功~兑换结果：\n" + results)
    else:
        await matcher.finish("暂时没有福利码可以获取")


@scheduler.scheduled_job("cron", second="*/5", id="job_0")
async def auto_run():
    group_id = 'xxxxxxxxx'  # 这里填写发送消息的群号
    bot = get_bot()
    state = await GetAlippChan().check()
    if state:
        cdk = await GetAlippChan().ocr(state)
        await bot.send_group_msg(
            group_id=group_id,
            message=MessageSegment.image('file:///' + state)
        )
        await bot.send_group_msg(
            group_id=group_id,
            message=cdk
        )
        results = ali.rewards_space(cdk).message
        await bot.send_group_msg(
            group_id=group_id,
            message="操作成功~兑换结果：\n" + results
        )
        scheduler.pause()
    else:
        pass
