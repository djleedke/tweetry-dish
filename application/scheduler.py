from apscheduler.schedulers.background import BackgroundScheduler
from application import tweetry_manager

scheduler = BackgroundScheduler()
scheduler.configure(timezone=utc)

#Scheduled to run everyday at 12:00am UTC
@scheduler.scheduled_job('interval', day_of_week='mon-sun', hour=0)
def job():

    print(f'Scheduler: Tweeting: { tweetry_manager.tweet_final_quote() }')
    
    tweetry_manager.create_new_tweetry()
    print('Scheduler: A new tweetry has been created.')

scheduler.start()