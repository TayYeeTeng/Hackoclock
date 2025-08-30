import os
from dotenv import load_dotenv
import time
from supabase import create_client, Client
import requests
import tempfile
import pandas as pd

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

#get data from supabase
# Get all rows from 'users' table
response = supabase.table("videos")\
    .select("*")\
    .filter("sentiment","not.is", "null")\
    .execute()

# The data is in response.data
data = response.data

df = pd.DataFrame(data)
#Columns we want to normalize
cols = ["views","likes","shares","comments","bookmarks","engagement_rate","sentiment"]

#Z-score normalisation (x-mean)/std
for col in cols:
    mean = df[col].mean()
    std = df[col].std(ddof=0)
    df[col+"_z"] = (df[col]-mean) / std if std > 0 else 0

# Get all the new Z-score column names
z_cols = [col+"_z" for col in cols]

# Sum across the Z-score columns row-wise
df["video_points"] = df[z_cols].sum(axis=1)

print(df["video_points"]) #for checking

#for _, row in df.iterrows():
#    supabase.table("videos")\
#        .update({"video_points": float(row["video_points"])})\
#        .eq("video_id", row["video_id"])\
#        .execute()


