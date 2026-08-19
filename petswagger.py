from locust import HttpUser, task, between

class PetStoreUser(HttpUser):
    host = "https://petstore.swagger.io/v2"

    wait_time = between(1, 3)

    @task
    def get_pet(self):
        headers = {
            "Content-Type": "application/json"
        }

        with self.client.get("/pet/1", headers=headers, catch_response=True) as response:

            if response.status_code == 200:
                response.success()
                print("Body:", response.text)
            else:
                print(f"Expected 200, got {response.status_code}")
                response.failure(f"Expected 200, got {response.status_code}")

    @task
    def find_pet_by_status(self):
        headers = {
            "Content-Type": "application/json"
        }

        with self.client.get("/pet/findByStatus?status=sold", headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                print("Body:", response.text)
            else:
                print(f"Expected 200, got {response.status_code}")
                response.failure(f"Expected 200, got {response.status_code}")

    @task
    def returns_pet_inventories_by_status(self):
        headers = {
            "Content-Type": "application/json"
        }

        with self.client.get("/store/inventory", headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                print("Body:", response.text)
            else:
                print(f"Expected 200, got {response.status_code}")
                response.failure(f"Expected 200, got {response.status_code}")