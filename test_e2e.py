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

MSG_TEMP = "Неожиданное значение поля '{}'"

def assert_data(data, data_dict, key_name):
    assert data[key_name] == data_dict[key_name], MSG_TEMP.format(key_name)

class TestBooker:
    def test_e2e(self):
        booker = BookerApi(BASE_URL)
        booker.login()
        print(f"\n[1] Токен получен: {booker.auth_token[:10]}...")

        booking_id = booker.create_booking(BOOKING_DATA)
        print(f"[2] Бронь создана. ID: {booking_id}")

        data = booker.get_booking(booking_id)
        assert_data(data, BOOKING_DATA, "firstname")
        assert_data(data, BOOKING_DATA, "lastname")
        assert_data(data, BOOKING_DATA, "totalprice")
        validate(instance=data, schema=BOOKING_SCHEMA)
        print(f"[3] Бронь получена и схема валидна: {data}")

        data = booker.update_booking(booking_id, UPDATED_DATA)
        assert_data(data, UPDATED_DATA, "firstname")
        print(f"[4] PUT выполнен: {data}")

        data = booker.get_booking(booking_id)
        assert_data(data, UPDATED_DATA, "firstname")
        assert_data(data, UPDATED_DATA, "lastname")
        print(f"[5] Данные после PUT подтверждены ✓")

        new_price = 200
        data = booker.partial_update_booking(booking_id, {"totalprice": new_price})
        assert data["totalprice"] == new_price
        assert_data(data, UPDATED_DATA, "firstname")
        print(f"[6] PATCH выполнен: totalprice={data['totalprice']} ✓")

        booker.delete_booking(booking_id)
        print(f"[7] Бронь удалена (201) ✓")

        booker.check_deleted(booking_id)
        print(f"[8] Проверка удаления (404) ✓")

        booker.close()