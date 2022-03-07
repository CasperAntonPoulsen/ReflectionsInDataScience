import os
from reflectionexperiment import ReflectionExperimentReddit

def main():

    r = ReflectionExperimentReddit(
            "postData.json",
            int(os.environ.get("POSTLIMIT")),
            os.environ.get("CLIENT_ID"),
            os.environ.get("CLIENT_SECRET"),
            os.environ.get("USER_AGENT"),
            os.environ.get("USERNAME"),
            os.environ.get("PASSWORD")
        )

    r.addPagesFromFile("blacklist.txt")
    r.checkSavedPosts()
    r.findNewPosts()

if __name__ == "__main__":
    main()