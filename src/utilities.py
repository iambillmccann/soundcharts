import math
import csv

from os import system, name, path

DATA_FOLDER = "./data/"

def format_milliseconds(total_time):
    """
    Format a python time value into HH:MM:SS:mmm
    Python time values are total second in a float. The decimal
    portion of the float is the fraction of a second.

    Args:
       total_time   The amount of time to format

    Returns:
        A string formatted as HH:MM:SS:mmm
    """

    milliseconds = math.floor(total_time % 1 * 1000)
    total_seconds = math.floor(total_time)
    total_minutes = math.floor(total_seconds / 60)
    seconds = int(math.floor(total_seconds % 60))
    minutes = int(math.floor(total_minutes % 60))
    hours = int(math.floor(total_minutes / 60))

    format_milliseconds = str(milliseconds)
    format_seconds = str(seconds)
    format_minutes = str(minutes)
    format_hours = str(hours)

    if milliseconds < 1: format_milliseconds = '000'
    elif milliseconds < 10: format_milliseconds = '00' + format_milliseconds
    elif milliseconds < 100: format_milliseconds = '0' + format_milliseconds

    if seconds < 10: format_seconds = '0' + format_seconds
    if minutes < 10: format_minutes = '0' + format_minutes
    if hours < 10: format_hours = '0' + format_hours

    return '{}:{}:{}.{}'.format(format_hours, format_minutes, format_seconds, format_milliseconds)

def save_data(data, file_name, file_disposition="w"):
    """ Save the data into a csv file

    Args:
        data         A list containing the items to save
        file_name    The name of the file to contain the data
    Returns:
        Nothing
    """

    fields = [
        "uuid",
        "slug",
        "name"
    ]

    with open(DATA_FOLDER + file_name, file_disposition) as file:
        write = csv.writer(file)
        if file_disposition == "w": write.writerow(fields)
        for item in data:
            write.writerow(item)

def take_checkpoint(url, file_name, file_disposition="w"):
    """ Save the url to a checkpoint file

    Args:
        url          The url to save
        file_name    The name of the file to contain the url
    Returns:
        Nothing
    """

    with open(DATA_FOLDER + file_name, file_disposition) as file:
        write = csv.writer(file)
        write.writerow([url])