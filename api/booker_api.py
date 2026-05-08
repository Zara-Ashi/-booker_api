from api.base_book_api import BaseBookApi
from data.booking_url_api import BOOKING
from data.booking_url_api import BOOKING, NOT_FOUND

class BookerApi(BaseBookApi):
    def __init__(self, base_url: str):
        super().__init__(base_url)

    def create_booking(self, booking_data: dict):
        response = self.post(BOOKING, booking_data)
        return response["bookingid"]

    def get_booking(self, booking_id: int):
        return self.get(f"{BOOKING}/{booking_id}")

    def update_booking(self, booking_id: int, booking_data: dict):
        return self.put(f"{BOOKING}/{booking_id}", booking_data)

    def partial_update_booking(self, booking_id: int, booking_data: dict):
        return self.patch(f"{BOOKING}/{booking_id}", booking_data)

    def delete_booking(self, booking_id: int):
        self.delete(f"{BOOKING}/{booking_id}")

    def check_deleted(self, booking_id: int):
        response = self.session.get(self._url(f"{BOOKING}/{booking_id}"))
        self._check_status(response.status_code, NOT_FOUND)

    def assert_field(self, data: dict, field: str, expected):
        assert data[field] == expected, f"Ожидали {field}={expected}, получили {data[field]}"