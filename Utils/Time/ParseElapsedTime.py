def parseElapsedTime(currentTime, startTime):
    elapsed_time = currentTime - startTime

    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    milliseconds = int((elapsed_time * 1000) % 1000)

    return minutes, seconds, milliseconds
