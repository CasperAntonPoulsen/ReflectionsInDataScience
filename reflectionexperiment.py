import random
import praw
import json
import pandas as pd
import time
import numpy as np
import datetime
import sys

class ReflectionExperimentReddit:
    def __init__(self, savedPostsFilename, postLimit, clientId, clientSecret, userAgent, username, password):
        
        # Expected fileformat is a newline seperated json
        self.savedPostsFilename = savedPostsFilename

        # amount of mew posts fetched from reddit
        self.postLimit = postLimit

        # Reddit API credentials
        self.reddit = praw.Reddit(
            client_id=clientId,
            client_secret=clientSecret,
            user_agent=userAgent,
            username=username, 
            password=password
        )

    def isEligiblePost(self, post):
        # Check the attributes of a post

        # Reddit posts start with one upvote from the original poster
        noVotes = post.score == 1
        noComments = post.num_comments == 0

        # If both conditions are met, return True, else False
        if noVotes and noComments:
            return True
        else:
            return False
    
    def likePost(self, post):

        # Reddit api has a theoretical limit of one interaction per second
        time.sleep(1)
        post.upvote()

    def createPostData(self, id, isExperimental):
        # Struct containing the relevant data from the post.
        # datetime is actually a timestamp, as datetime is not json seriallizable 

        postData = {
            "id":id,
            "nVotes": 1,
            "nComments": 0 ,
            "isExperimental": isExperimental,
            "datetime": time.time()
        }
        return postData

    def savePost(self, postData):
        # Saves posts to the file

        with open(self.savedPostsFilename, "a", encoding="utf-8") as file:
            file.write(json.dumps(postData)+ "\n")

    def findNewPosts(self):

        # Reddit has an api call to get any number of new posts made on reddit
        # Setting a limit is advisable, as this function is evaluated to be i api call for each batch of 100 posts
        for post in self.reddit.subreddit("all").new(limit=self.postLimit):

            if self.isEligiblePost(post):
                
                isExperimental = bool(random.randint(0,1))

                if isExperimental:

                    # Bad way to handle not being able to like, but it will be caught in the logs
                    try:
                        self.likePost(post)
                    except Exception as e:
                        sys.stdout.write(str(e))
                        continue


                self.savePost(self.createPostData(post.id, isExperimental))

    def loadSavedPosts(self):
        return pd.read_json("postData.json", lines=True)
        
    def checkPost(self, oldPostData):
        time.sleep(1)
        post = self.reddit.submission(id=oldPostData["id"])

        nComments = post.num_comments
        nVotes = post.score

        postData = {
            "id": oldPostData["id"],
            "nVotes": nVotes,
            "nComments": nComments,
            "isExperimental": oldPostData["isExperimental"],
            "datetime": time.time()
        }

        return postData

    def olderThan24Hours(self, dateTime):
        return (datetime.datetime.now() - dateTime) > datetime.timedelta(days=1)

    def checkSavedPosts(self):
        df = self.loadSavedPosts()
        if df.empty: 
            return
        
        gb = df.groupby(["id","isExperimental"])
        _df = gb.agg({"datetime":np.max})

        for idx, post in _df.reset_index().iterrows():

            if self.olderThan24Hours(post[2]):
                
                self.savePost(self.checkPost({"id":post[0], "isExperimental":post[1]}))
