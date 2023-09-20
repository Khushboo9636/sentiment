from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import plotly.express as px
mymodel=SentimentIntensityAnalyzer()
mymodel
#permission
f=InstalledAppFlow.from_client_secrets_file('key.json',['https://www.googleapis.com/auth/spreadsheets'])
cred=f.run_local_server(port=0)
#create a service
service=build('Sheets','v4',credentials=cred).spreadsheets().values()
#Retrive Data from Google Sheet
d=service.get(spreadsheetId='1AtPZyyWgqbpVuWoIwNtitJMaKVYO_bjGZ10zdk1c87g',range='A1:B').execute()
print(d['values'])
mycolumns=d['values'][0]
mydata=d['values'][1:]
df=pd.DataFrame(data=mydata,columns=mycolumns)
pos=0
neg=0
neu=0

for i in range(0,len(df)):
    k=df._get_value(i,'Review')
    pred = mymodel.polarity_scores(k)
    if(pred['compound']>0.5):
        pos=pos+1
    elif(pred['compound']<-0.5):
        neg=neg+1
    else:
        neu=neu+1
posper=(pos/len(df))*100
negper =(neg/len(df))*100
neuper=(neu/len(df)) *100
print("positive: ", posper)
print("negative: ",negper)
print("neutral: ",neuper)
fig=px.pie(values=[posper,negper, neuper],names=['Positive','Negative','Neutral'])
fig.show()

