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
response = supabase.table("videos").select("*").execute()

# The data is in response.data
data = response.data

df = pd.DataFrame(data)
#Columns we want to normalize
cols = ["views","likes","shares","comments","bookmarks","engagement_rate"]
