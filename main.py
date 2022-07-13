'''
Author: fantiga
Date: 2022-07-06 09:08:13
LastEditTime: 2022-07-13 12:50:50
LastEditors: fantiga
Description: 
FilePath: /futu-qta/main.py
'''

from utils import *

# 主函数
if __name__ == '__main__':
    # 初始化策略
    if not on_init():
        print('策略初始化失败，脚本退出！')
        quote_context.close()
        trade_context.close()
    else:
        # 设置回调
        quote_context.set_handler(OnTickClass())
        quote_context.set_handler(OnBarClass())
        trade_context.set_handler(OnOrderClass())
        trade_context.set_handler(OnFillClass())

        # 订阅标的合约的 逐笔，K 线和摆盘，以便获取数据
        quote_context.subscribe(code_list=[TRADING_SECURITY], subtype_list=[
                                SubType.TICKER, SubType.ORDER_BOOK, TRADING_PERIOD])
