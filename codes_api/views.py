
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
    Retrieve data from api and return xml file
    """

    #get the data from api passing the postcode 
    def get(self, request, post_code):
        
        try:
            #callin help function to load Pandas from csv file
            df = load_file_to_pandas('listings.csv')                

            #request from api url
            url = 'http://api.postcodes.io/outcodes/'+ post_code
            r = requests.get(url)

            # convert JSON format
            postcodes = r.json()

            #retrieve the ward dat from json
            ward = postcodes['result']['admin_ward']

            #create empty list to store future data
            count_list = []
            location_list = []
            price_list = []


            # loop over the data to bring the desire ones.
            for w in ward:
                location = df.loc[df['neighbourhood']== w]
                result_df = location[['neighbourhood','price']]
                # calculate the mean (average) price
                avr_price = location['price'].mean()
                # find the amount of indexes 
                index = location.index
                number_of_rows = len(index)

                # add data to lists
                count_list.append(number_of_rows)
                price_list.append(avr_price)
                location_list.append(w)

            # assing DataFrame structure
            data =  { 'listing-count': count_list, 'average-daily-rate': price_list , 'location': location_list }

            # Pands data frame structure          
            outcode_df = pd.DataFrame(data, columns = ['listing-count','average-daily-rate','location'])

            # result paased to help function to convert to xml
            result = to_xml(outcode_df)

            # response xml
            return Response(result)
            
        #  if no data consistent return 404 
        except:
            res = {"code": 404, "message": "Data not Found!"}
            return Response(data=json.dumps(res), status=status.HTTP_404_NOT_FOUND)


# Class to retrieve Nearest Outcodes
class NexusView(APIView):

    #permission_classes = [ReadOnly]

    # retrieve dat from api and compare to csv by passing outcode
    def get(self, request, post_code):

        try:
            # function to load csv file
            df = load_file_to_pandas('listings.csv')

            # API url to grab data from
            url = 'http://api.postcodes.io/outcodes/' + post_code + '/nearest'
            r = requests.get(url)
            #convert to json 
            postcodes = r.json()

            # get results from json file
            result = postcodes['result']

            # empty lists to store data
            locations = []
            longitude = []
            latitude = []
            new_result = []


            # get rid of unnecesary data from json
            for k in result:
                del k['northings']
                del k['eastings']
                del k['admin_district']
                del k['parish']
                del k['country']
                del k['admin_county']
                # append to new list the clean data
                new_result.append(k)


            
            # append necesary data
            for ward in new_result:       
                locations.append(ward['admin_ward'])
                longitude.append(ward['longitude'])
                latitude.append(ward['latitude'])

            # create list of dictionaries from cleaned data to Pandas DataFrame
            new_df = pd.DataFrame.from_dict(new_result)

            # emoty lists to store data
            count_list = []
            location_list = []
            price_list = []
            distance = []

            # loop over desire data and perform desire operations
            for l in locations:
                for n in l:
                    location = df.loc[df['neighbourhood']== n]
                    result_df = location[['neighbourhood','price']]
                    # calculate avergae price
                    avr_price = location['price'].mean()
                    # calcualte amount of indexes
                    index = location.index
                    number_of_rows = len(index)

                    # append to lists
                    count_list.append(number_of_rows)
                    price_list.append(avr_price)
                    location_list.append(n)

            # add to list the float values of latitude and longitude
            long_list = [float(i) for i in longitude]
            lat_list = [float(i) for i in latitude]

            # find out length of the desire amount of distance to calcualte
            n = len(long_list)

            # calculate list of distances
            for i in range(0,n):
                r = calculate_distance(long_list[0],lat_list[0],long_list[i],lat_list[i])
                distance.append(r)

            # adding columns to pandas dataframe
            new_df['listing-count'] = pd.Series(count_list)
            new_df['average-daily-rate'] = pd.Series(price_list)
            new_df['distance']= pd.Series(distance)

            # result to xml helper function
            result = to_xml(new_df)

            # return response
            return Response(result)

        # if no consistent data return 404
        except:
            res = {"code": 404, "message": "Data not Found!"}
            return Response(data=json.dumps(res), status=status.HTTP_404_NOT_FOUND)

