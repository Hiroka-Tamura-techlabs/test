
import streamlit as st
import pandas as pd
import plotly.graph_objects as go




a=pd.read_csv('mock_store_escalation.csv')
a1=a[(a['the_store_id']=='23476') &(a['the_store_id']=='7360') ]
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

st.plotly_chart(fig)

import plotly.express as px
df = px.data.iris()
fig2 = px.parallel_coordinates(df, color="species_id",
                              dimensions=['sepal_width', 'sepal_length', 'petal_width',
                                          'petal_length'],
                              color_continuous_scale=px.colors.diverging.Tealrose,
                              color_continuous_midpoint=2)
st.plotly_chart(fig2)
