from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    host = "http://localhost:1980"

    # @task
    # def get_all_artists(self):
    #     self.client.get(
    #         "/getall/artists?start=0&limit=50&sortby=created_date&reverse=1"
    #     )

    @task
    def get_album_info(self):
        self.client.get("/artist/9e6781427eab4934")
