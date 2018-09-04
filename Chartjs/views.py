from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response


User = get_user_model()



from Companies.models import Profile, News


class HomeView(View):
    def get(self, request, *args, **kwargs):


        def search():
            if 'params' in request.GET:
                x = request.GET['params']
            else:
                x = 'Form is empty'
            
            return x


        params = search()
        params = params.split('_')
        co_id = params[0] #profile id number
        global sheet_type
        sheet_type = params[1] #sheet type
        print(sheet_type)
    

        profile = Profile.objects.get(id = co_id) #reuturns NVDA : Technology
        global ticker
        ticker = str(profile).split(':')[0]
        ticker = "".join(ticker.split())




        #MORNINGSTAR_PATH = '/home/msands/Dropbox/ProgrammingFiles/Present/Share/Input/MorningstarFinancials/'
        YAHOO_HISTORIC_PATH = '/home/msands/Dropbox/ProgrammingFiles/Present/Share/Input/YahooHistorical/'
        YEAR = 2017
        OUTPUT_PATH = '/home/msands/Dropbox/ProgrammingFiles/Present/Share/Output/'
        STATIC_TECH_PATH = '/home/msands/Dropbox/ProgrammingFiles/Present/Linux/DjangoDirectory/Midas101/Technicals/static/'


        global yahoo_historic_path
        yahoo_historic_path = YAHOO_HISTORIC_PATH + ticker + '1Y.csv'


        global market_path
        market_path = YAHOO_HISTORIC_PATH + '^GSPC.csv'

        cols = ['date', 'open', 'high', 'low', 'close', 'adjClose', 'volume']

        global yahoo_historic_df
        yahoo_historic_df = pd.read_csv(yahoo_historic_path, names=cols, skiprows=range(0, 1))


        if sheet_type == "BollingerBands" or sheet_type == 'MACD':
            return render(request, 'multiline_charts.html', {"customers": 10})

        else:
            return render(request, 'charts.html', {"customers": 10})



def get_data(request, *args, **kwargs):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data) # http response


import sys
sys.path.insert(0, '/home/msands/Dropbox/ProgrammingFiles/Present/Linux/DjangoDirectory/Midas102/PyFiMethods/')

# import Beta as beta
import BollingerBands as bb
import RSI as rsi
import MACD as macd
import pandas as pd



class ChartData(APIView):

    authentication_classes = []
    permission_classes = []


    def get(self, request, format=None):
        selected_items = ''
        selected_items2 = ''
        selected_items3 = ''

        default_items  = yahoo_historic_df['close'].values
        label_items = yahoo_historic_df['date'].values

        #Check which sheet type is chosen from Buttons and call appropriate PyFi Method
        # if sheet_type == 'Beta':
        #     rollingbeta = beta.init_beta(ticker, yahoo_historic_path, market_path, 'x')
        #     selected_items = rollingbeta['beta']


        if sheet_type == 'BollingerBands':
            bolband = bb.init_bb(yahoo_historic_path)
            selected_items = bolband['upper']
            selected_items2 = bolband['middle']
            selected_items3 = bolband['lower']

        if sheet_type == 'RSI':
            relativestrength = rsi.init_rsi(yahoo_historic_path)
            selected_items = relativestrength

        if sheet_type == 'MACD':
            mac = macd.run_macd(yahoo_historic_path)
            selected_items = mac['signal']
            selected_items2 = mac['macd']

            default_items = ''





        #This info is what is passed into the charts html to be rendered
        data = {
                "labels": label_items,
                "default": default_items,
                "selected": selected_items,
                "selected2": selected_items2,
                "selected3": selected_items3
        }


        return Response(data)

