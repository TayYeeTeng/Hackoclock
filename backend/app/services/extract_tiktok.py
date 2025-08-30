from TikTokApi import TikTokApi
import asyncio
import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client
import datetime
import requests

load_dotenv()

# Create supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

# Initialize API
api = TikTokApi()

ms_token = os.environ.get(
    "ms_token", None
) 

with open('../../data/trending.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

videos = data['collector']

async def get_videos(videos):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False, browser="chromium")
        for vid in videos:
            url = vid['webVideoUrl']
            try: 
                video = api.video(
                    url=url
                )

                # Fetch stats
                video_info = await video.info()  # is HTML request, so avoid using this too much
                stats = video_info['stats']

                # Calculations
                views = int(stats['playCount'])
                likes_per_view = round(int(stats['diggCount']) / views, 5)
                comments_per_view = round(int(stats['commentCount']) / views, 5)
                shares_per_view = round(int(stats['shareCount']) / views, 5)
                bookmarks_per_view = round(int(stats['collectCount']) / views, 5)

                # Transform time
                timestamp = int(video_info["createTime"])

                # Convert to datetime
                dt = datetime.datetime.fromtimestamp(timestamp)
                date = dt.strftime("%Y-%m-%d")

                # Create insertions
                new_creator = {
                    'creator_id': video_info['author']['id'],
                    'follower_count': video_info['authorStats']['followerCount'],
                    'video_count': video_info['authorStats']['videoCount']
                }

                new_video = {
                    'video_id': video_info['id'],
                    'creator_id': video_info['author']['id'],
                    'url': url,
                    'views': stats['playCount'],
                    'likes': stats['diggCount'],
                    'comments': stats['commentCount'],
                    'shares': stats['shareCount'],
                    'bookmarks': stats['collectCount'],
                    'likes_per_view': likes_per_view,
                    'comments_per_view': comments_per_view,
                    'shares_per_view': shares_per_view,
                    'bookmarks_per_view': bookmarks_per_view,
                    'date_posted': date
                }

                # Insert into DB
                try:
                    creator_response = (
                        supabase.table("creators")
                        .upsert(new_creator, on_conflict="creator_id")
                        .execute()
                    )
                except Exception as e:
                    print(f"Failed to insert creator: {e}")

                try:
                    video_response = (
                    supabase.table("videos")
                    .upsert(new_video, on_conflict="video_id")
                    .execute()
                    )
                    if video_response:
                        print(f"Inserted {url} successfully")

                except Exception as e:
                    print(f"Failed to insert video:{e}")

                try:
                    # Insert into storage bucket

                    headers = {
                        "User-Agent": (
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/114.0.0.0 Safari/537.36"
                        ),
                        "Referer": "https://www.tiktok.com/",
                    }

                    # Pick best available video URL
                    downloadable_url = None

                    if "downloadAddr" in video_info and video_info["downloadAddr"]:
                        downloadable_url = video_info["downloadAddr"]
                    elif "video" in video_info and "downloadAddr" in video_info["video"]:
                        downloadable_url = video_info["video"]["downloadAddr"]
                    elif "video" in video_info and "bitrateInfo" in video_info["video"]:
                        # pick highest quality
                        bitrate_variants = video_info["video"]["bitrateInfo"]
                        if bitrate_variants:
                            downloadable_url = bitrate_variants[0]["PlayAddr"]["UrlList"][0]

                    if not downloadable_url:
                        print(f"No downloadable URL found for video {url}")
                        continue

                    response = requests.get(downloadable_url, headers=headers)
                    if response.status_code == 200:
                        video_bytes = response.content

                        video_bytes = response.content

                        bucket_name = "videos" 
                        storage_path = f"{video_info['id']}.mp4"

                        upload_response = supabase.storage.from_(bucket_name).upload(storage_path, video_bytes, {'content_type':"video/mp4"})

                        if upload_response:
                            print("Video uploaded successfully!")

                        else:
                            print("Failed to upload video.")

                    else:
                        print(f"Failed to fetch video {url}: {response.status_code}")
                    
                        
                except Exception as e:
                    print(f"Failed to upload video: {e}")


            except Exception as e:
                print(f"Error fetching {url}: {e}")
                print("Skipping to next video...\n")
                continue


if __name__ == "__main__":
    asyncio.run(get_videos(videos))