# How to set up the bot

To set up the bot all you need to do is fill in the info in the safety.py file and the bot should be ready to go. 
Below is a guide on how to get all the info you need. 

## Getting Credentials

### NOTE: IF YOU PLAN ON UPLOADING YOUR CODE TO GITHUB MAKE SURE TO ADD SAFETY.PY TO YOUR GITIGNORE

### TOKEN

To get your discord bot token follow these steps:
1. Go to the [discord's developer portal](https://discord.com/developers/applications)
2. Click "New Application" in the top right corner 
3. Type a name for your bot and click create
4. On the left-hand side click "Bot" then click "Add Bot" and confirm
5. Click "Copy" where it says token and then paste the token into the safety.py file

### API_KEY
To get your google api key follow these steps:
1. Go to this [link](https://developers.google.com/custom-search/v1/introduction#identify_your_application_to_google_with_api_key)
2. Click the blue "Get a key" button 
3. Click "create a new project" and name it what you wish
4. Click "Next" 
5. Copy the api key that you are given and paste it into the safety.py file

### CSE_ID
To get your custom search engine id follow these steps:
1. Go to this [link](https://programmablesearchengine.google.com/cse/all)
2. Click "Add" and add the two sites listed below
   1. www.wikipedia.com
   2. www.xkcd.com
3. Name the search engine whatever you wish and click create
4. Click "Get Code", then copy the code written next to **cx=**
5. Paste the code into the safety.py file 


### Errors
There are two errors you may receive
1. Youtube Command Error - This error will give you a link you need to go to in order to enable the Youtube Api, after doing so the command will work. 
2. Wikipedia/XKCD Error - Go to this [link](https://console.developers.google.com/apis/credentials?project=578680288012), click create credentials >> service account, fill in the details then hit create and continue, then click done 

