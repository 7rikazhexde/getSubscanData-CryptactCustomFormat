# getSubscanData-CryptactCustomFormat
Subscan APIを使用して取引履歴を取得してクリプタクトのカスタムファイルフォーマットでcsvファイル保存するソースコード

### 対象
* クリプタクトの[暗号資産の損益計算サービス](https://support.cryptact.com/hc/ja/categories/115000455551-%E4%BB%AE%E6%83%B3%E9%80%9A%E8%B2%A8%E3%81%AE%E6%90%8D%E7%9B%8A%E8%A8%88%E7%AE%97%E6%A9%9F%E8%83%BD-%E4%BD%BF%E3%81%84%E6%96%B9)を利用し、データをクリプタクトの[カスタムファイルのフォーマット](https://support.cryptact.com/hc/ja/articles/360002571312-%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%A0%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AE%E4%BD%9C%E6%88%90%E6%96%B9%E6%B3%95)で作成している
* Subscanでデータを取得している

### 前提条件
* Subscan APIの[API Keys](https://docs.api.subscan.io/#introduction)を取得済みであること

### 仕様
* 取得するデータは`reward-slash`を対象とし、コマンドラインから読込み件数（正の数）を入力する
* 取得するデータPythonのRequestsモジュールを使用して、[Subscan APIドキュメント](https://docs.api.subscan.io/#introduction)に従い設定したAPI Endpoint情報でHTTPのPOSTメソッドで送信し、Responseオブジェクトの`status_code`が`HTTP Status Codes: 200`の場合に受信したデータをJSONオブジェクトとして保存する
* `HTTP Status Codes: 200`以外の値の場合は`status_code`を表示し、プログラムを終了する
* 取得したデータは[カスタムファイルのフォーマット仕様](https://support.cryptact.com/hc/ja/articles/360002571312-%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%A0%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AE%E4%BD%9C%E6%88%90%E6%96%B9%E6%B3%95)で整形し、指定したパスにcsvファイルとして保存する
* ファイルの書き出し方法として新規作成と既存ファイルに追記する2つのケースに対応し、それぞれソースコードを作成する

### 注意事項
* Subscanの仕様やクリプタクトのデータフォーマットは変わることがありますので、利用する際は**自己責任**でお願いします
* データのチェックとして重複は考慮していますが、不足しているデータのチェックまではしていません
* Subscan APIで動作確認したNetworkは**Polkadot**のみ確認しています
* 特に作成したcsvファイルのデータについては**目的のデータを作成できていること**、
  トランザクションデータを参照して、**差異がないこと**や**誤りがないこと**も確認してください

### 使い方
#### 事前準備
##### モジュールのインストール
* requestsモジュールとnumpyモジュールをインストール
```
pip install requests
pip install numpy
```
##### 設定情報の作成(setting.py)
###### Subscan API情報
* API Host：`API_HOST` 
* Request URL：`REQUEST_URL`
* API Key:`API_KEY`
* Address:`ADDRESS`
###### ファイル情報
* File Path:`PATH`
* File Name:`FILE_NAME`
###### クリプタクトカスタムファイル用データ情報
[カスタムファイルのフォーマット](https://support.cryptact.com/hc/ja/articles/360002571312-%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%A0%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AE%E4%BD%9C%E6%88%90%E6%96%B9%E6%B3%95)に従い作成してください
* ステーキング報酬計算用定数:`ADJUST_VALUE`
  ※ Subscanや各種walletの取引履歴と差異がある場合は修正してください
* ヘッダー情報(リスト):`HEADER`
* データ固定値:`ACTION`,`SOURCE`,`BASE`,`PRICE`,`COUNTER`,`FEE`,`FEECCY`
  ※ 空データの場合は`NaN`を指定してください

#### ソースコードの実行
##### <ケース1>csvファイルを新規作成する場合
```
python getSubscanStakingRewardsInpuNewCreateCsvData.py
```
##### <ケース2>既存のcsvファイルに追記する場合
```
python getSubscanStakingRewardsInpuAddCsvData.py
```
#### 件数の入力
* 以下のメッセージ表示後、**正の数**で件数を入力してください
* ステーキング報酬量は直近のデータから入力された件数分取得します
```
 -- Input Num: 
```

#### 処理について
##### 共通処理
* 取得件数の入力処理
* データは[Subscan APIドキュメント](https://docs.api.subscan.io/#introduction)に従い設定したAPI Endpoint情報でHTTP POSTし、Responseが`HTTP Status Codes: 200`の場合に受信したデータをJSON形式で抽出処理を実行します
* `HTTP Status Codes: 200`以外の値の場合はHTTPステータスコードを表示し、プログラムを終了します
* csvファイル保存処理（ファイルパス表示）

##### 依存処理（ケース1）
* 設定したパス、ファイル名、日付でcsvファイルを作成します
* ファイルが存在する場合は上書き保存します
##### 依存処理（ケース2）
* ファイルが存在する場合は追記処理をします
* データに重複がある場合は完全一致のデータを参照し、重複行を削除します