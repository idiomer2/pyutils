""" 消息通知util
"""

import json
import requests


class Feishu:
    WEBHOOK_BASE_URL = 'https://open.feishu.cn/open-apis/bot/v2/hook/'
    HEADERS = {"Content-Type": "application/json"}
    def __init__(self, hook_token:str):
        self.token = hook_token.rsplit('/', 1)[-1]
        self.webhook_url = self.WEBHOOK_BASE_URL + self.token
    
    def _send_(self, payload):
        webhook_url, headers = self.webhook_url, self.HEADERS
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            resp_dict = response.json()
            print("✅ 飞书消息发送成功" if resp_dict.get('code') == 0 else f"❌ 发送失败: {str(resp_dict)}")
        else:
            raise Exception(response.text)

    def send_text(self, msg:str, at_all:bool=False):
        at_msg = '<at user_id="all">所有人</at>' if at_all else ''
        payload = {"msg_type":"text","content":{"text": msg + at_msg}}
        self._send_(payload)

    def send_markdown(self, title:str, markdown_content:str, footer:str=''):
        """
        发送 Markdown 格式消息到飞书

        Args:
            title (str): 卡片标题
            markdown_content (str): Markdown 内容文本
            footer: 脚注内容
        """
        footer = [{"tag": "hr"}, {"tag": "note", "elements": [{"tag": "plain_text", "content": footer}]}] if footer else []  # 分割线和底部注释（可选）
        payload = {
            "msg_type": "interactive",
            "card": {
                "config": {
                    "wide_screen_mode": True  # 开启宽屏模式，适合看长文
                },
                "header": {
                    "template": "blue",  # 标题颜色：blue, wathet, turquoise, green, yellow, orange, red, carmine, violet, purple, indigo, grey
                    "title": {"tag": "plain_text", "content": title}
                },
                "elements": [{"tag": "markdown", "content": markdown_content}] + footer
            }
        }
        self._send_(payload)

    def send_markdown_interactive(self, title:str, markdown_content:str, actions:list):
        """
        发送 markdown互动卡片 到飞书

        Args:
            title (str): 卡片标题
            content (str): 内容文本
            actions: 按钮列表，如 [
                {"tag":"button", "type":"primary", "text":{"content":"查看详情","tag":"plain_text"}, "url":"https://open.feishu.cn/"}, 
                {"tag":"button", "type":"default", "text":{"content":"查看活动指南","tag":"plain_text"}, "url":"https://open.feishu.cn/"}, 
            ]
        """
        payload = {
            "msg_type": "interactive",
            "card": {
                "config": {
                    "wide_screen_mode": True
                },
                "header": {
                    "template": "turquoise",
                    "title": {"tag": "plain_text", "content": title}
                },
                "elements": [
                    {"tag": "div", "text": {"tag": "lark_md", "content": markdown_content}},
                    {"tag": "action", "actions": actions}
                ]
            }
        }
        self._send_(payload)


class Pushme:
    WEBHOOK_BASE_URL = 'https://push.i-i.me'
    HEADERS = {'accept': '*/*', 'accept-encoding': 'gzip', 'accept-language': 'zh-CN,zh;q=0.9', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.160 Safari/537.36'}

    def __init__(self, push_key):
        self.token = push_key
        self.webhook_url = self.WEBHOOK_BASE_URL

    def _send_(self, payload):
        webhook_url, headers = self.webhook_url, self.HEADERS
        response = requests.post(webhook_url, headers=headers, data=payload)
        if response.status_code == 200:
            print("✅ Pushme消息发送成功" if response.text.lower() == 'success' else f"❌ 发送失败: {response.text}")
        else:
            raise Exception(response.text)

    def send_markdown(self, title, markdown_content):
        push_key = self.token
        payload = {'push_key':push_key, 'type': 'markdown', 'title': title, 'content': markdown_content}
        self._send_(payload)
