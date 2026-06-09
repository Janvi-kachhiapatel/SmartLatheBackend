from collector import collect_live_data
from db_service import save_snapshot
import time
import cache

def background_logger():

    while True:
        try:
            data = collect_live_data()

            cache.latest_data = data

            save_snapshot(data)

            print("DATA UPDATED")

        except Exception as e:
            print("LOGGER ERROR =", e)

        time.sleep(2)