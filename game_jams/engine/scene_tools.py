class FrameCounter:
    def __init__(self, fps: int):
        self.fps = fps
        self.frame: int = 0
        self.millisecond: int = 0
        self.seconds: int = 0
        self.minutes: int = 0
        self.new_second = False
        self.new_minute = False

    def tick(self, delta_time: float):
        self.new_second = False
        self.new_minute = False
        self.frame += 1
        self.millisecond += int(delta_time * 1000)
        if self.millisecond >= 1000:
            self.millisecond -= 1000
            self.seconds += 1
            self.new_second = True
        if self.seconds >= 60:
            self.seconds -= 60
            self.minutes += 1
            self.new_minute = True


__all__ = ["FrameCounter"]
