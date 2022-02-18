import json
import requests
import datetime
import pandas as pd
from settings import *
from docs import *

def main():
      # 取得件数入力
      input_num = int(input(' -- Input Num: '))

      # ヘッダー作成
      df_new = pd.DataFrame(columns=HEADER)

      print(' -- API Endpoint: ' + API_HOST + REQUEST_URL)

      # Subscan APIを使用しrequestsモジュールでPOSTリクエストする
      # header情報
      headers_dict = {
            'Content-Type': 'application/json',
            'X-API-Key': API_KEY,
      }

      # data-raw情報
      # 1ページ25件だがrowの指定のみでlistの情報は取得できるためpageは0固定とする
      data_dict = { 'row': 0, 'page': 0, 'address': ADDRESS }
      # 件数で上書き
      data_dict['row'] = input_num

      # Staking API / rewards-slash指定
      response = requests.post(API_HOST+REQUEST_URL, headers=headers_dict, data=json.dumps(data_dict))

      # HTTPステータスコード確認
      if response.status_code == 200:
            print(' -- HTTP Status Codes:',response.status_code)
      else:
            print(' -- HTTP Status Codes:',response.status_code)
            print(' -- Check Subscan API Documents: ' + SUBSCAN_API_DOC)
            print(' -- quit()')
            quit()

      # レスポンスデータ(JSON形式)
      response_json = response.json()

      # 1件数ずつ処理する
      for i in range(input_num):
            # block_timestamp取得(csv:Timestamp)
            block_timestamp = response_json['data']['list'][i]['block_timestamp']
            # UTC(日本時間)以外にする場合はtimedeltaオブジェクトで調整すること。
            dt_block_timestamp = datetime.datetime.fromtimestamp(block_timestamp)
            # フォーマット変更
            dt_block_timestamp_fmt = dt_block_timestamp.strftime('%Y/%m/%d %H:%M:%S')
            # 0埋め表記を有効にするためシングルコーテーションを付ける
            dt_block_timestamp_fmt = "'" + dt_block_timestamp_fmt
            # ステーキング報酬取得(csv:Volume)
            amount = response_json['data']['list'][i]['amount']
            # 報酬量調整
            amount_float = float(amount) * ADJUST_VALUE
            # event_index取得(csv:Comment)
            event_index = response_json['data']['list'][i]['event_index']
            # csvファイル書き用データを作成
            value = [dt_block_timestamp_fmt,ACTION,SOURCE,BASE,amount_float,PRICE,COUNTER,FEE,FEECCY,event_index]

            # DataFrame作成
            # 行データを追加する
            df_new.loc[i, :] = value
            # Volumeの表示桁数調整
            df_new['Volume'] = df_new['Volume'].astype(float)
            df_new = df_new.round({'Volume':10})
            # Feeの型変換
            df_new['Fee'] = df_new['Fee'].astype(int)

      # ファイル書き出し処理
      # Timestamp列で昇順にソート
      df_csv = df_new.sort_values('Timestamp')
      # プログラム実行時の日付を取得
      dt_today = datetime.date.today()
      # ファイル名を日付指定で保存
      filename = FILE_NAME + '_' + str(dt_today) + '.csv'
      # index指定なしでファイル書き出し
      df_csv.to_csv(PATH + filename,index = False)
      print(' -- Save Location: ['+ PATH +  filename + ']\n')

if __name__ == '__main__':
      main()
