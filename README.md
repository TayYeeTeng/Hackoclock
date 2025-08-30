# Hackoclock
For TechJam 2025

Process for rewarding points to content creators

# 1. Top 1000 Trending Videos Tik Tok dataset
- Made use of a dataset containing fields such as creator's id, createTime, webVideoUrl, diggCount (number of likes), shareCount, commentCount etc.
- From the dataset, we came up with our main tables -- creators and videos

# 2. Creators Table Documentation
- creator_id: unique id of each TikTok content creator
- follower_count: No. of followers for that TikTok creator (Type: int)
- video_count: No. of total videos the creator has made
- total_points: Calculated column which sums the total points earned by the creator

# 3. Videos Table Documentation
- creator_id acts as the foreign key in Videos table 
- video_id: unique id of each TikTok video posted
- url: text string showing the link of the TikTok video (webpage)
- views, likes, shares, bookmarks, comments: Count of fields on that TikTok video
- engagement_rate: sum of likes_per_view, shares_per_view, bookmarks_per_view, comments_per_view
- likes_per_view: No. of Likes / No. of Views
- shares_per_view, bookmarks_per_view, comments_per_view: same as above but with their respective values
- date_posted: Date when the TikTok video was created and posted
- video_points: Calculated column which classifies a few variables for content creators to earn points
- sentiment: Using genai api, it helps to assign a score 0 to 1 (0 negative 1 positive) by analysing the video content through the storage buckets with the downloaded TikTok videos. 

# 4. Calculations of points
- Using Z-score and scaling, the video_points is calculated by summing the z-scores of 7 fields: views, likes, shares, bookmarks, engagement_rate, comments & sentiment
- The points are then scaled to match the shop table requirements connected to the main webpage UI, encouraging content creators to make videos of better quality and of appropriate content.

# 5. Shop Table Documentation
- There are a few fixed rewards for creators to redeem with the points they earned from their videos.
- reward_id: unique id for each type of reward
- amount: indicates the amount of points needed
- exposure: description of what reward is given

# 6. Redemption Table Documentation
- This table is a backend table that acts to store logs, i.e. what was redeemed, by which creator, and the time of redemtion
- From then, points will also be deducted from the creator's total points once the redemption has been successfully received.


