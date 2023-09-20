import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import plotly.express as px
st.set_page_config(page_title='SENTIMENT ANALYSIS SYSTEM',page_icon='random')
menu_options = {
    "Home": "color: red; font-size:50px",
    "Analyze Sentiment": "color: yellow;",
    "Visualize the Results": "color: green;",
    "CSV Files": "color: yellow;"
}

st.sidebar.image("https://genaikit.com/gif/SentimentAnalysis.gif")
st.sidebar.image("https://www.radaco.net/wp-content/uploads/2020/11/Global-Segments-Size-Industry-Growth-and-Recent-Trends-by-Forecast-to-2027-%E2%80%93-Food-Beverage-Herald.gif")



choice=st.sidebar.selectbox("My Menu", list(menu_options.keys()))

st.header(choice)

st.write(f'<p style="{menu_options[choice]}">{choice}</p>', unsafe_allow_html=True)
if(choice=="Home"):
    st.markdown("<h1 style= 'text-align:center;color:Red;'>SENTIMENT ANALYSIS SYSTEM</h1>",unsafe_allow_html=True)
    st.image("https://miro.medium.com/proxy/1*_JW1JaMpK_fVGld8pd1_JQ.gif")
    st.markdown("<center><h1 style= 'color:Red;'>WELCOME</h1></center>",unsafe_allow_html=True)
    st.image("https://blog.ttisi.com/hs-fs/hubfs/072221_blog.gif?width=2400&name=072221_blog.gif")
elif(choice=="Analyze Sentiment"):
    st.image("https://i.pinimg.com/originals/52/ad/6a/52ad6a11c1dcb1692ff9e321bd520167.gif")
    url=st.text_input("Enter Google Sheet URL")
    r=st.text_input("Enter Range")
    c=st.text_input("Enter Column")
    btn = st.button("Analyze")
    if btn:
        if 'cred' not in st.session_state:
            f=InstalledAppFlow.from_client_secrets_file('key.json',['https://www.googleapis.com/auth/spreadsheets'])
            st.session_state['cred']=f.run_local_server(port=0)
        mymodel=SentimentIntensityAnalyzer()
        service=build('Sheets','v4',credentials=st.session_state['cred']).spreadsheets().values()
        d=service.get(spreadsheetId=url,range=r).execute()
        mycolumns=d['values'][0]
        mydata=d['values'][1:]
        df=pd.DataFrame(data=mydata,columns=mycolumns)
        l=[]
        for i in range(0,len(df)):
            k=df._get_value(i,c)
            pred = mymodel.polarity_scores(k)
            if(pred['compound']>0.5):
                l.append("positive")
            elif(pred['compound']<-0.5):
                l.append("Negative")
            else:
                l.append("Neutral")
        df['Sentiment']=l
        st.dataframe(df)
        df.to_csv("Review.csv",index=False)
        st.header("This data has been saved by name of review.csv")
elif(choice=="Visualize the Results"):
    st.image("https://cdn.dribbble.com/users/72535/screenshots/2630779/data_visualization_by_jardson_almeida.gif")
    st.image("https://cdn.dribbble.com/users/3083633/screenshots/8258363/media/55d788add27fc8029c22aefe21603f73.gif")
    
    choice2=st.selectbox("Choose Visualization",("None","Pie","Histogram","Scatter Plot"))
    if(choice2=="Pie"):
        df=pd.read_csv("Review.csv")
        posper=(len(df[df['Sentiment']=='positive'])/len(df))*100
        negper=(len(df[df['Sentiment']=='Negative'])/len(df))*100
        neuper=(len(df[df['Sentiment']=='Neutral'])/len(df))*100
        fig=px.pie(values=[posper,negper,neuper],names=['positive','Negative','Neutral'])
        st.plotly_chart(fig)
    elif(choice2=="Histogram"):
        t=st.text_input("Choose any Categorical Column")
        if t:
            df=pd.read_csv("Review.csv")
            fig=px.histogram(x=df['Sentiment'],color=df[t])
            st.plotly_chart(fig)
    elif(choice2=="Scatter Plot"):
        df=pd.read_csv("Review.csv")
        x=st.selectbox("Choose any continious data for x-axis",df.columns)
        y=st.selectbox("Choose any continious data for y-axis",df.columns)
        if st.button("Generate Scatter Plot") and x and y:
            fig = px.scatter(df, x=x, y=y, title="Scatter Plot Representation", labels={x: 'X-axis', y: 'Y-axis'})
            st.plotly_chart(fig)
        
elif(choice=="CSV Files"):
    st.image("https://i.pinimg.com/originals/52/ad/6a/52ad6a11c1dcb1692ff9e321bd520167.gif")
    path=st.text_input("Enter Files Path")
    c=st.text_input("Enter Column")
    btn = st.button("Analyze")
    if btn:
        if 'cred' not in st.session_state:
            f=InstalledAppFlow.from_client_secrets_file('key.json',['https://www.googleapis.com/auth/spreadsheets'])
            st.session_state['cred']=f.run_local_server(port=0)
        mymodel=SentimentIntensityAnalyzer()
        df=pd.read_csv(path)
        l=[]
        for i in range(0,len(df)):
            k=df._get_value(i,c)
            pred = mymodel.polarity_scores(k)
            if(pred['compound']>0.5):
                l.append("positive")
            elif(pred['compound']<-0.5):
                l.append("Negative")
            else:
                l.append("Neutral")
        df['Sentiment']=l
        st.dataframe(df)
        df.to_csv("Review.csv",index=False)
        st.header("This data has been saved by name of review.csv")
   
    
    
            
            

    
