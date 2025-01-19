# Manages exercise planning

from enum import Enum
import API_Helpers.Google as goog
import pandas as pd
from datetime import datetime, timedelta
from Utils.utils import load_json
from API_Helpers.openai_utils import OpenAIAPI


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


class Training:
    def __init__(self, df):
        df = df.drop(index=df.index[0]).reset_index(drop=True)  # Remove example row
        df['Week Start'] = pd.to_datetime(df['Week Start'], format="%Y/%m/%d")
        self.df = df

    def this_weeks_workout(self):
        today = pd.Timestamp(datetime.now())
        last_week = today - timedelta(days=7)

        this_week = self.df[(self.df['Week Start'] >= last_week) &
                            (self.df['Week Start'] <= today)]

        pd.set_option('display.max_columns', None)  # Show all columns
        display_columns = ['Week Start',
                           'Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7',
                           'Total Time']

        if not this_week.empty:
            return this_week[display_columns]
        else:
            print("No exercise plan for this week.")

    def specific_week_workout(self, date):
        day = pd.to_datetime(date, format="%Y/%m/%d")
        past_week = day - timedelta(days=7)
        the_week = self.df[(self.df['Week Start'] >= past_week) &
                            (self.df['Week Start'] <= day)]

        pd.set_option('display.max_columns', None)  # Show all columns
        display_columns = ['Week Start',
                           'Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7',
                           'Total Time']

        if not the_week.empty:
            return the_week[display_columns]
        else:
            print("No exercise plan for that week.")

    def workouts_in_dates(self, start_date, end_date):
        start_day = pd.to_datetime(start_date, format="%Y/%m/%d")
        end_day = pd.to_datetime(end_date, format="%Y/%m/%d")

        the_weeks = self.df[(self.df['Week Start'] >= start_day) &
                           (self.df['Week Start'] <= end_day)]

        pd.set_option('display.max_columns', None)  # Show all columns
        display_columns = ['Week Start',
                           'Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7',
                           'Total Time']

        if not the_weeks.empty:
            return the_weeks[display_columns]
        else:
            print("No exercise plan within those dates.")


def workouts_to_prompt(workouts):
    return workouts.to_string(index=False, justify='left')


def example():
    credentials_path = '../Credentials/api_keys.json'
    api_keys = load_json(credentials_path)

    scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    user_google_sheets_credentials_path = '../Credentials/google_sheets_user_token.json'
    google_credentials_path = '../Credentials/google_client.json'
    google_sheets_api = goog.google_sheets_utils.GoogleSheetsAPI(user_google_sheets_credentials_path, google_credentials_path, scope)

    # https://docs.google.com/spreadsheets/d/<spreadsheet_id>/edit
    # You will need your own, since it is account based
    spreadsheet_id = '1JFpTX7CfaQ-GYvUSiq6dA397tgVxM1v3x_s2vA_UIeQ'
    spreadsheet_range = 'Weekly Training!A1:X25'
    df = google_sheets_api.load_sheet_to_dataframe(spreadsheet_id, spreadsheet_range)

    training = Training(df)

    this_week_workouts = training.this_weeks_workout()
    if not(this_week_workouts is str):
        this_week_workouts = workouts_to_prompt(this_week_workouts)

    today = datetime.now() - timedelta(days=7)
    six_weeks_ago = today - timedelta(weeks=6)
    six_weeks_workouts = training.workouts_in_dates(six_weeks_ago.strftime('%Y/%m/%d'), today.strftime('%Y/%m/%d'))
    if not(six_weeks_workouts is str):
        six_weeks_workouts = workouts_to_prompt(six_weeks_workouts)

    openai = OpenAIAPI(api_keys['openai_api_key'])

    model = "gpt-4o"
    character = "You are Korra from the tv show Legend of Korra acting as my personal trainer."
    task = "Give a short paragraph summary of the workouts in the upcoming week. Don't mention rest."
    workouts = this_week_workouts
    prompt = character + " " + task + " " + workouts
    completion = openai.ask(model, prompt)
    print(completion.choices[0].message.content)

    model = "gpt-4o"
    character = "You are Korra from the tv show Legend of Korra, acting as my personal trainer."
    goal = "My goal is building cardio and increasing my total time working out to prep for a triathlon training plan."
    task = "Look at the last few weeks of workouts and suggest four workouts for this week with a terse description."
    workouts = six_weeks_workouts
    prompt = character + " " + goal + " " + task + " " + workouts
    completion = openai.ask(model, prompt)
    print(completion.choices[0].message.content)


if __name__ == "__main__":
    example()
