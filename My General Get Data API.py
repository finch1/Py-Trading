from typing import List
import requests
import pandas as pd
import datetime
import sqlalchemy
from sqlalchemy import delete

# DB Connection
engine = sqlalchemy.create_engine('sqlite:///OurDataBase.db/')


def RequestData(api, url, querystring):
    headers = {
        'x-rapidapi-host': "yh-finance.p.rapidapi.com",
        'x-rapidapi-key': "c6cd8b9f2emshfb2615731363f42p15d34cjsn7042a149083c"
        }
    
    ## Do not delete. to quickly get informatio on API
    # response = requests.request("GET", url, headers=headers, params=querystring)
    # data = response.json()
    # for key in data:
    #     print(f"API: {api} \t Keys: {key}")    
    # return 0
    return requests.request("GET", url, headers=headers, params=querystring)

def TransformToTable(table, symbol, data_dict):
    columns = ['key', 'value']
    # convert to data frame
    data_items = data_dict.items()
    data_list = list(data_items)
    df = pd.DataFrame(data_list)

    # name the columns
    df.columns=columns

    # ad symbol as index
    df['symbol'] = symbol
    #print(df.head(5))

    # transpose
    df = df.pivot(index = 'symbol', columns = 'key', values = 'value').reset_index()

    # store in DB
    print(df.head(5))
    try:
        df.to_sql(table, engine, if_exists='append', index=False)
    except Exception as e:    
        print("ERROR WITH INSERT TO DB!!!")
        print(e)

def ClearTable(table):
    try:
        delete(table)
    except Exception as e:    
        print("ERROR WITH DB!!!")
        print(e)

def DirectDictionary(symbol, data, table):
    data_dict = {}
    for key in data:
        if isinstance(data[key], str):
            data_dict[key] = data[key] #print(f"Symbol:{Symbol}\tCall: Holders\tTable: data\tKey: {key}\tValue: {data[key]}")
        
        elif isinstance(data[key], int):
            data_dict[key] = data[key] #print(f"Symbol:{Symbol}\tCall: Holders\tTable: data\tKey: {key}\tValue: {data[key]}")
        
        elif bool(data[key]): # if dictionary is not empty
            if 'longFmt' in data[key]:
                value = data[key]['longFmt']
                data_dict[key] = value #print(f"Symbol:{Symbol}\tCall: Holdings\tTable: data\tKey: {key}\tValue: {value}")
            elif 'fmt' in data[key]:
                value = data[key]['fmt']
                data_dict[key] = value #print(f"Symbol:{Symbol}\tCall: Holdings\tTable: data\tKey: {key}\tValue: {value}")

    TransformToTable(table, symbol, data_dict)

def ListOfDictionaries(symbol, data, table):
    data_dict = {}

    for dic in data:
        if "maxAge" in dic:
            del dic['maxAge']

        for key in dic:
            if isinstance(dic[key], str):
                data_dict[key] = dic[key]

            elif isinstance(dic[key], int):
                data_dict[key] = dic[key] 
                       
            elif bool(dic[key]): # if dictionary is not empty
                if 'longFmt' in dic[key]:
                    value = dic[key]['longFmt']
                    data_dict[key] = value
                elif 'fmt' in dic[key]:
                    value = dic[key]['fmt']
                    data_dict[key] = value
    
        TransformToTable(table, symbol, data_dict)


### CASHFLOW
def GetCashflow(symbol, dataDict):
    Get_CashflowStatementHistory(symbol, dataDict['cashflowStatementHistory'])    
    Get_BalanceSheetHistoryQuarterly(symbol, dataDict['balanceSheetHistoryQuarterly'])
    Get_Earnings(symbol, dataDict['earnings'])
    Get_price(symbol, dataDict['price'])
    Get_IncomeStatementHistoryQuarterly(symbol, dataDict['incomeStatementHistoryQuarterly'])
    Get_IncomeStatementHistory(symbol, dataDict['incomeStatementHistory'])
    Get_BalanceSheetHistory(symbol, dataDict['balanceSheetHistory'])
    Get_CashflowStatementHistoryQuarterly(symbol, dataDict['cashflowStatementHistoryQuarterly'])
    # Get_QuoteType(dataDict['quoteType'])
    # Get_SummaryDetail(dataDict['summaryDetail']) # Not sure if this is needed 
    # Get_PageViews(symbol, dataDict['pageViews'])
    Get_TimeSeries(symbol, dataDict['timeSeries'])
    # Get_Meta(dataDict['meta'])
    return 0

def Get_CashflowStatementHistory(symbol, cashflowStatementHistory):
    table = "CashFlow_CashflowStatementHistory"   
    
    ListOfDictionaries(symbol, cashflowStatementHistory['cashflowStatements'], table)

    return 0

def Get_BalanceSheetHistoryQuarterly(symbol, balanceSheetHistoryQuarterly):
    table = "CashFlow_BalanceSheetHistoryQuarterly"
   
    ListOfDictionaries(symbol, balanceSheetHistoryQuarterly['balanceSheetStatements'], table)

    return 0


def Get_Earnings(symbol, earnings):
    for dicKey in earnings: # loop keys of dict
        if dicKey == 'earningsChart':        
            #for innerDict in earnings[dicKey]: # loop list of dicts. returns array content(elements)
                Store_EarningsChart(symbol, earnings[dicKey])

        elif dicKey == 'financialsChart':       
            #for innerDict in earnings[dicKey]: # loop list of dicts. returns array content(elements)
                Store_FinancialChart(symbol, earnings[dicKey])

        elif dicKey == 'financialCurrency':
            print(earnings[dicKey])

def Store_EarningsChart(symbol, earnings_dic):
    table = "CashFlow_EarningsChart"
    ListOfDictionaries(symbol, earnings_dic['quarterly'], table)

    currQuatEst = earnings_dic['currentQuarterEstimate']['raw']
    currQuatEstDate = earnings_dic['currentQuarterEstimateDate']
    currQuatEstYear = earnings_dic['currentQuarterEstimateYear']
    print(f"Call: Cashflow\tTable: EarningsChart\tCurrent Quarter Estimate Date: {currQuatEstDate}\tCurrent Quarter Estimate Year: {currQuatEstYear}\tCurrent Quarter Estimate: {currQuatEst}")

# def Store_EarningsQuarterly(symbol, quarterlyList):
#     for dic in quarterlyList: # loop yearly list of dict. retrieves one key value pair and 2 dictionaries
#         date = dic['date']
#         actual = dic['actual']['fmt']
#         estimate = dic['estimate']['fmt']
#         print(f"Call: Cashflow\tTable: EarningsQuarterly\tDate: {date}\tActual: {actual}\tEstimate: {estimate}")

def Store_FinancialChart(symbol, balsheethist_dic):
    table = "CashFlow_YearlyFinancials"
    ListOfDictionaries(symbol, balsheethist_dic['yearly'], table)
    table = "CashFlow_QuarterlyFinancials"
    ListOfDictionaries(symbol, balsheethist_dic['quarterly'], table)

# def Store_YearlyFinancials(symbol, yearlyList):
#     for dic in yearlyList: # loop yearly list of dict. retrieves one key value pair and 2 dictionaries
#         date = dic['date']
#         revenue = dic['revenue']['longFmt']
#         earnings = dic['earnings']['longFmt']
#         print(f"Call: Cashflow\tTable: YearlyFinancials\tDate: {date}\tRevenue: {revenue}\tEarnings: {earnings}")

# def Store_QuarterlyFinancials(symbol, quarterlyList):
#     for dic in quarterlyList: # loop yearly list of dict. retrieves one key value pair and 2 dictionaries
#         date = dic['date']
#         revenue = dic['revenue']['longFmt']
#         earnings = dic['earnings']['longFmt']
#         print(f"Call: Cashflow\tTable: QuarterlyFinancials\tDate: {date}\tRevenue: {revenue}\tEarnings: {earnings}")


def Get_price(symbol, price):
    table = "Cashflow_Price"

    del price['maxAge'] # unwanted pairs
    del price['symbol']

    DirectDictionary(symbol, price, table)

    return 0

def Get_IncomeStatementHistoryQuarterly(symbol, incomeStatementHistoryQuarterly):
    table = "CashFlow_IncomeStatementHistoryQuarterly"
    
    ListOfDictionaries(symbol, incomeStatementHistoryQuarterly['incomeStatementHistory'], table)

    return 0

def Get_IncomeStatementHistory(symbol, incomeStatementHistory):
    table = "CashFlow_IncomeStatementHistory"
    
    ListOfDictionaries(symbol, incomeStatementHistory['incomeStatementHistory'], table)

    return 0

def Get_BalanceSheetHistory(symbol, balanceSheetHistory):
    table = "CashFlow_BalanceSheetHistory"
    
    ListOfDictionaries(symbol, balanceSheetHistory['balanceSheetStatements'], table)

    return 0

def Get_CashflowStatementHistoryQuarterly(symbol, cashflowStatementHistoryQuarterly):
    table = "CashFlow_CashflowStatementHistoryQuarterly"
    
    ListOfDictionaries(symbol, cashflowStatementHistoryQuarterly['cashflowStatements'], table)

    return 0

def Get_TimeSeries(symbol, timeSeries):
    table = "CashFlow_TimeSeries"
    del timeSeries['timestamp']

    for key in timeSeries:
        
            for dic in timeSeries[key]: # looping list of dicts
                if bool(dic):
                    try:
                        data = {'Symbol': symbol,
                                'Section': [key],
                                'As of Date': dic['asOfDate'],
                                'Period Type': [dic['periodType']],
                                'Currency': [dic['currencyCode']],
                                'Reported Value': [dic['reportedValue']['fmt']]
                                }
                        # create dateframe
                        df = pd.DataFrame(data)
                        df.to_sql(table, engine, if_exists='append', index=False)
                    except Exception as e:    
                        print("ERROR WITH DB!!!")
                        print(e)

    #print(f"Call: Cashflow\tTable: TimeSeries\tSection: {key}\t As of Date: {dic['asOfDate']}\t Period Type: {dic['periodType']}\t Currency: {dic['currencyCode']}\t Reported Value: {dic['reportedValue']['fmt']}")
'''
    # def Get_CashflowStatementHistory(symbol, cashflowStatement):
    #     for dicKey in cashflowStatement: # loop keys of dict
    #         if isinstance(cashflowStatement[dicKey], list):
                
    #             for innerDict in cashflowStatement[dicKey]: # loop list of dicts
    #                 Store_CashflowStatement(innerDict)

    # def Store_CashflowStatement(symbol, cashflow_dic):
    #     periodDate = cashflow_dic['endDate']['fmt']
    #     for innerDicKey in cashflow_dic: # FOR key IN dictionary
    #         if isinstance(cashflow_dic[innerDicKey], dict):
            
    #             for subDicKey in cashflow_dic[innerDicKey]: # FOR keys of returned dictionary IN get the first dictionary
    #                 if subDicKey == 'longFmt':
    #                     print(f"Call: Cashflow\tTable: CashflowStatementHistory\tPeriod: {periodDate}\tSection: {innerDicKey}\tValue: {cashflow_dic[innerDicKey][subDicKey]}")


    # def Get_BalanceSheetHistoryQuarterly(symbol, balanceSheetHistoryQuarterly):
    #     for dicKey in balanceSheetHistoryQuarterly: # loop keys of dict
    #         if isinstance(balanceSheetHistoryQuarterly[dicKey], list):
                
    #             for innerDict in balanceSheetHistoryQuarterly[dicKey]: # loop list of dicts. returns array content(elements)
    #                 Store_BalanceSheetStatements(innerDict)

    # def Store_BalanceSheetStatements(symbol, balsheethist_dic):
    #     periodDate = balsheethist_dic['endDate']['fmt']
    #     for innerDicKey in balsheethist_dic: # loop dictionary key value pairs. FOR key IN dictionary
    #         if isinstance(balsheethist_dic[innerDicKey], dict):
    #             for subDicKey in balsheethist_dic[innerDicKey]: # FOR keys of returned dictionary IN get the first dictionary
    #                 if subDicKey == 'longFmt':
    #                     print(f"Call: Cashflow\tTable: BalanceSheetHistoryQuarterly\tPeriod: {periodDate}\tSection: {innerDicKey}\tValue: {balsheethist_dic[innerDicKey][subDicKey]}")




    # def Get_Price(symbol, price_dic):
    #     data = []
    #     for key in price_dic:
    #         if isinstance(price_dic[key], str):
    #             data.append({key:price_dic[key]})
                    
    #         elif isinstance(price_dic[key], int):
    #             data.append({key:price_dic[key]})

    #         elif isinstance(price_dic[key], dict):
    #             if bool(price_dic[key]):# check for empty dictionary
                    
    #                 if 'longFmt' in price_dic[key]:
    #                     data.append({key:price_dic[key]['longFmt']})

    #                 elif 'fmt' in price_dic[key]: # check if dict contains this key
    #                     data.append({key:price_dic[key]['fmt']})

    #     data = [i for i in data if not (i == 'maxAge')]

    #     for dic in data:
    #         for key, value in dic.items():
    #             print(f"Call: Cashflow\tTable: Price\tData: {key}\tValue: {value}")


    # def Get_IncomeStatementHistoryQuarterly(symbol, incomeStatementHQ):
    #     for dicKey in incomeStatementHQ: # loop list of dict
    #         if isinstance(incomeStatementHQ[dicKey], list):
    #             Store_IncomeStatementHistoryQuarterly(incomeStatementHQ[dicKey])

    # def Store_IncomeStatementHistoryQuarterly(symbol, incStHQ_dic):
    #     for dic in incStHQ_dic:
    #         periodDate = dic['endDate']['fmt']
    #         for key in dic:
    #             if isinstance(dic[key], dict):# check for empty dictionary
    #                 if 'longFmt' in dic[key]: # do not include date again
    #                     print(f"Call: Cashflow\tTable: IncomeStatementHistoryQuarterly\tPeriod: {periodDate}\tKey: {key}\tValue: {dic[key]['longFmt']}")


    # def Get_IncomeStatementHistory(symbol, incomeStatementH):
    #     for dicKey in incomeStatementH: # loop list of dict
    #         if isinstance(incomeStatementH[dicKey], list):
    #             Store_IncomeStatementHistory(incomeStatementH[dicKey])

    # def Store_IncomeStatementHistory(symbol, incStH_dic):
    #     for dic in incStH_dic:
    #         periodDate = dic['endDate']['fmt']
    #         for key in dic:
    #             if isinstance(dic[key], dict):# check for empty dictionary
    #                 if 'longFmt' in dic[key]: # do not include date again
    #                     print(f"Call: Cashflow\tTable: IncomeStatementHistory\tPeriod: {periodDate}\tKey: {key}\tValue: {dic[key]['longFmt']}")


    # def Get_BalanceSheetHistory(symbol, balanceSheetH):
    #     for dicKey in balanceSheetH: # loop list of dict
    #         if isinstance(balanceSheetH[dicKey], list):
    #             Store_IncomeStatementHistory(balanceSheetH[dicKey])

    # def Store_BalanceSheetHistory(symbol, balShtH_dic):
    #     for dic in balShtH_dic:
    #         periodDate = dic['endDate']['fmt']
    #         for key in dic:
    #             if isinstance(dic[key], dict):# check for empty dictionary
    #                 if 'longFmt' in dic[key]: # do not include date again
    #                     print(f"Call: Cashflow\tTable: BalanceSheetHistory\tPeriod: {periodDate}\tKey: {key}\tValue: {dic[key]['longFmt']}")


    # def Get_CashflowStatementHistoryQuarterly(symbol, casflowStmtHQ):
    #     for dicKey in casflowStmtHQ: # loop list of dict
    #         if isinstance(casflowStmtHQ[dicKey], list):
    #             Store_CashflowStatementHistoryQuarterly(casflowStmtHQ[dicKey])

    # def Store_CashflowStatementHistoryQuarterly(symbol, casflowStmtHQ_dic):
    #     for dic in casflowStmtHQ_dic:
    #         periodDate = dic['endDate']['fmt']
    #         for key in dic:
    #             if isinstance(dic[key], dict):# check for empty dictionary
    #                 if 'longFmt' in dic[key]: # do not include date again
    #                     print(f"Call: Cashflow\tTable: CashflowStatementHistoryQuarterly\tPeriod: {periodDate}\tKey: {key}\tValue: {dic[key]['longFmt']}")

    # def Get_PageViews(symbol, pageView):
    #     for key in pageView:
    #         print(f"Call: Cashflow\tTable: PageViews\tKey: {key}\tValue: {pageView[key]}")
'''
### CASHFLOW

### HOLDINGS
def GetHolders(symbol, dataDict):
    Get_Hprice(symbol, dataDict['price'])
    Get_fundOwnership(symbol, dataDict['fundOwnership'])
    Get_insiderTransactions(symbol, dataDict['insiderTransactions'])
    Get_insiderHolders(symbol, dataDict['insiderHolders'])
    Get_netSharePurchaseActivity(symbol, dataDict['netSharePurchaseActivity'])
    Get_majorHoldersBreakdown(symbol, dataDict['majorHoldersBreakdown'])
    Get_institutionOwnership(symbol, dataDict['institutionOwnership'])
    Get_HsummaryDetail(symbol, dataDict['summaryDetail'])

    # Get_quoteType(symbol, dataDict['quoteType'])
    # Get_assetProfile(symbol, dataDict['assetProfile'])
    return 0

def Get_Hprice(symbol, price):
    table = "Holders_Price"

    del price['maxAge'] # unwanted pairs
    del price['symbol']

    ClearTable(table)
    DirectDictionary(symbol, price, table)

    return 0

def Get_fundOwnership(symbol, fundOwnership):
    table = "Holders_FundOwnership"
    
    ListOfDictionaries(symbol, fundOwnership['ownershipList'], table)

    return 0

def Get_insiderTransactions(symbol, insiderTransactions):
    table = "Holders_InsiderTransactions"

    # check if dict is empty
    if not bool(insiderTransactions):
        return

    ListOfDictionaries(symbol, insiderTransactions['transactions'], table)

    return 0

def Get_insiderHolders(symbol, insiderHolders):
    table = "Holders_InsiderHolders"
    
    ListOfDictionaries(symbol, insiderHolders['holders'], table)
    return 0

def Get_netSharePurchaseActivity(symbol, netSharePurchaseActivity):
    table = "Holders_NetSharePurchaseActivity"

    del netSharePurchaseActivity['maxAge'] # unwanted pairs

    ClearTable(table)
    DirectDictionary(symbol, netSharePurchaseActivity, table)
    return 0

def Get_majorHoldersBreakdown(symbol, majorHoldersBreakdown):
    table = "Holders_MajorHoldersBreakdown"

    del majorHoldersBreakdown['maxAge'] # unwanted pairs

    DirectDictionary(symbol, majorHoldersBreakdown, table)
    return 0

def Get_institutionOwnership(symbol, institutionOwnership):
    table = "Holders_InstitutionOwnership"
    
    ListOfDictionaries(symbol, institutionOwnership['ownershipList'], table)
    return 0

def Get_HsummaryDetail(symbol, summaryDetail):
    table = "Holders_Price"
    del summaryDetail['maxAge'] # unwanted pairs

    DirectDictionary(symbol, summaryDetail, table)

    return 0

# quoteData has shares outstanding. in case we cannot find them any where else  
### HOLDINGS

### HISTORICAL
def GetHistoricalData(symbol, data):
    # check if list is empty
    if not data['prices']:
        return

    data_dict = {}
    table = 'HistoricalData_Prices'
    df = pd.DataFrame()

    for dic in data['prices']:
        data_dict['symbol'] = symbol
        for key in dic:
            if key == 'date':
                data_dict[key] = datetime.datetime.fromtimestamp(dic[key]).strftime(format = '%Y/%m/%d')
            else:
                data_dict[key] = dic[key]
        df = df.append(data_dict, True)

    # store in DB
    df = df[['symbol','date','open','high','low','close','volume','adjclose']]
    print(df.head(5))


    try:
        # Get last input date so we eleminate dublicates from df before inserting
        myQuery = f"SELECT IFNULL(MAX(date),'1990-01-01') AS lastDate FROM {table} WHERE symbol = '{symbol}'"

        lastDate = pd.read_sql_query(myQuery, engine)

        df[(df['date'] > lastDate['lastDate'][0])].to_sql(table, engine, if_exists='append', index=False)


    except:
        print("ERROR WITH DB!!!")

    return 0
### HISTORICAL

### SUMMARY
def GetSummary(symbol, data):
    Get_summaryProfile(symbol, data['summaryProfile'])
    Get_recommendationTrend(symbol, data['recommendationTrend'])
    Get_financialData(symbol, data['financialData'])
    ##Get_calendarEvents(symbol, data['calendarEvents'])
    ##Get_summaryDetail(symbol, data['summaryDetail']) # Not Sure if this is needed. 
    # esgScore lists controversial facts
    return 0

def Get_summaryProfile(symbol, summaryProfile):
    table = "Summary_SummaryProfile"
    try:
        data = {'Symbol': symbol,
                'sector': [summaryProfile['sector']],
                'fullTimeEmployees': [summaryProfile['fullTimeEmployees']],
                'longBusinessSummary': [summaryProfile['longBusinessSummary']],
                'country': [summaryProfile['country']],
                'industry': [summaryProfile['industry']],
                'website': [summaryProfile['website']]
        }
        # create dateframe
        df = pd.DataFrame(data)
        df.to_sql(table, engine, if_exists='append', index=False)
    except Exception as e:    
        print("ERROR WITH DB!!!")
        print(e)

    return 0

def Get_recommendationTrend(symbol, recommendationTrend):
    table = "Summary_recommendationTrend"

    ClearTable(table)
    ListOfDictionaries(symbol, recommendationTrend['trend'], table)
    return 0

def Get_financialData(symbol, financialData):
    table = "Summary_financialData"
    del financialData['maxAge']

    ClearTable(table)
    DirectDictionary(symbol, financialData, table)

    return 0

def Get_SummaryDetail(symbol, summaryDetail):
    table = "Summary_summaryDetail"
    del summaryDetail['maxAge']

    DirectDictionary(symbol, summaryDetail, table)

    return 0
### SUMMARY



Symbols = [ 'UPS', 'MU', 'IUGNF',	'GCPEF',	'ZOM',	'NIO',	'MRMD',	'AAH',	'CANF',	'AYTU',	'TWLO', 'SEAC',	'SOLO',	'XERS',	'TAN',	'DOYU',	'XXII',	'BNGO',	'BDSI',	'WLMIF',	'KNDI',	'SB',	'NNDM',	'LI',	
            'MVIS',	'WKHS',	'OCGN',	'FCEL',	'CRON',	'CAN',	'RBBN',	'NOK',	'SOPA',	'SOL',	'ARVL',	'FUV',	'OTLY',	'APPS',	'ARKO',	'GOGL',	'VWDRY',	'MOMO',	'NVX',	'POAHY',	'SPCE',	'ACRS',	'BLDP',	'ASAI',	'ICL',	
            'LILA',	'IRWD',	'CARA',	'SCPL',	'968',	'WHGLY',	'TPIC',	'API',	'DVAX',	'HOLI',	'TAK',	'VTRS',	'PLTR',	'MNDT',	'STNE',	'UTZ',	'BE',	'AMKBY',	'WOOF',	'COLL',	'DDD',	'AR',	'FANUY',	'SPWR',	'QURE',	
            'NLSN',	'RIOT',	'MTLS',	'QS',	'AES',	'BLNK',	'PLUG',	'SG',	'SSYS',	'GT',	'F',	'NLOK',	'T',	'XM',	'RMBS',	'CSIQ',	'LBTYA',	'MRVI',	'VCYT',	'LAC',	'ACI',	'RUN',	'BAESY',	'AVID',	'OGN',	'AGIO',	
            'BGS',	'TTM',	'RDWR',	'CSX',	'SUM',	'AQUA',	'RPRX',	'DAL',	'NRG',	'LYFT',	'FE',	'LCID',	'DQ',	'SAGE',	'GBX',	'FIZZ',	'UNFI',	'UAL',	'KR',	'CELH',	'XPEV',	'INMD',	'COST',	'8466',	'CAH',	'VZ',	'EVBG',
            'INTC',	'NTDOY',	'DRE',	'PDD',	'AVAV',	'GM',	'SWTX',	'ZIM',	'BMY',	'ATVI',	'DAR',	'CF',	'BYND',	'IRBT',	'CRSP',	'IHG',	'AFRM',	'CGNX',	'BRKR',	'ADM',	'GILD',	'NTR',	'BCS',	'DAC',	'DAI',	'RBLX',
            'RIVN',	'MRK',	'ACP',	'FSLR',	'COP',	'SAIC',	'NVS',	'H',	'RTX',	'ESTC',	'BG',	'NET',	'CMA',	'LYB',	'PM',	'EOG',	'RJF',	'TMUS',	'UPST',	'RHI',	'CINF',	'AMD',	'PAYX',	'CHKP',	'ABT',	'EA',
            'BABA',	'SQ',	'IBM',	'ABBV',	'AXON',	'DDOG',	'CW',	'AME',	'ENPH',	'CYBR',	'HLT',	'NKE',	'DIS',	'HEI',	'APTV',	'PLD',	'HPGLY',	'AMBA',	'MMC',	'CDNS',	'MAR',	'ETSY',	'ABNB',	'OMCL',	'ROKU',
            'W',	'AAPL',	'SE',	'CRWD',	'PYPL',	'VOW3',	'ROBO',	'HII',	'XLNX',	'TM',	'TRN',	'UNP',	'SEDG',	'ZS',	'SYK',	'NVDA',	'CACI',	'NSC',	'KSU',	'ISRG',	'FTNT',	'FB',	'MA',	'LMT',	'GS',
            'NOC',	'FAN',	'ASML',	'PRSM',	'PRU',	'ABB',	'PFIZER',	'NOKIA',	'NU',	'VS',	'NOVA', 'BAC', 'AMC', 'TDOC', 'SM', 'TWLO', 'ZM', 'GME', 'CRM', 'WDAY', 'CHPT', 'EVGO', 'DOCU', 'LMND', 'DASH', 'FSLY', 
            'FVRR', 'FTCI', 'TLRY', 'UNP', 'CSX', 'NSC', ] 

# # start
for symbol in Symbols:
    data = RequestData(api="get-historical-data",   url = "https://yh-finance.p.rapidapi.com/stock/v3/get-historical-data", querystring = {"symbol":symbol,"region":"US"})
    if data.status_code == 200:
        GetHistoricalData(symbol, data.json())

    data = RequestData(api="get-holders",           url = "https://yh-finance.p.rapidapi.com/stock/v2/get-holders",         querystring = {"symbol":symbol,"region":"US"})
    if data.status_code == 200:
        GetHolders(symbol, data.json())

    data = RequestData(api="get-cash-flow",         url = "https://yh-finance.p.rapidapi.com/stock/v2/get-cash-flow",       querystring = {"symbol":symbol,"region":"US"})
    if data.status_code == 200:
        GetCashflow(symbol, data.json())

    data = RequestData(api="get-summary",           url = "https://yh-finance.p.rapidapi.com/stock/v2/get-summary",         querystring = {"symbol":symbol,"region":"US"})
    if data.status_code == 200:
            GetSummary(symbol, data.json())





'''
RequestData(api="get-recommendations", url = "https://yh-finance.p.rapidapi.com/stock/v2/get-recommendations", querystring = {"symbol":"INTC"})
RequestData(api="get-upgrades-downgrades", url = "https://yh-finance.p.rapidapi.com/stock/v2/get-upgrades-downgrades", querystring = {"symbol":"INTC","region":"US"})
RequestData(api="get-chart", url = "https://yh-finance.p.rapidapi.com/stock/v3/get-chart", querystring = {"interval":"1mo","symbol":"AMRN","range":"5y","region":"US","includePrePost":"falseGetData()","useYfid":"true","includeAdjustedClose":"true","events":"capitalGain,div,split"})
RequestData(api="get-statistics", url = "https://yh-finance.p.rapidapi.com/stock/v3/get-statistics", querystring = {"symbol":"JD"})
RequestData(api="get-profile", url = "https://yh-finance.p.rapidapi.com/stock/v2/get-profile", querystring = {"symbol":"AMRN","region":"US"})
RequestData(api="get-financials", url = "https://yh-finance.p.rapidapi.com/stock/v2/get-financials", querystring = {"symbol":"AMRN","region":"US"})
RequestData(api="get-balance-sheet", url = "https://yh-finance.p.rapidapi.com/stock/v2/get-balance-sheet", querystring = {"symbol":"AMRN","region":"US"})
RequestData(api="get-analysis", url = "https://yh-finance.p.rapidapi.com/stock/v2/get-analysis", querystring = {"symbol":"AMRN","region":"US"})
RequestData(api="get-options", url = "https://yh-finance.p.rapidapi.com/stock/v2/get-options", querystring = {"symbol":"AMRN","date":"1562284800","region":"US"})
data = RequestData(api="get-holdings",          url = "https://yh-finance.p.rapidapi.com/stock/v2/get-holdings",        querystring = {"symbol":"AMD"})
data = RequestData(api="get-timeseries",        url = "https://yh-finance.p.rapidapi.com/stock/v2/get-timeseries",      querystring = {"symbol":"AMD","period1":"493578000","period2":"1625011200","region":"US"})
GetTimeseries(Symbol, data.json())

data = RequestData(api="get-movers", url = "https://yh-finance.p.rapidapi.com/market/v2/get-movers", querystring = {"region":"US","lang":"en-US","count":"6","start":"0"}).json()
data = RequestData(api="get-trending-tickers", url = "https://yh-finance.p.rapidapi.com/market/get-trending-tickers", querystring = {"region":"US"}).json()
data = RequestData(api="get-popular-watchlists", url = "https://yh-finance.p.rapidapi.com/market/get-popular-watchlists", querystring={}).json()
data = RequestData(api="get-watchlist-performance", url = "https://yh-finance.p.rapidapi.com/market/get-watchlist-performance", querystring = {"userId":"X3NJ2A7VDSABUI4URBWME2PZNM","pfId":"the_berkshire_hathaway_portfolio","symbols":"^GSPC","region":"US"}).json()
data = RequestData(api="get-watchlist-detail", url = "https://yh-finance.p.rapidapi.com/market/get-watchlist-detail", querystring = {"userId":"X3NJ2A7VDSABUI4URBWME2PZNM","pfId":"the_berkshire_hathaway_portfolio"}).json()

data = RequestData(api="get-recommendations", url = "https://yh-finance.p.rapidapi.com/stock/v2/get-recommendations", querystring = {"symbol":"INTC"}).json()
data = RequestData(api="get-insider-transactions", url = "https://yh-finance.p.rapidapi.com/stock/v2/get-insider-transactions", querystring = {"symbol":"AMRN","region":"US"}).json()
data = RequestData(api="get-insider-roster", url = "https://yh-finance.p.rapidapi.com/stock/v2/get-insider-roster", querystring = {"symbol":"AMRN","region":"US"}).json()


RequestData(api="get-insights", url = "https://yh-finance.p.rapidapi.com/stock/v2/get-insights", querystring = {"symbol":"AAPL"})





RequestData(api="get-quotes", url = "https://yh-finance.p.rapidapi.com/market/v2/get-quotes", querystring = {"region":"US","symbols":"AMD,IBM,AAPL"})
RequestData(api="get-summary", url = "https://yh-finance.p.rapidapi.com/market/v2/get-summary", querystring = {"region":"US"})
RequestData(api="get-spark", url = "https://yh-finance.p.rapidapi.com/market/get-spark", querystring = {"symbols":"AMZN,AAPL,WDC,REYN,AZN,YM=F","interval":"1m","range":"1d"})
RequestData(api="get-earnings", url = "https://yh-finance.p.rapidapi.com/market/get-earnings", querystring = {"region":"US","startDate":"1585155600000","endDate":"1589475600000","size":"10"})
RequestData(api="get-charts", url = "https://yh-finance.p.rapidapi.com/market/get-charts", querystring = {"symbol":"HYDR.ME","interval":"5m","range":"1d","region":"US","comparisons":"^GDAXI,^FCHI"})

'''







print()