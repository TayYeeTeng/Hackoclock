import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

# Fetch relevant columns where sentiment is not null
response = supabase.table("videos")\
    .select("*")\
    .filter("sentiment","not.is", None)\
    .execute()

rows = response.data

for row in rows:
    row["engagement_rate"] = (
        (row.get("likes_per_view") or 0) +
        (row.get("shares_per_view") or 0) +
        (row.get("bookmarks_per_view") or 0) +
        (row.get("comments_per_view") or 0)
    )

for row in rows:
    supabase.table("videos")\
        .update({"engagement_rate": row["engagement_rate"]})\
        .eq("id", row["id"])\
        .execute()
