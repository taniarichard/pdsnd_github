import time
import pandas as pd
import numpy as np
import calendar
from datetime import date

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = CITY_DATA.keys()
months = list(calendar.month_name[:7])
days = list(calendar.day_name)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let\'s explore some US bikeshare data!")

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input ("\nPlease enter \"Chicago\", \"New York City\" or \"Washington\":\n\n").lower()
        if city in cities:
            break
        else:
            print()
            print('~'*40)
            print("Sorry, the data for this city is not available.")
            print('~'*40)
            continue

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input ("\nPlease enter a month from January to June.\nFor no filter, enter \"all\":\n\n").lower().strip()
        if month.title() == "All":
            break
        elif month.title() in months:
            break
        else:
            print()
            print('~'*40)
            print('Sorry, there is no data for this month.')
            print('~'*40)
            continue;

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input ("\nPlease enter a day of the week or \"all\" for all days:\n\n").strip().lower()
        if day.title() == "All":
            break
        elif day.title() in days:
            break
        else:
            print()
            print('~'*40)
            print('Please check your spelling and try again.')
            print('~'*40)
            continue;
    print('-'*40)
    print()
    print('Getting the data for:\n')
    print('\ncity:\t{} \nmonth:\t{} \nday:\t{}'.format(city, month, day).title(), '\n')

    print('-'*40)
    return city, month, day;


#Loading and filtering data

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # TO DO: display the most common month
    #getting the month name based on its index using the calendar module:
    common_month = calendar.month_name[df['month'].mode()[0]]
    print("\nMost common ride month:\t{}".format(common_month))

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("Most common ride day:\t{}".format(common_day))

    # TO DO: display the most common start hour
    #The output is formatted to "HH:MM" with .strftime("%H:%M")
    common_start_hour = df['Start Time'].mode()[0].strftime("%H:%M")
    print("Most common start time:\t{}".format(common_start_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    #getting the total of rides in the filtered data set:
    total_rides = len(df.index)
    print('Total rides:\t{}\n'.format(total_rides))
    
    #getting the most used start station:
    common_start_station = df['Start Station'].mode()[0]
    print('Most common start station:\t\t\t',common_start_station)

    #getting the number of rides that started at the most used start station:
    start_times_used = df['Start Station'].value_counts().max()
    print ('Number of rides started here:\t\t\t',start_times_used)

    #getting the percentage of rides that started on the most used start station:
    precentage_common_start = (start_times_used / total_rides)*100
    print('Percentage of rides started here:\t\t', round(precentage_common_start,1),'%' )


    # TO DO: display most commonly used end station
    #getting the most used end station:
    common_end_station = df['End Station'].mode()[0]
    print('\nMost common end station:\t\t\t', common_end_station)

    #getting the number of rides that ended at the most used end station:
    end_times_used = df['End Station'].value_counts().max()
    print ('Number of rides that ended here:\t\t',end_times_used)

    #getting the percentage of rides that ended at the most used end station:
    precentage_common_end = (end_times_used / total_rides)*100
    print('Percentage of rides that ended here:\t\t', round(precentage_common_end,1),'%' )


    # TO DO: display most frequent combination of start station and end station trip
    #creating a column in the data frame with a to/from station combination:
    df['From / To'] = df['Start Station'].str.cat(df['End Station'], sep=' => ')

    #getting the most used to/from station combination:
    common_from_to = df['From / To'].mode()[0]
    print("\nMost commont to/from combination:\t\t", common_from_to)

    #getting the number of rides with this to/from station combination:
    combo_times_used = df['From / To'].value_counts().max()
    print("Number of rides with this combination:\t\t", combo_times_used)

    #getting the percentage of rides with this to/from station combination:
    precentage_combo = (combo_times_used / total_rides)*100
    print("Percentage of rides with this combination:\t", round(precentage_combo,2),'%' )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    # TO DO: display total travel time
    #getting values for hours, minutes and seconds:
    mn, sec = divmod(df['Trip Duration'].sum(), 60)
    hr, mn = divmod(mn, 60)
    print ("Total travel time:\t\t%d h %02d min %02d sec" % (hr, mn, sec))

 # TO DO: display mean travel time
    mn, sec = divmod(int(df['Trip Duration'].mean()), 60)
    hr, mn = divmod(mn, 60)
    print ("Average travel time:\t%d h %02d min %02d sec" % (hr, mn, sec))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    #getting the number of users per user type:
    count_per_user_type = df['User Type'].value_counts()

    #coverting the result into a dictionary for a better looking output:
    count_per_user_type_dict = dict(count_per_user_type)
    print('Number of users per user type:\n')
    for key, value in count_per_user_type_dict.items():
            print(key,":\t", value)

    #getting a percentage of users per user type and coverting it into a dictionary for a better looking output:
    percent_per_user_type = dict(df['User Type'].value_counts(normalize=True)*100)
    print("\nPercentage of users per user type:\n")
    for key, value in percent_per_user_type.items():
        value = round(value, 1)
        print(key,":\t", value, "%")


    # TO DO: Display counts of gender

    #Gender data is not available for all cities, so we use an if statement
    #to inform the user when this data is not available:
    if 'Gender' in df:
        #getting the number of values per gender:
        count_per_gender = df['Gender'].value_counts()

        #coverting the result into a dictionary for a better looking output:
        count_per_gender_dict = dict(count_per_gender)
        print("\nNumber of users per gender:\n")
        for key, value in count_per_gender_dict.items():
            print(key,":\t", value)

        #getting a percentage of users per gender and coverting it into a dictionary for a better looking output:
        percent_per_gender = dict(df['Gender'].value_counts(normalize=True)*100)
        print("\nPercentage of users per gender:\n")
        for key, value in percent_per_gender.items():
            value = round(value, 1)
            print(key,":\t", value, "%")
    else:
        print("\nNo gender information is available.")


    # TO DO: Display earliest, most recent, and most common year of birth
    #Birth Year data is not available for all cities, so we use an if statement to inform the user when this data is not available:
    if 'Birth Year' in df:
        #getting the earlies birth year:
        min_year = df['Birth Year'].min()
        print('\nThe earliest birth year:\t', int(min_year))

        #getting the latest birth year:
        max_year = df['Birth Year'].max()
        print('The most recent birth year:\t', int(max_year))

        #getting the most common birth year:
        mode_year = df['Birth Year'].mode()
        print('The most common birth year:\t', int(mode_year))

        #getting the oldest rider's age:
        oldest_rider = date.today().year - int(min_year)
        print('\nThe oldest rider\'s age:\t', oldest_rider)

        #getting the youngest rider's age:
        youngest_rider = date.today().year - int(max_year)
        print('The youngest rider\'s age:\t', youngest_rider)

        #getting the average rider age:
        average_age = date.today().year - int(mode_year)
        print('The average rider age is:\t', average_age)
    else:
        print('No birth year information is available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def dislpay_rawdata(df):
    """Script prompts the user if they want to see 5 lines of raw data, display that data if the answer is 'yes', and continue these prompts and displays until the user says 'no'."""
    #setting up indexes
    n = 5
    first = 0
    last = n - 1

    print('\nWould you like to see the data on the first 5 individual trips?')
    while True:
        #getting the user's input:
        yes_no_input = input('Enter yes or no:\n')

        #the if statement allowing to accept as valid an input that starts with "y" for yes
        #and an input that starts with "n" for no. The input starting with any other letter is invalid:
        if yes_no_input[0].lower() == 'y':
            print()
            print('~'*40)
            print('Rows {} - {}:'.format(first + 1, last + 1))
            print('~'*40)
            print('\n', df.iloc[first : last + 1])
            first += n
            last += n
            print('-'*40)
            print('\nWould you like to see the next {} rows?'.format(n))
            continue
        elif yes_no_input[0].lower() == 'n':
            break
        else:
            continue

#The function will restart the script if the user enters "yes" and exit if the user enters "no":
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        dislpay_rawdata(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

#USED RESOURCES:

#For printing a dictionary without brackets and quotation marks:
#https://stackoverflow.com/questions/40071006/python-2-7-print-a-dictionary-without-brackets-and-quotation-marks

#For rounding values:
#https://datatofish.com/round-values-pandas-dataframe/

#For getting a month name from its index:
#https://stackoverflow.com/questions/6557553/get-month-name-from-number

#For displaying a defined number of data frame rows:
#https://www.shanelynn.ie/select-pandas-dataframe-rows-and-columns-using-iloc-loc-and-ix/#iloc-selection
