from google import genai
import os
from dotenv import load_dotenv
import time
from supabase import create_client, Client
import requests
import tempfile

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

def wait_video_upload(client, uploaded_file):
    while True:
        file_info = client.files.get(name=uploaded_file.name)
        print(f"   Current state: {file_info.state}")
        if file_info.state == "ACTIVE":
            print(f"File is ACTIVE, ready to use.")
            break
        elif file_info.state == "FAILED":
            raise RuntimeError("File processing failed.")
        time.sleep(2)


def main():
    
    bucket_name = "videos"
    response = (
        supabase.storage
        .from_("videos")
        .list()
    )

    client = genai.Client(api_key=api_key)

    for video in response:
        vid_name = video['name']
        vid_url = f"{url}/storage/v1/object/public/{bucket_name}/{vid_name}"

        r = requests.get(vid_url)
        r.raise_for_status()

        # Write to temp file
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
            tmp_file.write(r.content)
            tmp_file_path = tmp_file.name

        try:

            uploaded_file = client.files.upload(file=tmp_file_path)

            wait_video_upload(client, uploaded_file)

            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=["You are a content moderator of a social media platform. Generate a score from 0-1 to 2 d.p., of how much you would want this content on your platform. Reduce score for AI-generated videos, and prioritise human-made content, including edits. Return just the score.", uploaded_file]
            )
            score = response.text

            if score is not None:

                # Update DB for the matching video_id
                update_resp = supabase.table("videos").update(
                    {"sentiment": score}
                ).eq("video_id", vid_name[:-4]).execute()

                print(f"Updated sentiment for video_id={vid_name[:-4]}")

            else:
                print("Could not extract score from Gemini response.")

        except Exception as e:
            print(f"Error processing vid_name: {e}")

        finally:
                os.remove(tmp_file_path)  # clean up temp file

        

if __name__ == "__main__":
    main()