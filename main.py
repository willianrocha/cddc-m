from apscheduler.schedulers.blocking import BlockingScheduler
import twitter_interface

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=20)
def scheduled_job():
    # Run twitter interface
    api = twitter_interface.connect()
    twitter_interface.run(api)

sched.start()