import json
import threading
import logging
import time
import os
import glob
import gevent

from locust import HttpUser, task, events, between
from locust.exception import StopUser

"""
To run, in cmd
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
    for file in glob.glob("payloads_1/*.json")
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
            # If all json are already used, stop vuser eventhough they will keep spawning 
            if DummyJsonUser.user_counter >= len(CASE_FILES):
                raise StopUser()
            #
            DummyJsonUser.user_counter += 1
            self.vuser_number = DummyJsonUser.user_counter

        # Allocate payload for vuser for the whole flow
        with open(
            f"payloads_1/vuser{self.vuser_number}.json",
            "r"
        ) as file:
            self.payload1 = json.load(file)

        with open(
            f"payloads_2/item{self.vuser_number}.json",
            "r"
        ) as file:
            self.payload2 = json.load(file)

        with open(
            f"payloads_3/recipe{self.vuser_number}.json",
            "r"
        ) as file:
            self.payload3 = json.load(file)

        #================================================================================
        #         
        # 
        # 
        # FIRST API HIT
        # 
        # 
        #================================================================================

        response = self.client.post(
            "/auth/login",
            json=self.payload1,
            name="1 - POST /auth/login"
        )

        logging.info(
            f"nth Vuser: {DummyJsonUser.user_counter} | "
            f"Payload: {self.payload1} | "
            f"Status: {response.status_code} | "
            f"Response: {response.text}"
        )

        gevent.sleep(3) # wait n seconds for the vuser

        #================================================================================
        #         
        # 
        # 
        # SECOND API HIT
        # 
        # 
        #================================================================================

        response = self.client.post(
            "/products/add",
            json=self.payload2,
            name="2 - POST /products/add"
        )

        logging.info(
            f"nth Vuser: {DummyJsonUser.user_counter} | "
            f"Payload: {self.payload2} | "
            f"Status: {response.status_code} | "
            f"Response: {response.text}"
        )

        gevent.sleep(3) # wait n seconds for the vuser

        #================================================================================
        #         
        # 
        # 
        # THIRD API HIT
        # 
        # 
        #================================================================================

        response = self.client.get(
            "/recipes/search",
            params=self.payload3,
            name="3 - GET /recipes/search?{param}"
        )

        logging.info(
            f"nth Vuser: {DummyJsonUser.user_counter} | "
            f"Payload: {self.payload3} | "
            f"Status: {response.status_code} | "
            f"Response: {response.text}"
        )
        
        time.sleep(150) #wait n seconds

        with DummyJsonUser.lock:
            DummyJsonUser.completed += 1

            if DummyJsonUser.completed == total_flow:

                threading.Thread(
                    target=self.wait_and_quit,
                    daemon=True
                ).start()

    def wait_and_quit(self):

        logger.info(
            "===== START WAITING FOR 1 MINUTES ====="
        )

        time.sleep(60 * 1)
    
        logger.info(
            "===== 1 MINUTES FINISHED ====="
        )
    
        logger.info(
            "===== QUITTING LOCUST ====="
        )
    
        self.environment.runner.stop()


