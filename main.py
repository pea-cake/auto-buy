import uiautomator2 as u2
import requests
import json
import time

'''
  自动抢菜v1.0.0
  by peacake
  ...
'''

d = u2.connect('192.168.137.145:5555')  # 连接设备
key = ''  # 企业微信机器人链接中key


def sendmsg(msg):
    # 企业微信机器人通知
    data = {
        "msgtype": "text",
        "text": {
            "content": msg
        }
    }
    requests.post(
        'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key='+key, json.dumps(data))


def buy():
    d.xpath('//*[@resource-id="com.yaya.zone:id/tv_submit"]').click()
    time.sleep(4)
    pay_button = d.xpath(
        '//*[@resource-id="com.alipay.android.app:id/flybird_layout"]')
    pay_button_exists = pay_button.exists
    if pay_button_exists:
        sendmsg('🎉🎉🎉恭喜，购买成功了！')
    else:
        d.xpath(
            '//*[@resource-id="com.yaya.zone:id/iv_dialog_select_time_close"]').click()
        d.press("back")
        run()


def start():
    select_time = d.xpath('//*[@text="请选择送达时间"]')
    select_time_exists = select_time.exists
    if select_time_exists:
        select_time.click()
        hasfull = d.xpath(
            '//*[@resource-id="com.yaya.zone:id/rv_selected_day"]/android.widget.LinearLayout[1]/android.widget.TextView[2]').exists  # 今天已满
        if hasfull:
            print('今天已满')
            # 关闭时间弹框
            d.xpath(
                '//*[@resource-id="com.yaya.zone:id/iv_dialog_select_time_close"]').click()
            d.press("back")
            run()
        else:
            print('可以买')
            for elem in d.xpath('//*[@resource-id="com.yaya.zone:id/rv_selected_hour"]/android.view.ViewGroup').all():
                if elem.attrib['enabled'] == 'true':
                    elem.click()
                    break
                else:
                    print('no')
            buy()
    else:
        buy()


def run():
    # 购物车
    d.xpath('//*[@resource-id="com.yaya.zone:id/ani_car"]').click()
    # 全选
    all_button = d.xpath('//*[@resource-id="com.yaya.zone:id/cb_all"]')
    if all_button.attrib['checked'] == 'false':
        all_button.click_exists(timeout=4.0)
    print('checked', (all_button.attrib['checked']))
    if all_button.attrib['checked'] == 'true':
        # 去结算
        # d(resourceId="com.yaya.zone:id/btn_submit").click()
        d.xpath('//*[@resource-id="com.yaya.zone:id/btn_submit"]').click()
        start()
    else:
        # sendmsg('购物车全失效')
        print('购物车全失效')

run()
