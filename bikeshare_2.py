import time
import pandas as pd


CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}

# lists for check validity of user input
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
filter_data_list = ['month', 'day', 'both', 'none']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    global month
    global day
    global city

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city =  check_input("Do you want to see data for 'Chicago', 'New York City' or 'Washington'?\n")
    filter_data = check_input("Would you like to filter the data by 'month', 'day', 'both' or not at all? Type 'none' for no time filter.\n")

    if filter_data == "month":
        month = check_input("Which month? 'January', 'February', 'March', 'April', 'May' or 'June' or 'All'?\n")
        day = "all"
    elif filter_data == "day":
        day = check_input("Which day? 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' or 'All'\n")
        month = "all"
    elif filter_data == "both":
        month = check_input("Which month? January, February, March, April, May or June?\n")
        day = check_input("Which day? 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' or 'All'\n")
    elif filter_data =="none":
        month = "all"
        day = "all"

    #print('-'*40)
    return city, month, day

def check_input(user_text):
    while True:
        modified_user_text=input(user_text).lower()
        try:
            if modified_user_text in ['chicago','new york city', 'washington']:
                break
            elif modified_user_text in months:
                break
            elif modified_user_text in days:
                break
            elif modified_user_text in filter_data_list:
                break
            else:
                print("Wrong input! Try again and ensure correct spelling!")
        except ValueError:
            print("Your input is not correct!")
    return modified_user_text




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
    #Load data into dataframe
    df = pd.read_csv(CITY_DATA[city])

    #Convert Start Time
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #seperate month, day and hour for new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    #filter
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most common month is: ', most_common_month)

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('Most common day of week: ', most_common_day)

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('Most common start hour of day is: ', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most common start station: ', most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most common end station: ', most_common_end_station)


    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + " " + "to" + " " + df['End Station']
    pop_com = df['combination'].mode()[0]
    print("The most frequent combination of Start and End Station is {} ".format(pop_com))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time: ', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User types in data: ', df['User Type'].value_counts())

    #Only for New York City and Chicago
    if city.title() == "new york city" or city.title() == "washington":
        # Display counts of gender
        print('Counts of gender: ', df['Gender'].value_counts())
        # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        print('Earliest year: ', earliest_year)
        most_recent_year = df['Birth Year'].max()
        print('Most recent year: ', most_recent_year)
        most_common_year = df['Birth Year'].mode()[0]
        print('Most common year: ', most_common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#view raw data
def show_row_data(df):
    row=0
    while True:
        view_raw_data = input("Would you like to see the raw data? Enter 'Yes' or 'No'.\n").lower()
        if view_raw_data == 'yes':
            print(df.iloc[row:row+5])
            row += 5
        elif view_raw_data == 'no':
            break
        else:
            print(("Wrong input! Try again"))

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_row_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
