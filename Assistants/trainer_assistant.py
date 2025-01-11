# Manages exercise planning

from enum import Enum


class WorkoutDay:
    def __init__(self):
        self.workouts = []

    def add_workout(self, workout):
        self.workouts.append(workout)


class Workout:
    def __init__(self, start_time=None, brick=False):
        self.start_time = start_time
        self.brick = brick
        self.warm_up_segments = []
        self.main_segments = []
        self.cool_down_segments = []

    def add_warm_up_segment(self, workout_segment):
        self.warm_up_segments.append(workout_segment)

    def add_main_segment(self, workout_segment):
        self.main_segments.append(workout_segment)

    def add_cool_down_segment(self, workout_segment):
        self.cool_down_segments.append(workout_segment)


class Effort:
    def __init__(self):
        self.rpe = "unknown"
        self.hr = "unknown"
        self.hr_zone = "unknown"
        self.ftp = "unknown"
        self.breathing = "unknown"

        # TODO: define setting functions for each, that set all the rest
        # https://docs.google.com/spreadsheets/d/1JFpTX7CfaQ-GYvUSiq6dA397tgVxM1v3x_s2vA_UIeQ/edit?gid=1083446366#gid=1083446366


class Sport(Enum):
    BIKE = "Bike"
    RUN = "Run"
    SWIM = "Swim"
    STRENGTH_TRAIN = "Strength Train"
    ROW = "Row"
    BOX = "Box"
    YOGA = "Yoga"
    CLIMB = "Climb"
    ROLLER_SKATE = "Roller Skate"
    UNCATEGORIZED = "Uncategorized"


class WorkoutSegment:
    def __init__(self, sport=Sport.UNCATEGORIZED, duration=0):
        self.sport = sport
        self.duration = duration
        self.effort = Effort()


class Bike(WorkoutSegment):
    def __init__(self, duration):
        super().__init__(sport=Sport.BIKE, duration=duration)


class Run(WorkoutSegment):
    def __init__(self, duration):
        super().__init__(sport=Sport.RUN, duration=duration)


class Swim(WorkoutSegment):
    def __init__(self, duration):
        super().__init__(sport=Sport.SWIM, duration=duration)


class StrengthTrain(WorkoutSegment):
    def __init__(self, duration):
        super().__init__(sport=Sport.STRENGTH_TRAIN, duration=duration)


class Row(WorkoutSegment):
    def __init__(self, duration):
        super().__init__(sport=Sport.ROW, duration=duration)


class Box(WorkoutSegment):
    def __init__(self, duration):
        super().__init__(sport=Sport.BOX, duration=duration)


class Yoga(WorkoutSegment):
    def __init__(self, duration):
        super().__init__(sport=Sport.YOGA, duration=duration)
