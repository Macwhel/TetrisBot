import time


class Stats(object):
    def __init__(self):
        self.totalPiecesPlaced = self.totalLinesSent = 0
        self.startTime = time.time()

    def incrementTotalPiecesPlaced(self):
        self.totalPiecesPlaced += 1

    def incrementTotalLinesSent(self, lines):
        self.totalLinesSent += lines

    def getElapsedTimeInSeconds(self):
        return time.time() - self.startTime

    def getMinutesSecondsMilliseconds(self):
        elapsed_time = self.getElapsedTimeInSeconds()
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        milliseconds = int((elapsed_time * 1000) % 1000)

        return minutes, seconds, milliseconds

    def getMinutes(self):
        return self.getElapsedTimeInSeconds() / 60

    def getSeconds(self):
        return self.getElapsedTimeInSeconds()

    def getAPM(self):
        return round(self.totalLinesSent / self.getMinutes(), 2)

    def getPPS(self):
        return round(self.totalPiecesPlaced / self.getSeconds(), 2)
