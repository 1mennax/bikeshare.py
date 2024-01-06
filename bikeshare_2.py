import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def view_trip_data(df):
    """
    Allows the user to view 5 rows of individual trip data and continue if desired.
    Args:
        df: Pandas DataFrame containing trip data
    """
    start_loc = 0
    while True:
        view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no: ").lower()
        if view_data != 'yes':
            break

        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5

        view_display = input("Do you wish to continue? Enter yes or no: ").lower()
        if view_display != 'yes':
            break


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    valid_cities = ['chicago', 'new york city', 'washington']
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

    while True:
        user_input = input('Enter the city, month, and day separated by commas (e.g., Washington, January, Monday): ').lower()
        user_input = user_input.replace(" ", "")

        # Split user input into city, month, and day
        input_values = user_input.split(',')

        if len(input_values) != 3:
            print("Please provide all three values (city, month, day) separated by commas.")
        else:
            city, month, day = map(str.strip, input_values)
            # Now you can use city, month, and day variables for further processing
            print(f"City: {city}, Month: {month}, Day: {day}")

        # Check if the city is valid
        if city.strip() in valid_cities:
            city = city.strip()
            break
        else:
            print('Invalid city input. Please enter a valid city.')

    # Check if the month is valid
        if month.strip() not in valid_months:
            print('Invalid month input. Applying no month filter.')
            month = 'all'
        else:
            month = month.strip()

        # Check if the day is valid
        if day.strip() not in valid_days:
            print('Invalid day input. Applying no day filter.')
            day = 'all'
        else:
            day = day.strip()

        print('-' * 40)
        return city, month, day


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

    df = pd.read_csv(CITY_DATA[city])

    # Convert input month/day to lowercase for case insensitivity in filtering
    month = month.lower()
    day = day.lower()

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Filter by month and day if not 'all'
    if month != 'all':
        df = df[df['Start Time'].dt.month_name().str.lower() == month]

    if day != 'all':
        df = df[df['Start Time'].dt.day_name().str.lower() == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0]

    print(f'Most Popular Start Month: {common_month}')

    # display the most common day of week
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day'] = df['Start Time'].dt.weekday_name
    common_day = df['day'].mode()[0]

    print(f'Most Popular Start Day: {common_day}')

    # display the most common start hour

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]

    print(f'Most Popular Start Hour: {common_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts()
    print(f'Commonly used start station is: {start_station}')

    # display most commonly used end station
    end_station = df['End Station'].value_counts()
    print(f'Commonly used end station is: {end_station}')

    # display most frequent combination of start station and end station trip
    start_end_station = df.groupby(['Start Station'])['End Station'].value_counts()
    print(f'Commonly used start and end station: {start_end_station}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_travel_time = df['Trip Duration'].sum()
    print(f'Total travel time is all trips: {total_travel_time}')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f'Mean travel time in all trips: {mean_travel_time}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'Total counts of user types: {user_types}')

    # Display counts of gender
    if 'Gender' in CITY_DATA:
        gender = df['Gender'].value_counts()
        print(f'Total gender count: {gender}')
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the city data')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in CITY_DATA:
        earliest_year = df['Birth Year'].min()
        print(f'Earliest year of birth: {earliest_year}')
        recent_year = df['Birth Year'].max()
        print(f'Recent year of birth: {recent_year}')
        common_year = df['Birth Year'].mode()[0]
        print(f'Most common year of birth: {common_year}')
    else:
        print('Earliest year, recent year and most common year cannot be calculated because these does not appear in the city data')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        view_trip_data(df)  # Add this line to view trip data

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
