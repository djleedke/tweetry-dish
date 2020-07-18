from apscheduler.schedulers.background import BackgroundScheduler
from application import tweetry_manager

scheduler = BackgroundScheduler()
print('Scheduler: Initialized')

@scheduler.scheduled_job('interval', seconds=30)
def job():

    print(f'Scheduler: Tweeting: { tweetry_manager.tweet_final_quote() }')
    
    tweetry_manager.create_new_tweetry()
    print('Scheduler: A new tweetry has been created.')

scheduler.start()