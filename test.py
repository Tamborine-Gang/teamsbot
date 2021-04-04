import schedule
schedule.every().sunday.at("21:25:50").do(lambda: print("hahnayesd"))
while True:
    schedule.run_pending()
    
