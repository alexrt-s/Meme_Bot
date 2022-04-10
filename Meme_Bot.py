"""
Reddit Meme Bot
@author: alexrt-s
https://github.com/alexrt-s
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy
import time

import os
import glob

import requests
from instabot import Bot

from PIL import Image
import PIL

import time as t

path = '/Users/alexthomson-strong/Desktop/Undergraduate Physics/Junior Honours/Meme Bot/config/your_mom_is_a_ho_chi_minh_uuid_and_cookie.json'
dummy_folder = '/Users/alexthomson-strong/Desktop/Undergraduate Physics/Junior Honours/Meme Bot/dummy_folder'

username='your_mom_is_a_ho_chi_minh'
password='PoopSock123'

if os.path.isfile(path):
    os.remove(path)

def Fetch_Meme(subreddit,listing,limit,timeframe):
    '''
    

    Parameters
    ----------
    subreddit : String
        The subreddit you want to steal memes from.
    listing : String
        How you want to sort the memes from your chosen subreddit, choose from : top, controversial, best, hot, new, random, rising .
    limit : Integer
        How many memes you want to fetch from the sub. Non JPEG & PNG files will not be used, so the number of memes posted will always be
        less than the limit
    timeframe : String
        The timeframe that you want the memes to come from, choose from: hour, day, week, month, year, all.

    Returns
    -------
    memes : List
        A list of url's for the reddit posts.

    '''
    memes = []
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
    except:
        print('An Error Occured')
    for i in range(0,limit):
        try:
            meme_url = request.json()['data']['children'][i]['data']['url']
            memes.append(meme_url)
        except:
            pass
    return memes
        
def Save_Meme(memes):
    '''
    

    Parameters
    ----------
    memes : List
        A list of url's for the reddit posts.

    Returns
    -------
    None.

    '''
    keep = []
    filenames = []
    for meme in memes:
        if meme.endswith('.jpg'):
            keep.append(meme)
        elif meme.endswith('.png'):
            keep.append(meme)
        '''
        elif meme.endswith('.gif'):
            keep.append(meme)
        '''
    else:
        pass
    if os.path.exists(dummy_folder) is False: 
        os.mkdir(dummy_folder)
    else:
        pass
    for url in keep:
        img_data = requests.get(url).content
        filename = url.replace('/','') + '.jpeg'
        with open(dummy_folder + '/' + filename,'wb') as f:
            f.write(img_data)


def Edit_Image(name):
    try:
        im = Image.open(name)
        newsize = (1080,1080)
        im1 = im.resize(newsize)
        im1 = im1.convert("RGB")
        os.remove(name)
        im1.save(name)
    except:
        pass

            
def Post(folder):
    files = os.listdir(folder)
    print(files)
    bot = Bot()
    bot.login(username=username,
              password=password)
    for name in files:
        try:
            bot.upload_photo(dummy_folder + '/' + name,caption='What the fuck am I doing with my life? X')
            os.remove(dummy_folder + '/' + name + '.REMOVE_ME')
        except:
            pass
    #os.empty_directory
    
    
    

def main(subreddit,listing,limit,timeframe):
    Save_Meme(Fetch_Meme(subreddit=subreddit,listing=listing,limit=limit,timeframe=timeframe))
    for meme in os.listdir(dummy_folder):
        Edit_Image(dummy_folder + '/' + meme)
    Post(dummy_folder)


subreddits = ['communistmemes','aww','shitposting','EyeBleach']

while True:
    start = t.time()
    for sub in subreddits:
        if os.path.isfile(path):
            os.remove(path)
        main(sub,'top',10000,'hour')
    end = t.time()
    diff = end - start
    if diff >= 3600:
        pass
    else:
        t.sleep(3600 - diff)
