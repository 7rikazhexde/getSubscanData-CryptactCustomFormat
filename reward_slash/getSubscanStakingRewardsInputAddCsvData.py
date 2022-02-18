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
      df_base = pd.DataFrame(columns=HEADER)
      df_add = pd.DataFrame(columns=HEADER)

      # 書き出し用ファイルチェック
      try:
            # ファイルが存在する場合
            filename = FILE_NAME + '.csv'
            df_base = pd.read_csv(filename)
      except FileNotFoundError:
            # ファイルが存在しない場合
            print(' -- No such file or directory: New Create ['+ filename + ']')
      except pd.errors.EmptyDataError:
            # ファイルは存在するが中身が空の場合
            print(' -- Empty csv file!: Add Data to ['+ PATH +  filename + ']')
      except:
            # 上記以外のケースの場合はエラーを表示しプログラムを終了する
            print(' -- Check Pandas API Reference: ' + PANDAS_DOC_READ_CSV)
            print(' -- quit()')
            quit()

      print(' -- API Endpoint: ' + API_HOST + REQUEST_URL)

      # Subscan APIを使用しrequestsモジュールでPOSTリクエストする
      # header情報
      headers_dict = {
            'Content-Type': 'application/json',
            'X-API-Key': API_KEY,
      }

      # data-raw情報
      # rowの指定のみでlistの情報は取得できるためpageは0固定とする
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
            df_add.loc[i, :] = value
            # Volumeの表示桁数調整
            df_add['Volume'] = df_add['Volume'].astype(float)
            df_add = df_add.round({'Volume':10})
            # Feeの型変換
            df_add['Fee'] = df_add['Fee'].astype(int)

      # データを結合する
      df_cc = pd.concat([df_base,df_add])
      # 重複行を削除する
      df_cc = df_cc.drop_duplicates()
      # Timestamp列で昇順にソート
      df_csv = df_cc.sort_values('Timestamp')
      # index指定なしでファイル書き出し
      df_csv.to_csv(PATH + filename, index = False)
      print(' -- Save Location: ['+ PATH +  filename + ']\n')

if __name__ == '__main__':
      main()
