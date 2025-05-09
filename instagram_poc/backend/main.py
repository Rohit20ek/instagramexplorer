import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from instagrapi import Client, exceptions

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

USERNAME = os.getenv('IG_USERNAME')
PASSWORD = os.getenv('IG_PASSWORD')

# Initialize Instagram client and login once
db_session_file = os.path.join(os.path.dirname(__file__), 'session.json')
cl = Client()
if os.path.exists(db_session_file):
    cl.load_settings(db_session_file)
try:
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings(db_session_file)
except exceptions.ClientError as e:
    raise RuntimeError(f"Instagram login failed: {e}")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get("/profile")
def get_profile(user: str = Query(None, description="Instagram username to fetch; leave empty for your own")):
    """
    Fetch profile information for the given username, or your own if none provided.
    """
    try:
        if user:
            profile = cl.user_info_by_username(user)
        else:
            profile = cl.account_info()
    except exceptions.ClientError as e:
        raise HTTPException(status_code=404, detail=str(e))

    # Determine whether profile is dict or instagrapi User object
    if isinstance(profile, dict):
        data = profile
    else:
        # instagrapi User object has attribute .dict() returning full dict
        data = profile.model_dump()

    # Extract profile data
    return {
        'username': data.get('username'),
        'full_name': data.get('full_name'),
        'followers': data.get('follower_count') or data.get('followers_count'),
        'following': data.get('following_count') or data.get('following'),
        'biography': data.get('biography'),
        'profile_pic_url': data.get('profile_pic_url')
    }



## 5. Extended Backend Features

# To enable scraping followers, following, and post likes in the POC, extend `backend/main.py` with these new endpoints:

### 5.1 Followers and Following Endpoints
# python
from fastapi import HTTPException

@app.get('/followers')
def get_followers(user: str = None, count: int = 100):
    target = user or USERNAME
    try:
        user_pk = cl.user_id_from_username(target)
        followers_map = cl.user_followers(user_pk, amount=count)
        return {'followers': [u.username for u in followers_map.values()]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/health")
def health():
    me = cl.account_info()
    return {
        "logged_in_as": me.username,
        "my_followers": getattr(me, "follower_count", None) or getattr(me, "followers_count", None)
    }

@app.get('/following')
def get_following(user: str = None, count: int = 100):
    """
    Fetch up to `count` usernames that this account is following.
    """
    target = user or USERNAME
    try:
        user_pk = cl.user_id_from_username(target)
        # Fetch up to `count` followings
        following_map = cl.user_following(user_pk, amount=count)
        return {'following': [u.username for u in following_map.values()]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get('/posts')
def get_posts(user: str = None, count: int = 10):
    """
    Fetch up to `count` most recent media and return simple stats:
    - id, caption (first 100 chars), like_count, timestamp.
    """
    target = user or USERNAME
    try:
        user_pk = cl.user_id_from_username(target)  # Convert username to user ID
        medias = cl.user_medias(user_pk, amount=count)  # Use user ID here
        posts = []
        for m in medias:
            posts.append({
                'id': m.pk,
                'caption': (m.caption_text or '')[:100],
                'like_count': m.like_count,
                'taken_at': m.taken_at.isoformat()
            })
        return {'posts': posts}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

