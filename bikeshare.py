import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': './data/chicago.csv',
             'new york': './data/new_york_city.csv',
             'washington': './data/washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # variable to use for checking valid user input
    city_list = ['chicago', 'new york', 'washington']
    month_list = ['january', 'february', 'march', 'april', 'may', 'june']
    day_list = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    
    # default values to be returned if user sets no time filter
    month = 'all'
    day = 'all' 

    # check if user input for city is valid
    while True:
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input('Would you like to see data from Chicago, New York or Washington?').lower()
        if city:
            if city in city_list:
                break
            else:
                print('You have entered an invalid city. Enter either Chicago, New York or Washington.')

        
    filter_data = input('Would you like to filter the data by month, day, both or not at all? Type "None" for no time filter').lower()
    while filter_data == 'both':
        # get user input for month (all, january, february, ... , june)
        month = input('Which month would you like to see data from? January, February, March, April, May, or June?').lower()
        
        # get user input for day of week (all, monday, tuesday, ... sunday)   
        day = input('Which day of the week would you like to see data from?').lower()
        
        if month in month_list and day in day_list:
            break
        else:
            print('Invalid Entry. Please enter month and day in a full text format i.e., january, february, saturday, monday,...')
        
    while filter_data == 'month':
        # get user input for month (all, january, february, ... , june)
        month = input('Which month would you like to see data from? January, February, March, April, May, or June?').lower()
        
        # check if user input is valid
        if month in month_list:
            break
        else:
            print('You have entered an invalid month. Please select from January to June.')
                
    while filter_data == 'day':
        # get user input for day of week (all, monday, tuesday, ... sunday)   
        day = input('Which day of the week would you like to see data from? Enter as monday, tuesday, wednesday...').lower() 
        
        # check if value is valid
        if day in day_list:
            break
        else:
            print('You have entered an invalid week day.')
        
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    # by selecting the CITY_DATA dict key and retrieve the value associated
    df = pd.read_csv(CITY_DATA[city])
    df.rename(columns={'Unnamed: 0':'Id'}, inplace=True )

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        
        '''
        ALTERNATIVE METHOD
        USAGE: df['Start Time'].dt.month is used to create month column
        
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        '''
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

def drop_rows(df):
    """ 
    drop rows with missing values. 
    
    args: 
    df - the dataframe to drop rows from
    
    Returns:
    df - modified df with no NaN values
    """
    
    df.dropna(axis = 0, inplace=True)
    
    return df

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    
    Args:
        df - the dataframe to use for computing the statistics
        
    Returns:
        None
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    

    # display the most common month
    month = len(df['month'].unique()) > 1 
    if month:
        popular_month = df['month'].mode()[0]
        print('Most Popular Month: ', popular_month)
    else:
        print('Filter: month')
   
    # display the most common day of week
    day = len(df['day_of_week'].unique()) > 1
    if day:
        popular_day = df['day_of_week'].mode()[0]
        print('Most common weekday: ', popular_day)
    else:
        print('Filter: day')
    
    # display the most common start hour
    popular_hour = pd.Series(df['Start Time'].dt.hour).mode()[0]
    print('Most popular hour of the day: ', popular_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most common Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most common End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_start_end_station = pd.Series(df['Start Station']+ ' to ' + df['End Station']).mode()[0]
    print('Most common Start and End Station trip:', popular_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Trip Duration:',total_travel_time)

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print('Average Trip Duration:',average_travel_time)

    count = df['Trip Duration'].count()
    print('Count:',count)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Users:\n',df['User Type'].value_counts(),'\n')

    if 'Gender' in df.columns and 'Birth Year' in df.columns:
        # Display counts of gender
        print('Gender:\n',df['Gender'].value_counts(),'\n')

        # Display earliest, most recent, and most common year of birth
        df['Birth Year'] = df['Birth Year'].astype('int64')
        print('Earliest Birth year:\n',df['Birth Year'].sort_values().min(),'\n')

        print('Most Recent Birth Year:\n',df['Birth Year'].sort_values().max(),'\n')

        print('Most Common Birth Year:\n',df['Birth Year'].sort_values().mode()[0],'\n')
    else:
        print('The dataset has no \'Birth Year\' and \'Gender\' column.')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def view_raw_data(df):
    """ To display five lines of individual trip data """
    start_time = time.time()
    ans = input('Would you like to see first five individual trip data? Enter "yes" or "no"').lower()
    if ans=="yes":
        print('\nDisplaying individual trip data...\n')
    data_dict = df.to_dict(orient='records')
    count = 0
    index = 0
    while ans == 'yes' and index < len(data_dict):
        print('\nUser',index+1)
        print(data_dict[index],'\n')
        index += 1
        count += 1
        if count == 5:
            ans1 = input('Would you like to see the next five individual trip data? Enter "yes" or "no"').lower()
            if ans1 == 'no':
                break
            else:
                count = 0
                         
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
     
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        df = drop_rows(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()