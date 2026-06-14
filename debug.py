import datetime

class Debug:
    now = datetime.now()
    time_str = now.strftime("%Y-%m-%d-%H-%M-%S")
    log = open(f"logs\\{time_str}.txt", "w+")