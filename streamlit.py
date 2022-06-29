
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import altair as alt
from altair import datum
#from sqlalchemy import create_engine
#from sqlalchemy import text
#redshift_url = "{d}+{driver}://{u}:{p}@{h}:{port}/{db}".format(d='redshift',driver='psycopg2',u=st.secrets["username"],p=st.secrets["password"],h=st.secrets["host"],port=st.secrets["port"],db=st.secrets["dbname"])
#redshift_eng = create_engine(redshift_url)
#a = pd.read_sql_query(""" select the_store_id,business_date,meal_time,release_branch,escalation_type from pa_prod.quicksight_golden_arches ga
#""",con=redshift_eng)

a=pd.read_csv('mock_store_escalation.csv')
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



heatmap=alt.Chart(
    order_count,
    title="Live Store Status"
).mark_rect().encode(
    x=alt.X('yearmonthdate(business_date):O', title='Business Date'),
    y=alt.Y('store:O', title='Store ID'),
    color=alt.condition("datum.the_chat_id == 0", alt.value('#3c3838'), 
                        alt.Color('the_chat_id:Q', scale=alt.Scale(scheme="redyellowgreen"),
                        legend=alt.Legend(title='Order Volume'))),
    tooltip=[
        alt.Tooltip('store:O', title='store ID'),
        alt.Tooltip('yearmonthdate(business_date)', title='Date'),
        alt.Tooltip('the_chat_id:Q', title='Orders')
    ]
).properties(width=800)

filtered_orders['Legend']='Live Today'
order_count['Legend']='Cumulative Live Stores'


line = alt.Chart(filtered_orders).properties(width=800).mark_line().encode(
    x=alt.X('yearmonthdate(business_date):O',title='Business Date'),
    y=alt.Y('distinct(store):Q', title='Live Stores'),
    color='Legend'
)
cum_sum=alt.Chart(order_count).properties(width=800).mark_line(strokeDash=[1,1]).encode(
    x=alt.X('yearmonthdate(business_date):O'),
    y='distinct(store):Q',
    color='Legend'
)

labels = alt.Chart(filtered_orders).mark_text(dx=3,dy=-5,size=7).encode(
                                            x=alt.X('yearmonthdate(business_date):O',sort="descending"),
                                            y='distinct(store):Q',
                                            text=alt.Text('distinct(store):Q'))
                                        
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['business_date'], empty='none')

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = alt.Chart(filtered_orders).mark_point().encode(
    x=alt.X('yearmonthdate(business_date):O'),
    opacity=alt.value(0),
).add_selection(
    nearest
)

# Draw points on the line, and highlight based on selection
points = line.mark_point().transform_filter(
    nearest
)

# Draw text labels near the points, and highlight based on selection
text = line.mark_text(align='left', dx=5, dy=7).encode(
    text=alt.Text('distinct(store):Q'),
    color=alt.value('#3c3838')
).transform_filter(
    nearest
)

# Draw text labels near the points, and highlight based on selection
date_text = cum_sum.mark_text(align='left', dx=5, dy=-15).encode(
    text=alt.Text('yearmonthdate(business_date):O'),
    color=alt.value('#3c3838')
).transform_filter(
    nearest
)

# Draw points on the line, and highlight based on selection
points2 = cum_sum.mark_point().transform_filter(
    nearest
)

# Draw text labels near the points, and highlight based on selection
text2 = cum_sum.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.Text('distinct(store):Q'),
    color=alt.value('#3c3838')
).transform_filter(
    nearest
)

# Draw a rule at the location of the selection
rules = alt.Chart(filtered_orders).mark_rule(color='gray').encode(
    x=alt.X('yearmonthdate(business_date):O'),
).transform_filter(
    nearest
)

# Put the five layers into a chart and bind the data
total=alt.vconcat(alt.layer(
    line, cum_sum,selectors, points, rules, text, points2, text2, date_text
), heatmap).properties(padding=15)


st.altair_chart(total)





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
