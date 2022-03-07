# ReflectionsInDataScience

### env variables

POSTLIMIT
- Should be an int. Is the amount of posts you want to pull from reddit. Recall that the reddit api does calls in 100 item increments, so a postlimit of 200 is two api calls and a postlimit of 201 is three.

CLIENT_ID
- Client id from your reddit app, can be found on your applications page

CLIENT_SECRET
- Client secret is generated when you make a new app in the reddit dev portal.

USER_AGENT
- Reddit api user agents are not like regular useragents. Since reddit expects you to use a third party app created by you to interact with the api. This means you dont need an useragent which emulates a browser, but should have a useragent which tells which app along with version and creator, "testapp v1 by u/myusername", is making the call instead.

USERNAME
- Your reddit username

PASSWORD
- Your reddit password