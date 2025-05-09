import streamlit as st
import requests

# Constants
API_URL = "http://127.0.0.1:8000"

st.title("📸 Instagram Explorer")

# Sidebar navigation
view = st.sidebar.selectbox("Select View", ["Profile", "Followers", "Following", "Posts"])

if view == "Profile":
    st.header("Profile Viewer")
    user = st.text_input("Enter Instagram username (leave blank for your own):")
    if st.button("Load Profile"):
        params = {"user": user} if user else {}
        try:
            resp = requests.get(f"{API_URL}/profile", params=params)
            resp.raise_for_status()
            data = resp.json()
            if data.get("profile_pic_url"):
                st.image(data["profile_pic_url"], width=150)
            st.write(f"**Username:** {data.get('username', 'N/A')}")
            st.write(f"**Name:** {data.get('full_name', 'N/A')}")
            st.write(f"**Followers:** {data.get('followers', 'N/A')}")
            st.write(f"**Following:** {data.get('following', 'N/A')}")
            st.write(f"**Bio:** {data.get('biography', '')}")
        except requests.exceptions.ConnectionError:
            st.error("Cannot reach backend — ensure the FastAPI server is running on port 8000.")
        except requests.exceptions.HTTPError as e:
            st.error(f"HTTP error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

elif view == "Followers":
    st.header("Followers List")
    user = st.text_input("Enter Instagram username (leave blank for your own):")
    if st.button("Load Followers"):
        params = {"user": user} if user else {}
        try:
            resp = requests.get(f"{API_URL}/followers", params=params)
            resp.raise_for_status()
            st.json(resp.json())
        except Exception as e:
            st.error(f"Error: {e}")

elif view == "Following":
    st.header("Following List")
    user = st.text_input("Enter Instagram username (leave blank for your own):")
    if st.button("Load Following"):
        params = {"user": user} if user else {}
        try:
            resp = requests.get(f"{API_URL}/following", params=params)
            resp.raise_for_status()
            st.json(resp.json())
        except Exception as e:
            st.error(f"Error: {e}")

elif view == "Posts":
    st.header("Recent Posts")
    user = st.text_input("Enter Instagram username (leave blank for your own):")
    count = st.number_input("Number of posts to fetch", min_value=1, max_value=50, value=10)
    if st.button("Load Posts"):
        params = {"user": user, "count": count} if user else {"count": count}
        try:
            resp = requests.get(f"{API_URL}/posts", params=params)
            resp.raise_for_status()
            st.json(resp.json())
        except Exception as e:
            st.error(f"Error: {e}")