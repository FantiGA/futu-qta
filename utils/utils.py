'''
Author: fantiga
Date: 2022-07-13 12:42:55
LastEditTime: 2022-07-25 10:18:48
LastEditors: fantiga
Description: 实用类包
FilePath: /futu-qta/utils/utils.py
'''

from .policy import *

################################ 框架实现部分，可忽略不看 ###############################

# 行情 - 逐笔推送
class OnTickClass(TickerHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        on_tick()


# 行情 - K 线推送
class OnBarClass(CurKlineHandlerBase):
    last_time = None

    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(OnBarClass, self).on_recv_rsp(rsp_pb)
        if ret_code == RET_OK:
            cur_time = data['time_key'][0]
            if cur_time != self.last_time and data['k_type'][0] == TRADING_PERIOD:
                if self.last_time is not None:
                    on_bar_open()
                self.last_time = cur_time


# 交易 - 订单更新
# class OnOrderClass(TradeOrderHandlerBase):
#     def on_recv_rsp(self, rsp_pb):
#         ret, data = super(OnOrderClass, self).on_recv_rsp(rsp_pb)
#         if ret == RET_OK:
#             on_order_status(data)


# 交易 - 成交更新
# class OnFillClass(TradeDealHandlerBase):
#     def on_recv_rsp(self, rsp_pb):
#         ret, data = super(OnFillClass, self).on_recv_rsp(rsp_pb)
#         if ret == RET_OK:
#             on_fill(data)
