"""
Reddit-Instagram Meme Bot 1.0
@author: alexrt-s
https://github.com/alexrt-s
####################################################
The purpose of this code is to make automated posts to instagram given a few parameters,
which can run indefinitely and thus make thousands of instagram posts without any ongoing 
human intervention.

The goal is a fully automated instagram account that will become self sustaining as it attrcts and 
retains new followers. in its current iteration, this has not been achieved
"""


import numpy as np
import os

import requests
from instabot import Bot

from PIL import Image
import PIL

import time as t

path = '/path/to/file/Meme Bot/config/your_username_here_uuid_and_cookie.json'
dummy_folder = '/path/to/file/Meme Bot/dummy_folder'

username='username'
password='password'

if os.path.isfile(path):
    os.remove(path)
    
    
def Caption_Bot(admin):
    '''
    A primitive method to give apparently unique captions to each post

    Parameters
    ----------
    admin : String
        A string that appears at the end of the caption. Can be an alias for the meme account admin running the bot on
        their machine.
    
    Returns
    -------
    None
   
    '''
    captions = ['list', 'of', 'strings', 'you', 'want', 'to', 'caption', 'your', 'posts', 'with' ]
    hashtags = '\n \n \n #hashtags #you #want #to #attach #to #your #posts'
    random = np.randomrandint(low=0,high=len(captions))
    return captions[random] + ' ' + admin + hashtags
    

def Fetch_Meme(subreddit,listing,limit,timeframe):
    '''
    Fetches urls of posts found on reddit that fulfill the criteria provided and returns them in a list

    Parameters
    ----------
    subreddit : String
        The subreddit you want to steal memes from.
    listing : String
        How you want to sort the memes from your chosen subreddit, choose from : top, controversial, best, hot, new, random, rising .
    limit : Integer
        How many memes you want to fetch from the sub. Only JPEG & PNG files will be used, so the number of memes posted will always be
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
    Sorts through a list of urls and downloads files from the list which have the correct file type, which here is .jpg or
    .png

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
        
        #elif meme.endswith('.gif'):
            #keep.append(meme)
        
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
    '''
    Changes the image that corresponds to the filename provided into a 1080x1080 aspect ratio so as to be compatible with instagram

    Parameters
    ----------
    name : String
        Filename of the image that needs to be resized

    Returns
    -------
    None.

    '''
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
    '''
    Posts all of the image files within the given folder to instagram

    Parameters
    ----------
    folder : String
        The location of a folder which contains the images that you want to post

    Returns
    -------
    None.

    '''
    files = os.listdir(folder)
    print(files)
    bot = Bot()
    bot.login(username=username,
              password=password)
    for name in files:
        try:
            bot.upload_photo(dummy_folder + '/' + name,caption=Caption_Bot('Admin'))
            os.remove(dummy_folder + '/' + name + '.REMOVE_ME')
        except:
            pass
'''
Example code that uses the above functions to post indefinitely on instagram.
'''
    

def main(subreddit,listing,limit,timeframe):
    Save_Meme(Fetch_Meme(subreddit=subreddit,listing=listing,limit=limit,timeframe=timeframe))
    for meme in os.listdir(dummy_folder):
        Edit_Image(dummy_folder + '/' + meme)
    Post(dummy_folder)


subreddits = ['okbuddychicanery','aww','shitposting','EyeBleach']

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
