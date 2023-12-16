import datetime

class Timer():
    def __init__(self) -> None:
        self.reset()
    def get_seconds(self):
        return (datetime.datetime.now() - self.start - self.stop_delta)
    def stop_timer(self):
        self.stop_start = datetime.datetime.now()
    def start_timer(self):
        self.stop_end = datetime.datetime.now()
        self.stop_delta += self.stop_end - self.stop_start - datetime.timedelta(seconds=1)
    def reset(self):
        self.start = datetime.datetime.now()
        self.stop_delta = datetime.timedelta() 
    def get_time(self):
        elapsed_time = self.get_seconds()
        minutes, seconds = divmod(elapsed_time.seconds, 60)
        return f"{minutes:02}:{seconds:02}"





