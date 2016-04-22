import tweepy

def download_timelines(fid, api_key, api_secret, access_key, access_secret):
    """
    Utility method for downloading the raw timelines of all the users
    specified by the original call.
    """
    # OAuth setup.
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

    # Retrieve all the tweets we can.
    count = 0
    page = 1
    statuses = []
    s = api.user_timeline(fid, count = 200, page = page)
    while len(s) > 0:
        for i in s:
            status = {'status_id': i.id_str,
                    'coords': i.coordinates,
                    'created_at': i.created_at.strftime("%Y-%m-%d %H:%I:%S"),
                    'rt_count': i.retweet_count,
                    'text': i.text,
                    'fave_count': i.favorite_count}
            statuses.append(status)
        count += len(s)
        page += 1
        s = api.user_timeline(fid, count = 200, page = page)

    # Set up the output dictionary.
    user = api.get_user(fid)
    out_dict = {'username': user.screen_name,
                'id_str': user.id_str,
                'created_at': user.created_at.strftime("%Y-%m-%d %H:%I:%S"),
                'profile': user.description,
                'followers': user.followers_count,
                'friends': user.friends_count,
                'name': user.name,
                'statuses_count': user.statuses_count,
                'statuses': statuses}

    # All done!
    return [fid, out_dict]
