from config import *
import requests
import pandas as pd
import datetime

# Setting options for correcting outputting the pandas dataframe
desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 12)

# Yesterdays date needed for querying the data until yesterday as
# the current day might no yet be completed
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

# Requesting time entries
headers = {'X-MiteApiKey': MITE_API_KEY}
payload = {'user_id': 'current', 'to': yesterday}
time_entries = requests.get(MITE_URL_TIME_ENTRIES, headers=headers, params=payload).json()

# The time entries come in the structure [{"time_entry":{"..."}},{"time_entry":{"..."}}] which can't be properly
# converted to Pandas dataframe. Hence it needs to be restructured first
time_entries = [time_entry['time_entry'] for time_entry in time_entries]

time_entries_df = pd.DataFrame(time_entries)

# Getting number of working days
no_working_days = len(time_entries_df[time_entries_df.service_name != 'Public Holidays'].date_at.unique())
# Getting the number minutes spent on sick leave
paid_absence_minutes = time_entries_df[time_entries_df.service_name.str.contains('sick')]['minutes'].sum()
# Getting the number of minutes spent on vacation
no_holidays_minutes = time_entries_df[time_entries_df.service_name.str.contains('Vacation')]['minutes'].sum()
# Getting the overtime
working_time_entries_df = time_entries_df.query('service_name != "Public Holidays" & service_name != "Overtime"')
working_time_minutes = working_time_entries_df['minutes'].sum()
overtime_minutes = working_time_minutes - no_working_days * 8 * 60

# Creating KPI's for reporting
mite_insights = {'Working Days': no_working_days, 'Sick Leave (days)': paid_absence_minutes / 60 / 8,
                 'Holidays': int(no_holidays_minutes / 60 / 8), 'Overtime': overtime_minutes / 60}

mite_insights_df = pd.DataFrame(mite_insights, index=[1])

# Getting relevant entries without any notes. Notes need to be added to these entries.
entries_without_note = time_entries_df.query('(note.isna() | note == "") & service_name != "Overtime" '
                                             '& service_name != "Public Holidays" & service_name != "Vacation"')

# Getting entries that have a service names
entries_with_odd_service = time_entries_df.query('project_name != "foryouandyourcustomers Munich (internal)" '
                                                 '& (service_name != "Consulting" & service_name != "Sales")'
                                                 )

print(mite_insights_df)
print("---------------------------------------------------------------------------------------- \n")
if entries_without_note.empty:
    print('No entries without empty notes')
else:
    print(entries_without_note[['date_at', 'project_name', 'service_name']])
print("---------------------------------------------------------------------------------------- \n")
if entries_with_odd_service.empty:
    print('No entries with odd service names')
else:
    print(entries_with_odd_service[['date_at', 'project_name', 'service_name']])