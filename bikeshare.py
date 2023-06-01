import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze. Also allows user to view unfiltered raw data by city.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    check_cities = ['chicago', 'new york city', 'washington']
    check = True
    while check:
        try:
            city = str(input("Choose a city (chicago, new york city, washington): ")).lower()
            if city in check_cities:
                print('You chose {} as the city'.format(city))
                break 
            else:
                print('That is not a valid input')            
                return None                               
        except (TypeError, KeyboardInterrupt,KeyError):
            print('That is not a valid input')
            return None
                     
    # create dataframe based on city selection for raw data view.        
    dff = pd.read_csv(CITY_DATA[city])
    maxrows = len(dff.index)
    startr = 0  
    endr = 5  
    try:
        rawdata = str(input('would you like to see the raw data? Enter yes or no \n')).lower()
        if rawdata == 'yes':
            while startr < maxrows:    
                print(dff[startr:endr]) 
                startr += 5
                endr += 5
                moredata = str(input('would you like to see more raw data? \n')).lower() 
                if moredata != 'yes':
                    morefilter = str(input('would you like to continue? Enter yes or no \n')).lower()
                    if morefilter != 'yes':
                        return None                
                    break                                        
    except (TypeError, KeyboardInterrupt):
        print('That is not a valid input')
        return None

              
    # get user input for month (all, january, february, ... , june)
    check_months =['january', 'february', 'march', 'april', 'may', 'june'] 
    check_days =['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
      
    while check:
        try:
            filters = str(input('Would you like to filter the data by day, month, both or not at all? Enter "none" for no time filter \n')).lower()
            if filters == 'month':
                day = 'all'
                month = str(input('Which month - January, February, March, April, May, or June? \n')).lower()
                if month not in check_months:
                    return None
                else:
                    break    
            elif filters == 'day':
                month = 'all'
                day = str(input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? \n')).lower()
                if day not in check_days:
                    return None 
                else:
                    break   
            elif filters == 'both':
                month = str(input('Which month - January, February, March, April, May, or June? \n')).lower()
                day = str(input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? \n')).lower()                
                if month not in check_months and day not in check_months:
                    return None
                else:
                    break                                               
            elif filters in ('none','no','not','not at all'):
                print('proceding with no filter for month and day')
                month = 'all'
                day = 'all' 
                break                
            else:
                 print('This is not a valid input .....')
                 return None
                 check = False  
        except (TypeError, KeyboardInterrupt):
            print('That is not a valid input')
            return
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
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month']== month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']== day.title()]
    
    return df
    


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].value_counts().idxmax()
    print('most common month: ',common_month)

    # display the most common day of week
    common_dayofweek = df['day_of_week'].value_counts().idxmax()
    print('most common day of week: ',common_dayofweek)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour    
    common_hour = df['hour'].value_counts().idxmax()
    print('most common start hour: ',common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_startstation = df['Start Station'].value_counts().idxmax()
    print('most common start station: ',common_startstation)

    # display most commonly used end station
    common_endstation = df['End Station'].value_counts().idxmax()
    print('most common end station: ',common_endstation)
  
    # display most frequent combination of start station and end station trip
    common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    
    print('most frequent trip starts at {} and ends at {}'.format(common_trip[0], common_trip[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('total travel time: {} minutes'.format(total_travel_time))


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('average travel time: {} minutes'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print('counts of user by type \n {}'.format(user_types_count))

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('counts of user by gender \n {}'.format(gender_count))
    except (KeyError, TypeError):
        print('\nno gender data avalible \n')       

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].value_counts().idxmax()
    except (KeyError, TypeError):
        print('no birth data avalible \n') 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def main():
    while True: 
        # evaluate get_filters() function and only continue the program if the function returns valid value. 
        try:
            city, month, day = get_filters()  
        except:
            print('Exiting program. Goodbye. ')
            break 
                            
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)        


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
