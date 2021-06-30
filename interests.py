# TODO: find a way to check if the subreddit chosen by the user actually exists
#       find a way to add new topics if the user choses so
#       find a way to have the user choose how many days back they want to go
#       clean up the code

import praw
from datetime import datetime

# read password, client id and client secret so the user can log in.
with open('reddit_pw.txt', 'r') as f:
	for position, line in enumerate(f):
		if position == 0:
			secret_password = line.strip()
		if position == 1:
			client_id = line.strip()
		if position == 2:
			client_secret = line.strip()

# authenticate with the server.
reddit = praw.Reddit(
    client_id = client_id,
    client_secret = client_secret,
    user_agent = 'Ubuntu:Interests:v0.01:u/tarzan_code',
    username = 'tarzan_code',
    password = secret_password
)

# choose the subreddit the user is interested in.
subreddit = reddit.subreddit(input('Which subreddit are you interested in today?\n-'))

# create an empty list for the topics the user is interested in and register what they are.
topics = []
answer = input('And what topics are you interested in? (Type "end" when you are finished.)\n-').lower().strip()

while answer != 'end':
    topics.append(answer)
    answer = input('-').lower().strip()

# show user the list of topics they have created and ask if they want to remove or add any.
print('Here is the list of topics you are interested in:')
for i in topics:
    print(f'- {i}')

mind_changed = input('Would you like to remove any of them?(y/n)\n-').lower().strip()

while mind_changed != 'y' and mind_changed != 'n':
    mind_changed = input('Please either reply with "y" for yes or "n" for no.\n-').lower().strip()            
    
while mind_changed == 'y':
    topic_change = input('Which one would you like to remove? If you have changed your mind, then type "none".\n-').lower().strip()
    if topic_change == 'none':
        break
    elif topic_change in topics: # check to make sure that the topic the user wants to remove actually exists in the list of topics they have entered.
        topics.remove(topic_change)
        print(f'{topic_change} has been removed from the topics list!')
        print('Here is the updated list of topics:')
        for i in topics:
            print(f'- {i}')
        mind_changed = input('Do you want to make any other changes?(y/n)\n-')
        while mind_changed != 'y' and mind_changed != 'n':
            mind_changed = input('Please either reply with "y" for yes or "n" for no.\n-').lower().strip()            
    else:
        print('That is not part of the list you have created.')

# ask the user if they want to add any new topics.
mind_changed = input('Would you like to add any new topics?(y/n)\n-').lower().strip()

while mind_changed != 'y' and mind_changed != 'n':
    mind_changed = input('Please either reply with "y" for yes or "n" for no.\n-').lower().strip()            

if mind_changed == 'y':
    print('After you are done adding new topics type "end" to finish the process.\n')

answer = ''
while mind_changed == 'y' and answer != 'end':
    answer = input('-').lower().strip()
    topics.append(answer)

if mind_changed == 'y':
    print('Here is the updated list of topics:')
    for i in topics:
        print(f'- {i}')

print('If you get no confirmation that a post about a topic you are interested in has been found and saved that means there are none currently available for today.\n')

# iterate through posts in 'new' to find any posts that include the topics the user is interested in and save them in their reddit account.
for submission in subreddit.new(limit=100):
    """datetime.fromtimestamp() --> turns POSIX time in local time
        datetime.date() --> returns the date part of the time provided
        datetime.now() --> returns the current date and time
    """
    if datetime.date(datetime.fromtimestamp(submission.created_utc)) == datetime.date(datetime.now()):
        for i in topics:
            timer = 0
            if i in submission.title or i in submission.selftext:
                print(f'* {i} * was found in ** {submission.title} ** and was added to your saved posts')
                submission.save()
    else:
        break