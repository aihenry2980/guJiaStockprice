'''
Author: your name
Date: 2021-09-03 12:57:16
LastEditTime: 2021-09-22 14:47:02
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \guJiaStockprice\main.py
'''
import pandas as pd
import requests

#해당 링크는 한국거래소에서 상장법인목록을 엑셀로 다운로드하는 링크입니다.
#다운로드와 동시에 Pandas에 excel 파일이 load가 되는 구조입니다.
# stock_code = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
stock_code = pd.read_excel('fix.xlsx')

# 데이터에서 정렬이 따로 필요하지는 않지만 테스트겸 Pandas sort_values를 이용하여 정렬을 시도해봅니다.
stock_code.sort_values(['상장일'], ascending=True)

# 필요한 것은 "회사명"과 "종목코드" 이므로 필요없는 column들은 제외
stock_code = stock_code[['회사명', '종목코드']]

# 한글 컬럼명을 영어로 변경
stock_code = stock_code.rename(columns={'회사명': 'company', '종목코드': 'code'})
#stock_code.head()

# 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
stock_code.code = stock_code.code.map('{:06d}'.format)

# stock_code.head()

#########################################################################################################
# LG화학의 일별 시세 url 가져오기
company='LG화학'
code = stock_code[stock_code.company==company].code.values[0].strip() ## strip() : 공백제거
page = 1

url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
url = '{url}&page={page}'.format(url=url, page=page)
print(url)
header = {'User-Agent':'<복사한 user-agent 값 대체>'}
res = requests.get(url,headers=header)
df = pd.read_html(res.text, header=0)[0]
df.head()

