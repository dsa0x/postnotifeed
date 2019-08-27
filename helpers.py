from instaloader import Instaloader, Profile
import requests
import re
L = Instaloader()

PROFILE = 'drealdsa'
typer = 'is_video'


def getposts(username,kind):
    url = 'https://www.instagram.com/{}'.format(username)
    r = requests.get(url.format(username))
    html = r.text
    if r.ok:
        posts = []
        profile = Profile.from_username(L.context, username)
        for post in profile.get_posts():
            posts.append(post.shortcode)
            if post.is_video:
                link = 'New Video Post: ' + 'https://www.instagram.com/' + posts[0] +'/'
                shorty = 'https://www.instagram.com/' + posts[0] + '/'
                types = 'video'
            else:
                link = 'New Image Post: ' + 'https://www.instagram.com/' + posts[0] +'/'
                shorty = 'https://www.instagram.com/' + posts[0] + '/'
                types = 'picture'
            linkdict = {
                'link':link,
                'shorty':shorty,
                'type': types
            }
        return linkdict
    else:
        return 'Username not found'


def checkUsername(username):
    url = 'https://www.instagram.com/{}'.format(username)
    r = requests.get(url.format(username))
    html = r.text
    if r.ok:
        return re.findall('"username":"(.*?)",', html)[0]
    else:
        return "invalid_username"
