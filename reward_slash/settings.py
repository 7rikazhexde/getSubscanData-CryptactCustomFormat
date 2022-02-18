from numpy import NaN

# Subscan API情報
# API Host
API_HOST = 'https://polkadot.api.subscan.io'
# Request URL
REQUEST_URL = '/api/scan/account/reward_slash'
# API Key
API_KEY = '''YOUR SUBSCAN APIKEY'''
# Address
ADDRESS = '''YOUR DDRESS'''
# File Path
PATH = './'
# File Name
FILE_NAME = 'cryptact_custum'

# ステーキング報酬計算用定数
# 計算後の値（ステーキング報酬量）は必ずSubscanのcsvファイルと一致することを確認してください。
ADJUST_VALUE = 0.0000000001

# ヘッダー情報(詳細はCryptactカスタムファイル形式参照)
HEADER = ['Timestamp', 'Action', 'Source', 'Base', 'Volume', 'Price', 'Counter', 'Fee', 'FeeCcy', 'Comment']

# 固定値
ACTION  = 'STAKING'
SOURCE  = '''YOUR SOURCE NAME'''
BASE    = '''YOUR NETWORK'''
PRICE   = NaN
COUNTER = 'JPY'
FEE     = 0
FEECCY  = 'JPY'