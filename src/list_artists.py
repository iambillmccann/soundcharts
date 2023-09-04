import time
import utilities
import json
from database import Session, Artist, func

LIMIT = 2000

def main(limit):

    # exclude_uuids = [157, 255]

    # Start the session
    session = Session()

    # Perform the query
    artists = ( session.query(Artist)       
        .filter(func.JSON_LENGTH(Artist.artistData) == 0)
        # .filter(~Artist.uuid.in_(exclude_uuids))
        .limit(limit)
        .all()
    )

    # Close the session
    session.close()

    uuids = [artist.uuid for artist in artists]
    return { "uuid_list": uuids }


if __name__ == "__main__":

    print("\n-----------------------------------------------------------------------")
    print("Function: list_artist.py")

    start_time = time.time()
    content = main(LIMIT)
    stop_time = time.time()
    total_time = stop_time - start_time

    print("Execution time was " + utilities.format_milliseconds(total_time))
    print("-----------------------------------------------------------------------")

    json_result = json.dumps(content)
    print(json_result)
