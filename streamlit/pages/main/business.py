#import conexion
import streamlit as st
import pandas as pd 
from multiprocessing import Value
from typing import List
#import conexion sale error :(




#def cql_to_pandas(cql_query,cassandra_session):
#    def pandaspark_factory(colnames, rows):\
#        return pd.DataFrame(rows, columns=colnames)
#    cassandra_session.row_factory = pandaspark_factory
#    cassandra_session.default_fetch_size = None
#    result = cassandra_session.execute(cql_query, timeout=None)
#    return result._current_rows


#def select_business(): 
#    #business = pd.read_csv(r'business_1000.csv')
#    #name_business = business['name']
#
#    option = st.selectbox(
#        'My businesses',
#        (name_business.to_list()))
#
#    st.write('You selected:', option)


#def func():
#    with st.form(key='searchForm'):
#        search_movie = st.text_input("Search Movie")
#        ubmit_button = st.form_submit_button(label='Search')
business = pd.read_csv(r'C:\Users\julie\OneDrive\Escritorio\trabajogrupal\trabajofinal\streamlit\data\business_1000.csv')
name_business = business['name']
#checkin = pd.read_csv(r'C:\Users\julie\OneDrive\Escritorio\trabajogrupal\trabajofinal\streamlit\checkin_1000.csv')
#review = pd.read_csv(r'C:\Users\julie\OneDrive\Escritorio\trabajogrupal\trabajofinal\streamlit\review_1000.csv') 
#business = cn.businessdf
#name_business = business['name']
#checkin = cn.checkindf
#review = cn.reviewdf





#def l(filtro):
#   ids = filtro['business_id'].to_list()
#   review_stars = filtro['stars'].mean()
#   review1 = review.loc[review['business_id'].isin(ids)]
#   checkin1 = review.loc[review['business_id'].isin(ids)]
#   review1['positive_score'] = review1['pos_reviews'] / ( review1['neg_reviews'] + review1['pos_reviews'])
#   Positive_sentiment = review1['positive_score'].mean()
#   review_total = review1.shape[0]
#   number_visits = checkin1['number_visits'].sum()
#   st.markdown("### Account Summary")
#   metrics = st.columns(6)
#   metrics[0].metric('Review Total',review_total, delta=None, delta_color="normal")
#   #metrics[1].image(im,width=50)
#   metrics[1].metric('Review stars', round(review_stars, 2), delta=None, delta_color="normal")
#   metrics[2].metric('Positive sentiment', f'{round(Positive_sentiment, 2)*100}%', delta=None, delta_color="normal")
#   metrics[3].metric('Influencer Score', '98,7%', delta=None, delta_color="normal")
#   metrics[4].metric('Top Hour', '18:00', delta=None, delta_color="normal")
#   metrics[5].metric('Number_visits', number_visits)


def selete_business(): 
    #business_name = cql_to_pandas("""select name from yelp.business ALLOW FILTERING;""",conexion.seccion)
    option = st.selectbox(
        'My businesses',
        (name_business.to_list()))

    st.write('You selected:', option)
    #print(option)
    #if option in option:
    #    filtro = business[business['name'] == option]
    #    st.markdown("### Account Summary")
    #    l(filtro)
    
#print(selete_business())
