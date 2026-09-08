import json
import threading
import logging
import time
import os
import glob

from locust import HttpUser, task, events, between
from locust.exception import StopUser

"""
locust -f dummyjson.py -u 10 -r 0.1 --html=dummyjson_result.html > dummyjson.log 2>&1
"""

total_flow = 10

logging.basicConfig(
    filename="dummyjson_placeholder.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Store A list of folder inside folder named payloads
CASE_FILES = [
    file
    for file in glob.glob("payloads/*.json")
]

# To allocate json, and handle race condition
case_counter = 0
case_lock = threading.Lock()

class DummyJsonUser(HttpUser):
    host = "https://dummyjson.com"

    global case_counter

    user_counter = 0
    completed = 0
    lock = threading.Lock()

    @task
    def login(self):
        with DummyJsonUser.lock:
            #If all json are already used, stop vuser eventhough they will keep spawning 
            if DummyJsonUser.user_counter >= len(CASE_FILES):
                raise StopUser()
            #
            DummyJsonUser.user_counter += 1
            self.vuser_number = DummyJsonUser.user_counter
    
        with open(
            f"payloads/vuser{self.vuser_number}.json",
            "r"
        ) as file:
            self.payload = json.load(file)

        response = self.client.post(
            "/auth/login",
            json=self.payload,
            name="POST /auth/login"
        )

        logging.info(
            f"nth Vuser: {DummyJsonUser.user_counter} | "
            f"Payload: {self.payload} | "
            f"Status: {response.status_code} | "
            f"Response: {response.text}"
        )

        time.sleep(125) #wait n seconds

        with DummyJsonUser.lock:
            DummyJsonUser.completed += 1

            if DummyJsonUser.completed == total_flow:

                threading.Thread(
                    target=self.wait_and_quit,
                    daemon=True
                ).start()

    def wait_and_quit(self):
    
        time.sleep(60 * 3)
    
        logger.info(
            "===== 3 MINUTES FINISHED ====="
        )
    
        logger.info(
            "===== QUITTING LOCUST ====="
        )
    
        self.environment.runner.quit()


