from Google import create_service
import base64
import pandas as pd
import json
import email
from email.parser import BytesParser
import streamlit as st
import plotly.graph_objects as Go
import re
import numpy as np


community_score = 117 # random values 
past_week_score = 102 # 

## Oauth2.0  gmail api
CLIENT_FILE = 'credentials.json'
API_SERVICE = 'gmail'
VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

st.header("Greenr")
st.header("Obtaining mail data from Gmail API")
st.write("Through the Gmail API we can fetch the last 100 emails of the users. This demo is only avaible for Gmail accounts that have permission. As per Google Cloud Api requirements. ")
data = create_service(CLIENT_FILE, API_SERVICE, VERSION, SCOPES)

response = data.users().messages().list(userId = 'me').execute()

df= []
for i in response['messages']:
    messageraw =data.users().messages().get(userId='me', id=i['id']).execute()
    m = messageraw['snippet']
    df.append([i['id'], m])

df1 = pd.DataFrame(df)
st.write(df1)


# accessing the json ile from google takeout
st.header("Collecting location data")
st.write("As we don't have time to start tracking location data now and we don;t have access to past location data, this demo will run on specific past location data coming from google timeline takout. where location data can be exported month by month in a json file. Ideally, in a real life application the location data would be collected in real time.")
file = st.file_uploader('upload json file' )

if file is not None:
   
    df = json.load(file)
    df= pd.DataFrame(df)
    l=[]
    for i in range(0, len(df)):

        if 'activitySegment' in str(df['timelineObjects'][i]): #selecting movements only
            l.append(df['timelineObjects'][i])

    lst = []
    for i in l:
        #changing to datetime format for graphs
        lst.append([i['activitySegment']['distance'], i['activitySegment']['activityType'], i['activitySegment']['duration']['startTimestamp'], i['activitySegment']['duration']['endTimestamp']])
    df = pd.DataFrame(lst)

    df['startTime'] = pd.to_datetime(df[2])
    df['endTime'] = pd.to_datetime(df[3])
    df = df.drop([2,3], axis = 1)
    st.write(df)
    #piechart
    piedata = df.groupby(df[1]).sum()
    st.header("activity data visualization")
    fig = Go.Figure(data=[Go.Pie(labels=piedata.index, values=piedata[0], hole=.5)])

    st.plotly_chart(fig)
    #explanation of score system
    st.header("Calculating Score")
    st.write('In a first stage we solely rely on location and email data, focusing especially on boarding passes and electricity bills. In a second moment we expect to integrate the service with IoT devices.')
    st.write('The scope of this Demo is to show a proof of concept, unfortunately we do not have a optimized scoring function yet.')
    st.write('Ideally we would use natural language processing to estimate and recover information from the email flow, however for the scope of this demo we focused on a much simpler version, by just looking for keyword in the text snippet of the emails, which did not yield the expected results')
    st.write('The score is calculated based on a variety of facotrs, which will need to to be fine tuned. The scores are going to be relative to each week and each community as it is difficult assess environmental sustainability')

 
    #results display
    score = round((piedata[0]['IN_PASSENGER_VEHICLE'])/(piedata[0].drop(['IN_PASSENGER_VEHICLE'], axis = 0)).sum(), 2)*100
    col1, col2 = st.columns(2)
    col1.metric(label="Weekly score", value=score, delta=f'{round((score-past_week_score)/(past_week_score),2)} since last week')
    col2.metric(label='comparison with Communtiy', value=community_score, delta=f'{score-community_score} since last week')
    past_week_score =score
    st.header("Calculating Score")
    st.write('In a first stage we solely rely on location and email data, focusing especially on boarding passes and electricity bills. In a second moment we expect to integrate the service with IoT devices.')
    st.write('The scope of this Demo is to show a proof of concept, unfortunately we do not have a optimized scoring function yet.')
    st.write('Ideally we would use natural language processing to estimate and recover information from the email flow, however for the scope of this demo we focused on a much simpler version, by just looking for keyword in the text snippet of the emails, which did not yield the expected results')
    st.write('The score is calculated based on a variety of facotrs, which will need to to be fine tuned. The scores are going to be relative to each week and each community as it is difficult assess environmental sustainability')

 
