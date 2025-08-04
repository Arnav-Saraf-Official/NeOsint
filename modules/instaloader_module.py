import instaloader

def run(user_data):
    L = instaloader.Instaloader()
    try:
        print(f"[+] Searching Instagram for: {user_data['name']}")
        profile = instaloader.Profile.from_username(L.context, user_data["name"])
        for post in profile.get_posts():
            L.download_post(post, target=profile.username)
    except Exception as e:
        print(f"[!] Instagram search failed: {e}")
