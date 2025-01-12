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


def last_week_workout(sheets_service):
    # https://docs.google.com/spreadsheets/d/<spreadsheet_id>/edit
    training_spreadsheet_id = '1JFpTX7CfaQ-GYvUSiq6dA397tgVxM1v3x_s2vA_UIeQ'
    training_spreadsheet_range = 'Weekly Training!A1:X25'
    training_column_types = {
        'Week': str,
        'Week Start': str,
        'Day 1': str,
        'Day 1 Data': str,
        'Day 2': str,
        'Day 2 Data': str,
        'Day 3': str,
        'Day 3 Data': str,
        'Day 4': str,
        'Day 4 Data': str,
        'Day 5': str,
        'Day 5 Data': str,
        'Day 6': str,
        'Day 6 Data': str,
        'Day 7': str,
        'Day 7 Data': str,
        'Run Distance': str,
        'Bike Distance': str,
        'Swim Distance': str,
        'Total Distance': str,
        'Total Time': str,
        'Running Goal': str,
        'Biking Goal': str,
        'Swimming Goal': str
    }

    # Load data into a Pandas DataFrame
    df = load_google_sheet_to_dataframe(sheets_service, training_spreadsheet_id,
                                        training_spreadsheet_range,
                                        column_types=training_column_types)

    df['Week Start'] = pd.to_datetime(df['Week Start'], format="%Y/%m/%d")

    # Get today's date in PST
    today_pst = pd.Timestamp(datetime.now())
    start_date = today_pst - timedelta(days=13)
    end_date = today_pst - timedelta(days=6)

    last_week = df[(df['Week Start'] >= start_date) &
                   (df['Week Start'] <= end_date)]

    pd.set_option('display.max_columns', None)  # Show all columns
    display_columns = ['Week', 'Week Start', 'Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']

    if not last_week.empty:
        print(last_week[display_columns])
    else:
        print("No exercise plan for last week.")


def next_week_workout(sheets_service):
    # https://docs.google.com/spreadsheets/d/<spreadsheet_id>/edit
    training_spreadsheet_id = '1JFpTX7CfaQ-GYvUSiq6dA397tgVxM1v3x_s2vA_UIeQ'
    training_spreadsheet_range = 'Weekly Training!A1:X25'
    training_column_types = {
        'Week': str,
        'Week Start': str,
        'Day 1': str,
        'Day 1 Data': str,
        'Day 2': str,
        'Day 2 Data': str,
        'Day 3': str,
        'Day 3 Data': str,
        'Day 4': str,
        'Day 4 Data': str,
        'Day 5': str,
        'Day 5 Data': str,
        'Day 6': str,
        'Day 6 Data': str,
        'Day 7': str,
        'Day 7 Data': str,
        'Run Distance': str,
        'Bike Distance': str,
        'Swim Distance': str,
        'Total Distance': str,
        'Total Time': str,
        'Running Goal': str,
        'Biking Goal': str,
        'Swimming Goal': str
    }

    # Load data into a Pandas DataFrame
    df = load_google_sheet_to_dataframe(sheets_service, training_spreadsheet_id,
                                        training_spreadsheet_range,
                                        column_types=training_column_types)

    df['Week Start'] = pd.to_datetime(df['Week Start'], format="%Y/%m/%d")

    # Get today's date in PST
    today_pst = pd.Timestamp(datetime.now())

    next_week = df[(df['Week Start'] >= today_pst - timedelta(days=6))
                   & (df['Week Start'] <= today_pst + timedelta(days=1))]

    pd.set_option('display.max_columns', None)  # Show all columns
    display_columns = ['Week', 'Week Start', 'Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']
    if not next_week.empty:
        print(next_week[display_columns])
    else:
        print("No exercise plan for next week.")
