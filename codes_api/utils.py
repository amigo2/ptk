from haversine import haversine, Unit
import pandas as pd




# funtion hepler to caltulate distance giving 
# 2 long and lat parameters
def calculate_distance(long1,lat1,long2,lat2):
    a = (long1, lat1)
    b = (long2, lat2)
    return haversine(a,b)



# Helper function to convert to xml
def to_xml(df):
        def row_xml(row):
            xml = ['<outcode>']
            for i, col_name in enumerate(row.index):
                xml.append('  <{0}>{1}</{0}>'.format(col_name, row.iloc[i]))
            xml.append('</outcode>')
            return '\n'.join(xml)
        res = '\n'.join(df.apply(row_xml, axis=1))
        return res



def load_file_to_pandas(filename):

        try:
            df = pd.read_csv(filename)
        except pd.errors.EmptyDataError:
            print('Note: listing.csv was not found, please make sure is in the right folder.')
            pass
        return df

