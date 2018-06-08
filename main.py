from apscheduler.schedulers.blocking import BlockingScheduler
import twitter_interface
import challengers

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=17)
def scheduled_job():
    # Run twitter interface
    api = twitter_interface.connect()
    tw_f, tw_r = twitter_interface.run_daily(api)
    status = twitter_interface.post_daily(tweets=tw_f, api=api)
    db, _ = challengers.connect_db()
    status = challengers.insert_daily(db, tw_f)

sched.start()