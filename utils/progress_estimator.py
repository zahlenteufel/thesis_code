import time


class ProgressEstimator:

    def __init__(self):
        self.time = time.time()
        self.rates = []

    def remaining_seconds(self, progress):
        self.rates.append((time.time() - self.time) / progress)  # how much time would the 100% take?
        # use last five rates
        if len(self.rates) > 5:
            self.rates = self.rates[-5:]
        mean_rate = sum(self.rates) / float(len(self.rates))
        remaining = 1.0 - progress
        return remaining * mean_rate

    def remaining_time(self, progress):
        remaining_seconds = self.remaining_seconds(progress)
        remaining_minutes, remaining_seconds = divmod(remaining_seconds, 60)
        if remaining_minutes:
            return "%d m %d s" % (remaining_minutes, remaining_seconds)
        else:
            return "%d s" % remaining_seconds
