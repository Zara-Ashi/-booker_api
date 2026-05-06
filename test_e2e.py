from jsonschema import validate
from api.booker_api import BookerApi
from data.booking_url_api import BASE_URL
from data.booking_data_api import BOOKING_DATA, UPDATED_DATA

BOOKING_SCHEMA = {
    "type": "object",
    "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
    "properties": {
        "firstname":    {"type": "string"},
        "lastname":     {"type": "string"},
        "totalprice":   {"type": "number"},
        "depositpaid":  {"type": "boolean"},
        "bookingdates": {
            "type": "object",
            "required": ["checkin", "checkout"],
            "properties": {
                "checkin":  {"type": "string"},
                "checkout": {"type": "string"}
            }
        }
    }
}

class TestBooker:
    from jsonschema import validate
    from api.booker_api import BookerApi
    from data.booking_url_api import BASE_URL
    from data.booking_data_api import BOOKING_DATA, UPDATED_DATA

    BOOKING_SCHEMA = {
        "type": "object",
        "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
        "properties": {
            "firstname": {"type": "string"},
            "lastname": {"type": "string"},
            "totalprice": {"type": "number"},
            "depositpaid": {"type": "boolean"},
            "bookingdates": {
                "type": "object",
                "required": ["checkin", "checkout"],
                "properties": {
                    "checkin": {"type": "string"},
                    "checkout": {"type": "string"}
                }
            }
        }
    }

    class TestBooker:
        def test_e2e(self):
            booker = BookerApi(BASE_URL)
            booker.login()
            print(f"\n[1] Токен получен: {booker.auth_token[:10]}...")

            booking_id = booker.create_booking(BOOKING_DATA)
            print(f"[2] Бронь создана. ID: {booking_id}")

            data = booker.get_booking(booking_id)
            assert data["firstname"] == BOOKING_DATA["firstname"]
            assert data["lastname"] == BOOKING_DATA["lastname"]
            assert data["totalprice"] == BOOKING_DATA["totalprice"]
            validate(instance=data, schema=BOOKING_SCHEMA)
            print(f"[3] Бронь получена и схема валидна: {data}")

            data = booker.update_booking(booking_id, UPDATED_DATA)
            assert data["firstname"] == UPDATED_DATA["firstname"]
            print(f"[4] PUT выполнен: {data}")

            data = booker.get_booking(booking_id)
            assert data["firstname"] == UPDATED_DATA["firstname"]
            assert data["lastname"] == UPDATED_DATA["lastname"]
            print(f"[5] Данные после PUT подтверждены ✓")

            data = booker.partial_update_booking(booking_id, {"totalprice": 200})
            assert data["totalprice"] == 200
            assert data["firstname"] == UPDATED_DATA["firstname"]
            print(f"[6] PATCH выполнен: totalprice={data['totalprice']} ✓")

            booker.delete_booking(booking_id)
            print(f"[7] Бронь удалена (201) ✓")

            booker.check_deleted(booking_id)
            print(f"[8] Проверка удаления (404) ✓")

            booker.close()