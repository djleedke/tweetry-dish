from pytz import utc
from apscheduler.schedulers.blocking import BlockingScheduler
from application import tweetry_manager

scheduler = BlockingScheduler()
scheduler.configure(timezone=utc)

#Scheduled to run everyday at 12:00am UTC
@scheduler.scheduled_job('cron', hour=0)
def cron_job():
    print(f'Scheduler: Tweeting: { tweetry_manager.tweet_final_quote() }')
    tweetry_manager.create_new_tweetry()
    print('Scheduler: A new tweetry has been created.')

scheduler.start()