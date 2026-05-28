import allure
import json
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


@allure.epic("Restful Booker API")
@allure.feature("Бронирование")
class TestBooker:

    @allure.story("E2E сценарий бронирования")
    @allure.title("Полный цикл: создание, обновление и удаление брони")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
    Тест проверяет полный E2E цикл работы с бронированием:
    - Авторизация и получение токена
    - Создание новой брони
    - Получение и валидация брони по схеме
    - Полное обновление брони (PUT)
    - Частичное обновление брони (PATCH)
    - Удаление брони
    - Проверка что бронь удалена (404)
    """)
    def test_e2e(self):
        booker = BookerApi(BASE_URL)

        with allure.step("1. Авторизация"):
            booker.login()
            allure.attach(
                f"Токен: {booker.auth_token[:10]}...",
                name="Auth Token",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("2. Создание брони"):
            booking_id = booker.create_booking(BOOKING_DATA)
            allure.attach(
                json.dumps(BOOKING_DATA, indent=2, ensure_ascii=False),
                name="Данные брони",
                attachment_type=allure.attachment_type.JSON
            )
            allure.attach(
                str(booking_id),
                name="ID брони",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("3. Получение и валидация брони"):
            data = booker.get_booking(booking_id)
            assert_data(data, BOOKING_DATA, "firstname")
            assert_data(data, BOOKING_DATA, "lastname")
            assert_data(data, BOOKING_DATA, "totalprice")
            validate(instance=data, schema=BOOKING_SCHEMA)
            allure.attach(
                json.dumps(data, indent=2, ensure_ascii=False),
                name="Ответ GET",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("4. Полное обновление брони (PUT)"):
            data = booker.update_booking(booking_id, UPDATED_DATA)
            assert_data(data, UPDATED_DATA, "firstname")
            allure.attach(
                json.dumps(UPDATED_DATA, indent=2, ensure_ascii=False),
                name="Данные для обновления",
                attachment_type=allure.attachment_type.JSON
            )
            allure.attach(
                json.dumps(data, indent=2, ensure_ascii=False),
                name="Ответ PUT",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("5. Проверка данных после PUT"):
            data = booker.get_booking(booking_id)
            assert_data(data, UPDATED_DATA, "firstname")
            assert_data(data, UPDATED_DATA, "lastname")

        with allure.step("6. Частичное обновление цены (PATCH)"):
            new_price = 200
            data = booker.partial_update_booking(booking_id, {"totalprice": new_price})
            assert data["totalprice"] == new_price
            assert_data(data, UPDATED_DATA, "firstname")
            allure.attach(
                json.dumps(data, indent=2, ensure_ascii=False),
                name="Ответ PATCH",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("7. Удаление брони"):
            booker.delete_booking(booking_id)

        with allure.step("8. Проверка удаления (ожидаем 404)"):
            booker.check_deleted(booking_id)

        booker.close()