'''
Author: fantiga
Date: 2022-07-06 09:08:13
LastEditTime: 2022-07-26 11:01:09
LastEditors: fantiga
Description: 主程序
FilePath: /futu-qta/main.py
'''

from utils.utils import *
import pandas as pd


# 计算VWAP的方法
def vwap(df):
    v = df['volume'].values
    tp = (
        df['low_price'] +
        df['prev_close_price'] +
        df['high_price']
    ).div(3).values
    return df.assign(vwap=(tp * v).cumsum() / v.cumsum())


class StockQuoteTest(StockQuoteHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(StockQuoteTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("StockQuoteTest: error, msg: %s" % data)
            return RET_ERROR, data
        # print("StockQuoteTest ", data)  # StockQuoteTest 自己的处理逻辑

        ret, data = quote_context.get_stock_quote(TRADING_SECURITY)
        if ret == RET_OK:
            stock_data = pd.DataFrame(
                index=['%s %s' % (data['data_date'][0], data['data_time'][0])],
                data={
                    "last_price": data['last_price'][0],
                    "amplitude": data['amplitude'][0],
                    "high_price": data['high_price'][0],
                    "low_price": data['low_price'][0],
                    "prev_close_price": data['prev_close_price'][0],
                    "volume": data['volume'][0]
                }
            )
            stock_data.index.rename('datetime', inplace=True)
            stock_data = vwap(stock_data)
            stock_data.drop(columns='high_price', inplace=True)
            stock_data.drop(columns='low_price', inplace=True)
            stock_data.drop(columns='prev_close_price', inplace=True)
            print(stock_data)
        else:
            print('ret_error:', data)
        return RET_OK, data


# 主函数
if __name__ == '__main__':
    # 初始化策略
    if not on_init():
        print('策略初始化失败，脚本退出！')
        quote_context.close()
        trade_context.close()
    else:
        # 设置回调
        # quote_context.set_handler(OnTickClass())
        # quote_context.set_handler(OnBarClass())
        # trade_context.set_handler(OnOrderClass())
        # trade_context.set_handler(OnFillClass())

        # quote_context.set_handler(StockQuoteHandlerBase())

        handler = StockQuoteTest()
        quote_context.set_handler(handler)  # 设置实时报价回调
        # 订阅实时报价类型，FutuOpenD 开始持续收到服务器的推送
        # quote_context.subscribe(['HK.00700'], [SubType.QUOTE])

        # 订阅标的合约的 逐笔，K 线和摆盘，以便获取数据
        quote_context.subscribe(
            TRADING_SECURITY, SUBTYPE_LIST)

        # pass
