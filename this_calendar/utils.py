from datetime import date, timedelta
from calendar import monthrange


DAY_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] 


def get_today():
    return date.today()


# Get this month 
def get_month():
    
    pass


def generate_month_dates(this_date,  first_day_is_monday, num_days=35):
    """
        Generate a list of dates with length of num_days.
        It envelops this_date's month,
        + padding with previous and next month dates.

        @param this_date: The date to generate the month around.
        @param num_days: The total number of days to generate.
        @param first_day_is_monday: If True, the week starts on Monday.
        @return: A list of date objects.
    """
    
    first_day_of_month = date(this_date.year, this_date.month, 1)
    last_day_num = monthrange(this_date.year, this_date.month)[1]
    last_day_of_month = date(this_date.year, this_date.month, last_day_num) 

    # --- Get padding for previous ---  
    def get_padding_to_week_start(this_date, first_day_is_monday):
        weekday = this_date.weekday()
        return weekday if first_day_is_monday else (weekday + 1) % 7
    def get_padding_to_week_end(this_date, first_day_is_monday):
        weekday = this_date.weekday()
        return 6 - weekday if first_day_is_monday else (6 - ((weekday + 1) % 7))
    
    padding_to_week_start = get_padding_to_week_start(first_day_of_month, first_day_is_monday)
    padding_to_week_end = get_padding_to_week_end(last_day_of_month, first_day_is_monday)

    # Dates for padding before the month
    start_padding_dates = [
        first_day_of_month - timedelta(days=padding_to_week_start - i)
        for i in range(padding_to_week_start)
    ] if padding_to_week_start > 0 else []

    # Dates for the full month
    month_dates = [
        date(this_date.year, this_date.month, day)
        for day in range(1, last_day_num + 1)
    ]

    # Dates for padding after the month
    end_padding_dates = [
        last_day_of_month + timedelta(days=i + 1)
        for i in range(padding_to_week_end)
    ] if padding_to_week_end > 0 else []

    all_dates = start_padding_dates + month_dates + end_padding_dates
    
    # If it's February and not enough dates, keep adding from next month 
    while len(all_dates) < num_days:
        last_date = all_dates[-1]
        all_dates.append(last_date + timedelta(days=1))

    return all_dates




# ----------------------------------------------------
def main():
    today = get_today()

    today= date(2025, 2, 1) # DEBUG
    first_day_is_monday = False  # DEBUG

    formatted_date = today.strftime("%A, %B %d, %Y")
    print("Today's formatted date:", formatted_date)
    
    this = generate_month_dates(today, first_day_is_monday, 35)
    print(len(this))
    print(this)

if __name__ == "__main__":
    main()