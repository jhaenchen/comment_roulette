import praw
import random
from threading import Thread
import time
import requests

r = praw.Reddit('comment_roulette'
		'Url:http://imtoopoorforaurl.com')
r.login()

def findNegCommentsAndDelete():
	while(1):
		comments = r.user.get_comments('new')
		for comment in comments:
			if(comment.score < 0):
				comment.delete()
		time.sleep(500)

thread = Thread(target = findNegCommentsAndDelete)
thread.start()

appendPhrase = '\n\n --------\n^[Huh?](https://www.reddit.com/r/comment_roulette/wiki/index) ^(I delete negative comments.)'

while True:
    try:
        print "checking...\n"
		#Check my messages
        for message in r.get_unread(unset_has_mail=True, update_user=True):
            if("/u/comment_roulette" in message.body.lower()):
                print "Got new message!"
                parent = r.get_info(thing_id=message.parent_id)
                file = open("responses.txt", 'r+')
                responseOptions = file.read().splitlines()
                message.reply(responseOptions[random.randrange(0,len(responseOptions))]+appendPhrase)
                if(parent.author.name == "agreeswithmebot"):
                    quote = 'Uh oh, we got ourselves a smart guy here! Try again :)'
                    newComment = message.reply(quote)
                    user = message.author
                    r.send_message(user.name, 'AgreesWithMeBot', 'Hey, you seem pretty clever. Maybe contribute to our [github](https://github.com/jhaenchen/agreeswithmebot)?')
                elif(isinstance(parent, praw.objects.Comment)):
                    messageText = parent.body
                    messageText = messageText.replace("/u/comment_roulette","")
                    messageText = messageText.replace("\n","\\n")
                    file.write(messageText + "\\n\\n -/u/" + message.author.name + "\n")
                file.flush()
                file.close()
                message.mark_as_read()
        print "sleeping..."
        time.sleep(15)
    except requests.exceptions.ReadTimeout:
        print "Read timeout. Will try again."
    except praw.errors.Forbidden:
        print "Im banned from there."
        user = message.author
        message.mark_as_read()
        r.send_message(user.name, 'comment_roulette', 'Hey, I\'m banned from \\r\\'+message.subreddit.display_name+'. Sorry.')
    except praw.errors.HTTPException as e:
        pprint(vars(e))	
        print(e)
        print "Http exception. Will try again."
    except praw.errors.RateLimitExceeded as error:
        print '\tSleeping for %d seconds' % error.sleep_time
        time.sleep(error.sleep_time)		
    except requests.exceptions.ConnectionError:
        print "ConnectionError. Will try again."
    except praw.errors.APIException:
        print "API exception. Will try again."
    except (KeyboardInterrupt, SystemExit):
        print "Safe exit..."
        raise
    except:
        print "Unhandled exception, bail!"
        r.send_message('therealjakeh', 'comment_roulette', 'Just went down! Help! Exception: ')
        raise
