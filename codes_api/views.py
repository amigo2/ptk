
import json
import requests
from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from django.http import Http404
from rest_framework.response import Response

import pandas as pd


from .utils import calculate_distance
from .utils import to_xml
from .utils import load_file_to_pandas


'''
The apps grabs data from 2 sources, 
1st is http://api.postcodes.io/outcodes/M11, from here it returns
the admind wards 'admin_ward': ['Ancoats & Beswick', 'Droylsden East', 'Clayton & Openshaw'],
2nd Taking those borrows we grab the data from the csv file we can claculate for example the average price and others
same as reflected in the airbnb page

The app needs to return 2 end points, with following XML structure
1.
GET/api/outcode/{outcode} M11
<outcode
listing-count="{{ number of listings within outcode }}"
average-daily-rate="{{ average daily rate of all listings within outcode }}"
>{{ outcode }}</outcode>

If no data is available, return an empty 404 response.

2.
GET /api/nexus/{outcode}

Returns a list of neighbouring postcode districts (outcodes) for the given nexus outcode.
NB you should include the nexus outcode within the list.
Use the following data structure:
<outcodes
nexus="{{ nexus outcode }}"
listing-count="{{ sum of listings }}"
average-daily-rate="{{ average daily rate across all listings }}">
<!-- repeat for each neighbouring outcode -->
<outcode
listing-count="{{ number of listings within outcode }}"
average-daily-rate="{{ average daily rate of all listings within outcode }}"
distance=”{{ distance from nexus }}”
>{{ outcode }}</outcode>
</outcodes>
If no data is available, return an empty 404 response.

'''



class OutcodesView(APIView):
    """
    Retrieve,
    """

    def get(self, request, post_code):
        
        try:

            df = load_file_to_pandas('listings.csv')                

            url = 'http://api.postcodes.io/outcodes/'+ post_code
            r = requests.get(url)


            postcodes = r.json()

            ward = postcodes['result']['admin_ward']


            count_list = []
            location_list = []
            price_list = []



            for w in ward:
                location = df.loc[df['neighbourhood']== w]
                result_df = location[['neighbourhood','price']]
                avr_price = location['price'].mean()
                index = location.index
                number_of_rows = len(index)

                
                count_list.append(number_of_rows)
                price_list.append(avr_price)
                location_list.append(w)

        
            data =  { 'listing-count': count_list, 'average-daily-rate': price_list , 'location': location_list }


            
            outcode_df = pd.DataFrame(data, columns = ['listing-count','average-daily-rate','location'])


            result = to_xml(outcode_df)

            return Response(result)
            

        except:
            res = {"code": 404, "message": "Data not Found!"}
            return Response(data=json.dumps(res), status=status.HTTP_404_NOT_FOUND)



class NexusView(APIView):

    #permission_classes = [ReadOnly]

    def get(self, request, post_code):

        try:

            # function to load csv file
            df = load_file_to_pandas('listings.csv')

            
            url = 'http://api.postcodes.io/outcodes/' + post_code + '/nearest'
            r = requests.get(url)
            postcodes = r.json()

            result = postcodes['result']

            locations = []
            longitude = []
            latitude = []


            new_result = []
            #print(result['northings'])


            for k in result:
                del k['northings']
                del k['eastings']
                del k['admin_district']
                del k['parish']
                del k['country']
                del k['admin_county']
                new_result.append(k)


            

            for ward in new_result:       
                locations.append(ward['admin_ward'])
                longitude.append(ward['longitude'])
                latitude.append(ward['latitude'])


            new_df = pd.DataFrame.from_dict(new_result)


            count_list = []
            location_list = []
            price_list = []
            distance = []


            for l in locations:
                for n in l:
                    location = df.loc[df['neighbourhood']== n]
                    result_df = location[['neighbourhood','price']]
                    avr_price = location['price'].mean()
                    index = location.index
                    number_of_rows = len(index)

                    count_list.append(number_of_rows)
                    price_list.append(avr_price)
                    location_list.append(n)


            long_list = [float(i) for i in longitude]
            lat_list = [float(i) for i in latitude]

            n = len(long_list)

            for i in range(0,n):
                r = calculate_distance(long_list[0],lat_list[0],long_list[i],lat_list[i])
                distance.append(r)


            new_df['listing-count'] = pd.Series(count_list)
            new_df['average-daily-rate'] = pd.Series(price_list)
            new_df['distance']= pd.Series(distance)

            result = to_xml(new_df)

            return Response(result)

        except:
            res = {"code": 404, "message": "Data not Found!"}
            return Response(data=json.dumps(res), status=status.HTTP_404_NOT_FOUND)

