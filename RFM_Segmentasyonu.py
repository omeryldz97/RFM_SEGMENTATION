#Task 1: Understanding and Preparing the Data
#Step 2: Read the dataset. Make a copy of the dataframe.
!pip install openpyxl
import pandas as pd
import datetime as dt
pd.set_option("display.max_columns",None)
pd.set_option("display.max_rows",None)
pd.set_option("display.float_format",lambda  x:"%.5f" %x)
df_=pd.read_csv("") #Note: The data set is private so cannot be shared.
df=df_.copy()

#Step2: In Dataset
#a. first 10 observations,
#b. variable names,
#c. descriptive statistics,
#d. null value,
#to. Variable types, review.

#a. first 10 observations,
df.head()
#b. variable names,
df.columns

#c. descriptive statistics,
df.describe().T

#d. null value,
df.isnull().sum()

#e.Variable types, review.
df.info()
#Step 3 :Create new variables for each customer's total purchases and spending.
df["customer_value_total"]=df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]
df["order_num_total"]=df["order_num_total_ever_offline"] + df["order_num_total_ever_online"]
df.head()

#Step 4: Examine the variable types. Change the type of variables that express date to date.
df.info()
my_date=["first_order_date","last_order_date","last_order_date_online","last_order_date_offline"]
df[my_date]=df[my_date].apply(pd.to_datetime)

#Step 5: Look at the distribution of the number of customers in the shopping channels, the total number of products purchased, and the total expenditures.
df.groupby("order_channel").agg({"master_id":"count","order_num_total":"sum","customer_value_total":"sum"})

#Step 6: Rank the top 10 customers with the highest revenue.
df.sort_values("customer_value_total",ascending=False).head(10)

#Step 7: List the top 10 customers with the most orders.
df.sort_values("order_num_total", ascending=False)[:10]

#Step 8: Streamline the data provisioning process

def data_prep(dataframe):
    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)
    return df

#Task 2: Calculating RFM Metrics

#Step 1: Make the definitions of Recency, Frequency and Monetary.
df["last_order_date"].max() # 2021-05-30
today_date=dt.datetime(2021,6,1)

#Step 2: Calculate the Recency, Frequency and Monetary metrics for the customer.
rfm=pd.DataFrame()
rfm["customer_id"]=df["master_id"]
rfm["recency"] = (today_date - df["last_order_date"]).astype('timedelta64[D]')
rfm["frequency"]=df["order_num_total"]
rfm["monetary"]=df["customer_value_total"]
rfm.head()

#Task 3: Calculating RF Score
#Step 1: Convert the Recency, Frequency and Monetary metrics to scores between 1-5 with the help of qcut.
#Step 2: Record these scores as recency score, frequency score and monetary score.
rfm["recency_score"]=pd.qcut(rfm["recency"],5,labels=[5,4,3,2,1])
rfm["monetary_score"]=pd.qcut(rfm["monetary"],5,labels=[1,2,3,4,5])
rfm["frequency_score"]=pd.qcut(rfm["frequency"].rank(method="first"),5,labels=[5,4,3,2,1])
rfm.head()
#Step 3: Express recency_score and frequency_score as a single variable and save it as RF_SCORE.
rfm["RF_SCORE"]=(rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str))

#Task 4: Segment Definition of RF Score
#Step 1: Make segment definitions for the generated RF scores.
#Step 2: Convert the scores into segments with the help of the seg_map below.
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}
rfm["segment"]=rfm["RF_SCORE"].replace(seg_map,regex=True)
rfm.head()


