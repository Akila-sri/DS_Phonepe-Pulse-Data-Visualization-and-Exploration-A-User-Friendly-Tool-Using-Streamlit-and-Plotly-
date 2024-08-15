import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector
import plotly.express as px
import requests
import json
from PIL import Image

#SQL CONNECTION

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="phonepe"
)
cur= conn.cursor()

#agg_transaction_df
cur.execute('select * from aggregate_transaction' )
table1=cur.fetchall()
conn.commit()

agg_trans=pd.DataFrame(table1,columns=('states','years','quarter','trans_type','trans_count','trans_amount'))

#agg_user_df
cur.execute('select * from aggregate_user' )
table2=cur.fetchall()
conn.commit()

agg_user=pd.DataFrame(table2,columns=('states','years','quarter','Brands','trans_count','Percentage'))

#agg_ins_df
cur.execute('select * from aggregate_insurance' )
table3=cur.fetchall()
conn.commit()

agg_ins=pd.DataFrame(table3,columns=('states','years','quarter','trans_type','trans_count','trans_amount'))

#map_transaction_df
cur.execute('select * from map_transaction' )
table4=cur.fetchall()
conn.commit()

map_trans=pd.DataFrame(table4,columns=('states','years','quarter','District','trans_count','trans_amount'))

#map_user_df
cur.execute('select * from map_user' )
table5=cur.fetchall()
conn.commit()

map_user=pd.DataFrame(table5,columns=('states','years','quarter','District','RegisteredUsers','App_opens'))

#map_ins_df
cur.execute('select * from map_insurance' )
table6=cur.fetchall()
conn.commit()

map_ins=pd.DataFrame(table6,columns=('states','years','quarter','District','trans_count','trans_amount'))

#top_transaction_df
cur.execute('select * from top_transaction' )
table7=cur.fetchall()
conn.commit()

top_trans=pd.DataFrame(table7,columns=('states','years','quarter','pincode','trans_count','trans_amount'))

#top_user_df
cur.execute('select * from top_user' )
table8=cur.fetchall()
conn.commit()

top_user=pd.DataFrame(table8,columns=('states','years','quarter','pincode','RegisteredUsers'))

#top_ins_df
cur.execute('select * from top_insurance' )
table9=cur.fetchall()
conn.commit()

top_ins=pd.DataFrame(table9,columns=('states','years','quarter','pincode','trans_count','trans_amount'))

#function1(transaction_count_amount_yearbased)
def transaction_count_amount_y(df,year):
    tacy=df[df["years"]==year]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("states")[["trans_count","trans_amount"]].sum()
    tacyg.reset_index(inplace=True)
    

    c1,c2=st.columns(2)
    with c1:
        fig_amount=px.bar(tacyg,x="states",y="trans_amount",title=f"{year} TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Purples_r,height=450,width=400)
        st.plotly_chart(fig_amount)

    with c2:
        fig_count=px.bar(tacyg,x="states",y="trans_count",title=f"{year} TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.deep_r,height=450,width=400)
        st.plotly_chart(fig_count)


    c1,c2=st.columns(2) 
    with c1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india=px.choropleth(tacyg,geojson=data1,locations="states",featureidkey="properties.ST_NM",color="trans_amount",color_continuous_scale="rainbow",
                                    range_color=(tacyg["trans_amount"].min(),tacyg["trans_amount"].max()),
                                    hover_name="states",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",height=450,width=500)


        fig_india.update_geos(visible=False)
        st.plotly_chart(fig_india)

    with c2:

        fig_india1=px.choropleth(tacyg,geojson=data1,locations="states",featureidkey="properties.ST_NM",color="trans_count",color_continuous_scale="rainbow",
                                range_color=(tacyg["trans_count"].min(),tacyg["trans_count"].max()),
                                hover_name="states",title=f"{year} TRANSACTION COUNT",fitbounds="locations",height=450,width=500)

        fig_india1.update_geos(visible=False)
        st.plotly_chart(fig_india1)
        return tacy


#function2(transaction_count_amount_quarterbased)
def transaction_count_amount_y_Q(df,quarter):
        tacy=df[df["quarter"]==quarter]
        tacy.reset_index(drop=True,inplace=True)

        tacyg=tacy.groupby("states")[["trans_count","trans_amount"]].sum()
        tacyg.reset_index(inplace=True)
    
        c1,c2=st.columns(2)
        with c1:
            fig_amount=px.bar(tacyg,x="states",y="trans_amount",title=f"QUARTER {quarter} TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Purples_r,height=450,width=400)
            st.plotly_chart(fig_amount)
        with c2:
            fig_count=px.bar(tacyg,x="states",y="trans_count",title=f"QUARTER {quarter} TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.deep_r,height=450,width=400)
            st.plotly_chart(fig_count)

        c1,c2=st.columns(2)

        with c1:
            url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response=requests.get(url)
            data1=json.loads(response.content)
            states_name=[]
            for feature in data1["features"]:
                states_name.append(feature["properties"]["ST_NM"])

            states_name.sort()

            fig_india=px.choropleth(tacyg,geojson=data1,locations="states",featureidkey="properties.ST_NM",color="trans_amount",color_continuous_scale="rainbow",
                                    range_color=(tacyg["trans_amount"].min(),tacyg["trans_amount"].max()),
                                    hover_name="states",title=f"QUARTER {quarter}  TRANSACTION AMOUNT",fitbounds="locations",height=450,width=500)


            fig_india.update_geos(visible=False)
            st.plotly_chart(fig_india)
        with c2:
            fig_india1=px.choropleth(tacyg,geojson=data1,locations="states",featureidkey="properties.ST_NM",color="trans_count",color_continuous_scale="rainbow",
                                    range_color=(tacyg["trans_count"].min(),tacyg["trans_count"].max()),
                                    hover_name="states",title=f"QUARTER {quarter}  TRANSACTION COUNT",fitbounds="locations",height=450,width=500)

            fig_india1.update_geos(visible=False)
            st.plotly_chart(fig_india1)
        return tacy 

#function 3(piechart for trans_type_states)
def agg_trans_trans_type(df,states):
    tacy=df[df["states"]==states]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("trans_type")[["trans_count","trans_amount"]].sum()
    tacyg.reset_index(inplace=True)
    c1,c2=st.columns(2)
    with c1:
        fig_pie=px.pie(data_frame=tacyg,names="trans_type",values="trans_amount",width=500,title=f"{states.upper()} TRANSACTION AMOUNT",hole=0.5)
        st.plotly_chart(fig_pie)
    with c2:
        fig_pie_1=px.pie(data_frame=tacyg,names="trans_type",values="trans_count",width=500,title=f"{states.upper()} TRANSACTION COUNT",hole=0.5)
        st.plotly_chart(fig_pie_1)

#function_4(agg_user_y)
def agg_user_plot1(df,year):
    aguy=df[df["years"]==year]
    aguy.reset_index(drop=True,inplace=True)

    aguyg=aguy.groupby("Brands")[["trans_count"]].sum()
    aguyg.reset_index(inplace=True)
  

    fig_tcount=px.bar(aguyg,x="Brands",y="trans_count",title=f"{year} BRANDS & TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Purples_r,hover_name="Brands",height=400,width=500)
    st.plotly_chart(fig_tcount)
    return aguy

#function_5(agg_user_q)
def agg_user_plot2(df,quarter):
    aguyq=df[df["quarter"]==quarter]
    aguyq.reset_index(drop=True,inplace=True)

    aguyqg=aguyq.groupby("Brands")[["trans_count"]].sum()
    aguyqg.reset_index(inplace=True)

    fig_tcount1=px.bar(aguyqg,x="Brands",y="trans_count",title=f"{quarter}QUARTER BRANDS & TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Purples_r,hover_name="Brands",height=400,width=500)
    st.plotly_chart(fig_tcount1)
    return aguyq
   

#function_6(agg_use state analysis)   
def agg_user_plot3(df,state):
   auyqs=df[df["states"]==state]
   auyqs.reset_index(drop=True,inplace=True)

   fig_line=px.line(auyqs,x="Brands",y="trans_count",hover_data="Percentage",title=f"{state.upper()} BRANDS,TRANSACTION COUNT,PERCENTAGE",width=500,markers=True,hover_name="Brands")
   st.plotly_chart(fig_line)
    
#function_7(map_ins_dist)
def map_ins_dist(df,states):
    tacy=df[df["states"]==states]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("District")[["trans_count","trans_amount"]].sum()
    tacyg.reset_index(inplace=True)

    c1,c2=st.columns(2)
    with c1:
        fig_bar=px.bar(data_frame=tacyg,x="trans_count",y="District",width=500,title=f"{states.upper()} TRANSACTION COUNT")
        st.plotly_chart(fig_bar)
    with c2:
        fig_bar1=px.bar(data_frame=tacyg,x="trans_amount",y="District",width=500,title=f"{states.upper()} TRANSACTION AMOUNT")
        st.plotly_chart(fig_bar1)

#function_8(map_user_plot1)
def map_user_plot1(df,years):
    aguy=df[df["years"]==years]
    aguy.reset_index(drop=True,inplace=True)

    aguyg=aguy.groupby("states")[["RegisteredUsers","App_opens"]].sum()
    aguyg.reset_index(inplace=True)

    fig_line=px.line(aguyg,x="states",y=["RegisteredUsers","App_opens"],title=f"{years} REGISTEREDUSERS & APP_OPENS",width=700,markers=True,hover_name="states")
    st.plotly_chart(fig_line)
    return aguy

#function_9(map_user_quarter)
def map_user_plot2(df,quarters):
    aguyq=df[df["quarter"]==quarters]
    aguyq.reset_index(drop=True,inplace=True)


    aguyqg=aguyq.groupby("states")[["RegisteredUsers","App_opens"]].sum()
    aguyqg.reset_index(inplace=True)

    fig_tcount1=px.line(aguyqg,x="states",y=["RegisteredUsers","App_opens"],title=f"{quarters}QUARTER REGISTEREDUSERS & APP_OPENS",markers=True,color_discrete_sequence=px.colors.sequential.Purples_r,height=400,width=500)
    st.plotly_chart(fig_tcount1)
    return aguyq

#function_10(map_user_statewise)
def map_user_plot3(df,states):
    aguyqs=df[df["states"]==states]
    aguyqs.reset_index(drop=True,inplace=True)
  

    fig_tcount1=px.bar(aguyqs,x="RegisteredUsers",y="District",title="RegisteredUsers",color_discrete_sequence=px.colors.sequential.Purples_r,height=400,width=500)
    st.plotly_chart(fig_tcount1)
        
    fig_tcount2=px.bar(aguyqs,x="App_opens",y="District",title=" App_opens",color_discrete_sequence=px.colors.sequential.Purples_r,height=400,width=500)
    st.plotly_chart(fig_tcount2)

#function_11(top_insurance)
def top_insurance_plot1(df,states):
    aguyq=df[df["states"]==states]
    aguyq.reset_index(drop=True,inplace=True)
    
    c1,c2=st.columns(2)
    with c1:
        fig_tcount1=px.bar(aguyq,x="quarter",y="trans_count",title=" Trans_count",color_discrete_sequence=px.colors.sequential.Blackbody,hover_data='pincode',height=400,width=500)
        st.plotly_chart(fig_tcount1)
    with c2:
        fig_tcount2=px.bar(aguyq,x="quarter",y="trans_amount",title=" Trans_amount",color_discrete_sequence=px.colors.sequential.Purples_r,height=400,width=500)
        st.plotly_chart(fig_tcount2)

#function_12(top_user)
def top_user_plot1(df,years):
    aguy=df[df["years"]==years]
    aguy.reset_index(drop=True,inplace=True)

    aguyg=aguy.groupby(["states","quarter"])[["RegisteredUsers"]].sum()
    aguyg.reset_index(inplace=True)
    

    fig_tcount1=px.bar(aguyg,x="states",y="RegisteredUsers",color="quarter",title=f"{years} REGISTEREDUSERS",color_discrete_sequence=px.colors.sequential.Greens,height=800,width=1000,hover_name="states")
    st.plotly_chart(fig_tcount1)
    return aguy
        

#function_13(top_user)
def top_user_plot2(df,states):
    aguy=df[df["states"]==states]
    aguy.reset_index(drop=True,inplace=True)
  
    fig_bar=px.bar(aguy,x="quarter",y="RegisteredUsers",color="RegisteredUsers",hover_data="pincode",
                   width=1000,height=800,title=f"{states.upper()} REGISTERED USERS,PINCODES & QUARTER",color_continuous_scale=px.colors.sequential.Magenta)
    st.plotly_chart(fig_bar)


#topcharts
def top_chart_tamount(table_name):
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="phonepe"
        )
        cur= conn.cursor()

        #quer1
        q1=f'''select states, sum(trans_amount) as trans_amount
                from {table_name}
                group by states
                order by trans_amount desc
                limit 10'''
        cur.execute(q1)
        table=cur.fetchall()
        conn.commit()

        df_1=pd.DataFrame(table,columns=("states","trans_amount"))
        c1,c2=st.columns(2)
        with c1:
            fig_tcount=px.bar(df_1,x="states",y="trans_amount",title="TOP 10 TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Purples_r,hover_name="states",height=400,width=500)
            st.plotly_chart(fig_tcount)

        #query2
        q2=f'''select states, sum(trans_amount) as trans_amount
                from {table_name}
                group by states
                order by trans_amount 
                limit 10'''
        cur.execute(q2)
        table1=cur.fetchall()
        conn.commit()

        df_2=pd.DataFrame(table1,columns=("states","trans_amount"))
        with c2:
            fig_tcount1=px.bar(df_2,x="states",y="trans_amount",title="LAST 10 TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Purples_r,hover_name="states",height=400,width=500)
            st.plotly_chart(fig_tcount1)

        #query3
        q3=f'''select states, avg(trans_amount) as trans_amount
                from {table_name}
                group by states
                order by trans_amount;'''
        cur.execute(q3)
        table2=cur.fetchall()
        conn.commit()

        df_3=pd.DataFrame(table2,columns=("states","trans_amount"))
        
        fig_tcount2=px.bar(df_3,y="states",x="trans_amount",title="AVG OF TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Purples_r,orientation="h",hover_name="states",height=800,width=1000)
        st.plotly_chart(fig_tcount2)

def top_chart_tcount(table_name):
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="phonepe"
        )
        cur= conn.cursor()

        #quer1
        q1=f'''select states, sum(trans_count) as trans_count
                from {table_name}
                group by states
                order by trans_count desc
                limit 10'''
        cur.execute(q1)
        table=cur.fetchall()
        conn.commit()

        df_1=pd.DataFrame(table,columns=("states","trans_count"))
        c1,c2=st.columns(2)
        with c1:
            fig_tcount=px.bar(df_1,x="states",y="trans_count",title="TOP 10 TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Purples_r,hover_name="states",height=400,width=500)
            st.plotly_chart(fig_tcount)

        #query2
        q2=f'''select states, sum(trans_count) as trans_count
                from {table_name}
                group by states
                order by trans_count 
                limit 10'''
        cur.execute(q2)
        table1=cur.fetchall()
        conn.commit()

        df_2=pd.DataFrame(table1,columns=("states","trans_count"))
        with c2:
            fig_tcount1=px.bar(df_2,x="states",y="trans_count",title="LAST 10 TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Purples_r,hover_name="states",height=400,width=500)
            st.plotly_chart(fig_tcount1)

        #query3
        q3=f'''select states, avg(trans_count) as trans_count
                from {table_name}
                group by states
                order by trans_count;'''
        cur.execute(q3)
        table2=cur.fetchall()
        conn.commit()

        df_3=pd.DataFrame(table2,columns=("states","trans_count"))
        
        fig_tcount2=px.bar(df_3,y="states",x="trans_count",title="AVG OF TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Purples_r,orientation="h",hover_name="states",height=800,width=1000)
        st.plotly_chart(fig_tcount2)
    
def top_chart_reguser(table_name,state):
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="phonepe"
        )
        cur= conn.cursor()

        #quer1
        q1=f'''select District,sum(RegisteredUsers)as RegisteredUsers from {table_name}
                where states='{state}'
                group by District
                order by RegisteredUsers desc
                limit 10;'''
        cur.execute(q1)
        table=cur.fetchall()
        conn.commit()

        df_1=pd.DataFrame(table,columns=("District","RegisteredUsers"))
        c1,c2=st.columns(2)
        with c1:
            fig_tcount=px.bar(df_1,x="District",y="RegisteredUsers",title="Top 10 RegisteredUsers",color_discrete_sequence=px.colors.sequential.Purples_r,hover_name="District",height=400,width=500)
            st.plotly_chart(fig_tcount)

        #query2
        q2=f'''select District,sum(RegisteredUsers)as RegisteredUsers from {table_name}
                where states='{state}'
                group by District
                order by RegisteredUsers 
                limit 10;'''
        cur.execute(q2)
        table1=cur.fetchall()
        conn.commit()

        df_2=pd.DataFrame(table1,columns=("District","RegisteredUsers"))
        with c2:
            fig_tcount1=px.bar(df_2,x="District",y="RegisteredUsers",title="Last 10 RegisteredUsers",color_discrete_sequence=px.colors.sequential.Purples_r,hover_name="District",height=400,width=500)
            st.plotly_chart(fig_tcount1)

        #query3
        q3=f'''select District,avg(RegisteredUsers)as RegisteredUsers from {table_name}
                where states='{state}'
                group by District
                order by RegisteredUsers;'''
        cur.execute(q3)
        table2=cur.fetchall()
        conn.commit()

        df_3=pd.DataFrame(table2,columns=("District","RegisteredUsers"))
        
        fig_tcount2=px.bar(df_3,y="District",x="RegisteredUsers",title="Avg of RegisteredUsers",color_discrete_sequence=px.colors.sequential.Purples_r,orientation="h",hover_name="District",height=400,width=500)
        st.plotly_chart(fig_tcount2)

def top_chart_appopens(table_name,state):
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="phonepe"
        )
        cur= conn.cursor()

        #quer1
        q1=f'''select District,sum(App_opens)as App_opens from {table_name}
                where states='{state}'
                group by District
                order by App_opens desc
                limit 10;'''
        cur.execute(q1)
        table=cur.fetchall()
        conn.commit()

        df_1=pd.DataFrame(table,columns=("District","App_opens"))
        c1,c2=st.columns(2)
        with c1:
            fig_tcount=px.bar(df_1,x="District",y="App_opens",title="Top 10 App_opens",color_discrete_sequence=px.colors.sequential.Purples_r,hover_name="District",height=400,width=500)
            st.plotly_chart(fig_tcount)

        #query2
        q2=f'''select District,sum(App_opens)as App_opens from {table_name}
                where states='{state}'
                group by District
                order by App_opens 
                limit 10;'''
        cur.execute(q2)
        table1=cur.fetchall()
        conn.commit()

        df_2=pd.DataFrame(table1,columns=("District","App_opens"))
        with c2:
            fig_tcount1=px.bar(df_2,x="District",y="App_opens",title="Last 10 App_opens",color_discrete_sequence=px.colors.sequential.Purples_r,hover_name="District",height=400,width=500)
            st.plotly_chart(fig_tcount1)

        #query3
        q3=f'''select District,avg(App_opens)as App_opens from {table_name}
                where states='{state}'
                group by District
                order by App_opens;'''
        cur.execute(q3)
        table2=cur.fetchall()
        conn.commit()

        df_3=pd.DataFrame(table2,columns=("District","App_opens"))
        
        fig_tcount2=px.bar(df_3,y="District",x="App_opens",title="Avg of App_opens",color_discrete_sequence=px.colors.sequential.Purples_r,orientation="h",hover_name="District",height=400,width=500)
        st.plotly_chart(fig_tcount2)

def top_chart_reguser1(table_name):
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="phonepe"
        )
        cur= conn.cursor()

        #quer1
        q1=f'''select states, sum(RegisteredUsers) as RegisteredUsers
                from {table_name} 
                group by states
                order by RegisteredUsers desc
                limit 10;'''
        cur.execute(q1)
        table=cur.fetchall()
        conn.commit()

        df_1=pd.DataFrame(table,columns=("states","RegisteredUsers"))
        c1,c2=st.columns(2)
        with c1:
            fig_tcount=px.bar(df_1,x="states",y="RegisteredUsers",title="Top 10 RegisteredUsers",color_discrete_sequence=px.colors.sequential.Purples_r,hover_name="states",height=400,width=500)
            st.plotly_chart(fig_tcount)

        #query2
        q2=f'''select states, sum(RegisteredUsers) as RegisteredUsers
                from {table_name}  
                group by states
                order by RegisteredUsers 
                limit 10;'''
        cur.execute(q2)
        table1=cur.fetchall()
        conn.commit()

        df_2=pd.DataFrame(table1,columns=("states","RegisteredUsers"))
        with c2:
            fig_tcount1=px.bar(df_2,x="states",y="RegisteredUsers",title="Last 10 RegisteredUsers",color_discrete_sequence=px.colors.sequential.Purples_r,hover_name="states",height=400,width=500)
            st.plotly_chart(fig_tcount1)

     #query3
        q3=f'''select states, avg(RegisteredUsers) as RegisteredUsers
                from {table_name}  
                group by states
                order by RegisteredUsers;'''         
        cur.execute(q3)
        table2=cur.fetchall()
        conn.commit()

        df_3=pd.DataFrame(table2,columns=("states","RegisteredUsers"))
        
        fig_tcount2=px.bar(df_3,y="states",x="RegisteredUsers",title="Avg of RegisteredUsers",color_discrete_sequence=px.colors.sequential.Purples_r,orientation="h",hover_name="states",height=800,width=1000)
        st.plotly_chart(fig_tcount2)

#streamlit part
st.set_page_config(layout='wide')
st.title(":violet[PHONEPE DATA VISULAIZATION AND EXPLORATION]")

with st.sidebar:
    select=option_menu("MENU",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select=="HOME":
    st.image("D:\capstone\phonepe.jpg",width=400)
    st.markdown("# :violet[Data Visualization and Exploration]")
    
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
    with col2:
        st.image("D:\capstone\phonepe2.jpg",width=500)
elif select=="DATA EXPLORATION":
    t1,t2,t3=st.tabs(["AGGREGATED ANALYSIS","MAP ANALYSIS","TOP ANALYSIS"])
    with t1:
        method=st.radio("select one method",["Transaction","user","Insurance"])
        if method=="Transaction":
            c1,c2=st.columns(2)
            with c1:
                years=st.slider("Select year",agg_trans["years"].min(),agg_trans["years"].max(),agg_trans["years"].min())
            agg_trans_tac_y=transaction_count_amount_y(agg_trans,years)

            c1,c2=st.columns(2)
            with c1:
                states=st.selectbox("SELECT ANY STATE", agg_trans_tac_y["states"].unique())
            agg_trans_trans_type(agg_trans_tac_y,states)

            c1,c2=st.columns(2)
            with c1:
                quarters=st.slider("Select Quarter",agg_trans_tac_y["quarter"].min(),agg_trans_tac_y["quarter"].max(),agg_trans_tac_y["quarter"].min())
            agg_trans_tac_y_Q=transaction_count_amount_y_Q(agg_trans_tac_y,quarters)

            c1,c2=st.columns(2)
            with c1:
                states=st.selectbox("SELECT STATE", agg_trans_tac_y_Q["states"].unique())
            agg_trans_trans_type(agg_trans_tac_y_Q,states)


            
        elif method=="user":
            c1,c2=st.columns(2)
            with c1:
                years=st.slider("Select year",agg_user["years"].min(),agg_user["years"].max(),agg_user["years"].min())
            agg_user_Y=agg_user_plot1(agg_user,years)

            
            c1,c2=st.columns(2)
            with c1:
                quarters=st.slider("Select Quarter",agg_user_Y["quarter"].min(),agg_user_Y["quarter"].max(),agg_user_Y["quarter"].min())
            agg_user_tac_y_Q=agg_user_plot2(agg_user_Y,quarters)
            
            c1,c2=st.columns(2)
            with c1:
                states=st.selectbox("SELECT STATE", agg_user_tac_y_Q["states"].unique())
            agg_user_plot3(agg_user_tac_y_Q,states)



        elif method=="Insurance":
            c1,c2=st.columns(2)
            with c1:
                years=st.slider("Select year",agg_ins["years"].min(),agg_ins["years"].max(),agg_ins["years"].min())
            tac_y=transaction_count_amount_y(agg_ins,years)

            c1,c2=st.columns(2)
            with c1:
                quarters=st.slider("Select year",tac_y["quarter"].min(),tac_y["quarter"].max(),tac_y["quarter"].min())
            transaction_count_amount_y_Q(tac_y,quarters)
            
            
    with t2:
        method=st.radio("select one method",["Map Transaction","Map user","Map Insurance"])
        if method=="Map Transaction":
            c1,c2=st.columns(2)
            with c1:
                years=st.slider("Select the year",map_trans["years"].min(),map_trans["years"].max(),map_trans["years"].min())
            map_trans_tac_y=transaction_count_amount_y(map_trans,years)

            c1,c2=st.columns(2)
            with c1:
                states=st.selectbox("SELECT STATE FOR MAP_INSURANCE",map_trans_tac_y["states"].unique())
            map_ins_dist(map_trans_tac_y,states)

            c1,c2=st.columns(2)
            with c1:
                quarters=st.slider("Select the Quarter",map_trans_tac_y["quarter"].min(),map_trans_tac_y["quarter"].max(),map_trans_tac_y["quarter"].min())
            map_trans_tac_y_Q=transaction_count_amount_y_Q(map_trans_tac_y,quarters)

            c1,c2=st.columns(2)
            with c1:
                states=st.selectbox("SELECT STATE MAP_INSURANCE FOR QUARTER BASED",map_trans_tac_y_Q["states"].unique())
            map_ins_dist(map_trans_tac_y_Q,states)
            
        elif method=="Map user":
            c1,c2=st.columns(2)
            with c1:
                years=st.slider("Select year for map_users",map_user["years"].min(),map_user["years"].max(),map_user["years"].min())
            map_user_Y=map_user_plot1(map_user,years)

            c1,c2=st.columns(2)
            with c1:
                quarters=st.slider("Select the Quarter",map_user_Y["quarter"].min(),map_user_Y["quarter"].max(),map_user_Y["quarter"].min())
            map_user_Y_Q=map_user_plot2(map_user_Y,quarters)

            c1,c2=st.columns(2)
            with c1:
                states=st.selectbox("SELECT STATE FOR MAP_USER",map_user_Y_Q["states"].unique())
            map_user_plot3(map_user_Y_Q,states)

            
        elif method=="Map Insurance":
            c1,c2=st.columns(2)
            with c1:
                years=st.slider("Select year",map_ins["years"].min(),map_ins["years"].max(),map_ins["years"].min())
            map_ins_tac_y=transaction_count_amount_y(map_ins,years)

            c1,c2=st.columns(2)
            with c1:
                states=st.selectbox("SELECT STATE FOR MAP_INSURANCE",map_ins_tac_y["states"].unique())
            map_ins_dist(map_ins_tac_y,states)

            c1,c2=st.columns(2)
            with c1:
                quarters=st.slider("Select Quarter for map_insurance year based",map_ins_tac_y["quarter"].min(),map_ins_tac_y["quarter"].max(),map_ins_tac_y["quarter"].min())
            map_ins_tac_y_Q=transaction_count_amount_y_Q(map_ins_tac_y,quarters)

            c1,c2=st.columns(2)
            with c1:
                states=st.selectbox("SELECT STATE MAP_INSURANCE FOR QUARTER BASED",map_ins_tac_y_Q["states"].unique())
            map_ins_dist(map_ins_tac_y_Q,states)


    
    with t3:
        method=st.radio("select one method",["Top Transaction","Top user","Top Insurance"])
        if method=="Top Transaction":
            c1,c2=st.columns(2)
            with c1:
                years=st.slider("Select particular year for top transaction",top_trans["years"].min(),top_trans["years"].max(),top_trans["years"].min())
            tTac_y=transaction_count_amount_y(top_trans,2021)

            c1,c2=st.columns(2)
            with c1:
                states=st.selectbox("SELECT STATE FOR TOP_INSURANCE",tTac_y["states"].unique())
            top_insurance_plot1(tTac_y,states)
            c1,c2=st.columns(2)
            with c1:
                quarters=st.slider("Select Quarter for top_transaction quarter based",tTac_y["quarter"].min(),tTac_y["quarter"].max(),tTac_y["quarter"].min())
            ttac_y_Q=transaction_count_amount_y_Q(tTac_y,quarters)

            
        elif method=="Top user":
            c1,c2=st.columns(2)
            with c1:
                years=st.slider("Select particular year for top user",top_user["years"].min(),top_user["years"].max(),top_user["years"].min())
            tuser_y=top_user_plot1(top_user,years)

            c1,c2=st.columns(2)
            with c1:
                states=st.selectbox("SELECT STATE FOR Top_user",tuser_y["states"].unique())
            top_user_plot2(tuser_y,states)

        elif method=="Top Insurance":
            c1,c2=st.columns(2)
            with c1:
                years=st.slider("Select particular year for top insurance",top_ins["years"].min(),top_ins["years"].max(),top_ins["years"].min())
            ttac_y=transaction_count_amount_y(top_ins,years)

            c1,c2=st.columns(2)
            with c1:
                states=st.selectbox("SELECT STATE FOR TOP_INSURANCE",ttac_y["states"].unique())
            top_insurance_plot1(ttac_y,states)

            c1,c2=st.columns(2)
            with c1:
                quarters=st.slider("Select the Quarter for top_insurance",ttac_y["quarter"].min(),ttac_y["quarter"].max(),ttac_y["quarter"].min())
            ttac_y_Q=transaction_count_amount_y_Q(ttac_y,quarters)
            
            
elif select=="TOP CHARTS":
    QUESTION=st.selectbox("Select the question",["1.TRANSACTION AMOUNT AND COUNT OF AGGREGATED INSURANCE",
                                                    "2.TRANSACTION AMOUNT AND COUNT OF MAP INSURANCE",
                                                    "3.TRANSACTION AMOUNT AND COUNT OF TOP INSURANCE",
                                                    "4.TRANSACTION AMOUNT AND COUNT OF AGGREGATED TRANSACTION",
                                                    "5.TRANSACTION AMOUNT AND COUNT OF MAP TRANSACTION",
                                                    "6.TRANSACTION AMOUNT AND COUNT OF TOP TRANSACTION",
                                                    "7.TRANSACTION COUNT OF AGGREGATED USER",
                                                    "8.REGISTERED USERS OF MAP USER",
                                                    "9.APP OPENS OF MAP USER",
                                                    "10.REGISTERED USERS OF TOP USER"])

    if QUESTION=="1.TRANSACTION AMOUNT AND COUNT OF AGGREGATED INSURANCE":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_tamount("aggregate_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_tcount("aggregate_insurance")

    elif QUESTION=="2.TRANSACTION AMOUNT AND COUNT OF MAP INSURANCE":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_tamount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_tcount("map_insurance")

    elif QUESTION=="3.TRANSACTION AMOUNT AND COUNT OF TOP INSURANCE":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_tamount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_tcount("top_insurance")

    elif QUESTION=="4.TRANSACTION AMOUNT AND COUNT OF AGGREGATED TRANSACTION":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_tamount("aggregate_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_tcount("aggregate_transaction")

    elif QUESTION=="5.TRANSACTION AMOUNT AND COUNT OF MAP TRANSACTION":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_tamount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_tcount("map_transaction")

    elif QUESTION=="6.TRANSACTION AMOUNT AND COUNT OF TOP TRANSACTION":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_tamount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_tcount("top_transaction")

    elif QUESTION=="7.TRANSACTION COUNT OF AGGREGATED USER":
        st.subheader("TRANSACTION COUNT")
        top_chart_tcount("aggregate_user")

    elif QUESTION=="8.REGISTERED USERS OF MAP USER":
        states=st.selectbox("select state",map_user["states"].unique())
        st.subheader("REGISTERED USERS")
        top_chart_reguser("map_user",states)

    elif QUESTION=="9.APP OPENS OF MAP USER":
        states=st.selectbox("select state",map_user["states"].unique())
        st.subheader("APP OPENS")
        top_chart_appopens("map_user",states)
    
    elif QUESTION=="10.REGISTERED USERS OF TOP USER":
        st.subheader("RegisteredUsers")
        top_chart_reguser1("top_user")

    