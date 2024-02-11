from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    host = "http://localhost:1980"

    @task
    def hello_world(self):
        self.client.get("/getall/artists?start=0&limit=50&sortby=created_date&reverse=1")
