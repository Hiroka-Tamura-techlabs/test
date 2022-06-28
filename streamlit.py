
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy import text
redshift_url = "{d}+{driver}://{u}:{p}@{h}:{port}/{db}".format(d='redshift',driver='psycopg2',u=st.secrets["username"],p=st.secrets["password"],h=st.secrets["host"],port=st.secrets["port"],db=st.secrets["dbname"])
redshift_eng = create_engine(redshift_url)
a = pd.read_sql_query(""" select the_store_id,business_date,meal_time,release_branch,escalation_type from pa_prod.quicksight_golden_arches ga
""",con=redshift_eng)

#a=pd.read_csv('mock_store_escalation.csv')
a1=a[(a['the_store_id']==23476) |(a['the_store_id']==7350)]
a1['meal_time'].replace(['breakfast','lunch','snack','dinner','evening','late_night'],
                        [0,1,2,3,4,5], inplace=True)


fig = go.Figure(data=
    go.Parcoords(
        #line_color='blue',
        line = dict(color = a1['the_store_id']),
        dimensions = list([
            dict(range = [0,6],
                 tickvals = [0,1,2,3,4,5],
                 ticktext = ['breakfast','lunch','snack','dinner','evening','late_night'],
                 label = 'Meal Time', values = a1['meal_time']),
            dict(range = [0,1],
                label = 'Escalation Ind', values = a1['escalated_ind']),
        ])
    )
)
a['the_store_id_cat'] = a['the_store_id'].astype('str')
fig4 = px.parallel_categories(a, dimensions=['meal_time', 'release_branch', 'escalated_ind'],
                labels={'meal_time':'Meal Time', 'release_branch':'Release Branch', 'escalated_ind':'Escalated or Not'})


st.plotly_chart(fig)
st.plotly_chart(fig4)


slist = a['the_store_id_cat'].unique()
store1 = st.sidebar.selectbox("Select store 1:",slist)
store2 = st.sidebar.selectbox("Select store 2:",slist)
fig5= px.parallel_categories(a[(a['the_store_id_cat']==store1) | (a['the_store_id_cat']==store2)], 
                             dimensions=['meal_time', 'release_branch', 'escalated_ind'],
                             labels={'meal_time':'Meal Time', 'release_branch':'Release Branch', 'escalated_ind':'Escalated or Not'},
                             color='the_store_id')

st.plotly_chart(fig5)



iris = px.data.iris()
fig2 = px.parallel_coordinates(iris, color="species_id",
                              dimensions=['sepal_width', 'sepal_length', 'petal_width',
                                          'petal_length'],
                              color_continuous_scale=px.colors.diverging.Tealrose,
                              color_continuous_midpoint=2)
#st.plotly_chart(fig2)

df = pd.read_csv("https://raw.githubusercontent.com/bcdunbar/datasets/master/iris.csv")

fig3 = go.Figure(data=
    go.Parcoords(
        line = dict(color = df['species_id'],
                   colorscale = [[0,'purple'],[0.5,'lightseagreen'],[1,'gold']]),
        dimensions = list([
            dict(range = [0,8],
                constraintrange = [4,8],
                label = 'Sepal Length', values = df['sepal_length']),
            dict(range = [0,8],
                label = 'Sepal Width', values = df['sepal_width']),
            dict(range = [0,8],
                label = 'Petal Length', values = df['petal_length']),
            dict(range = [0,8],
                label = 'Petal Width', values = df['petal_width'])
        ])
    )
)
#st.plotly_chart(fig3)
