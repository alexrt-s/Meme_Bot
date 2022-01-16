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
        meme_url = request.json()['data']['children'][i]['data']['url']
        memes.append(meme_url)
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
        filename = url.replace('/','') + '.jpg'
        with open(dummy_folder + '/' + filename,'wb') as f:
            f.write(img_data)
    
            
def Post(folder):
    files = os.listdir(folder)
    print(files)
    bot = Bot()
    bot.login(username=username,
              password=password)
    for name in files:
        try:
            bot.upload_photo(name,caption='your mom')
        except:
            pass
    
    
    

def main(subreddit,listing,limit,timeframe):
    memes = Fetch_Meme(subreddit=subreddit,listing=listing,limit=limit,timeframe=timeframe)
    keep = Save_Meme(memes)
    Post(dummy_folder)



main('memes','top',100,'day')
