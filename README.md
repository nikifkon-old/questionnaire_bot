ТЗ: [here](https://pastebin.com/KyEpdNUg)
Tables:
- Houses
    - id
    - area
    - street
    - house number

- Users:
    - id
    - houes_id
    - name
    - phone
    - flat (optional)

- Events (аварии, отключения, плановые и внеплановые работы)
    - id
    - type: "emergency", "scheduled work", "unscheduled work", "ads"
    - description (optional)
    - start
    - end
    - house_id (optional)
    - area (optional)
    - target: "house", "area", "all"


[x] deep link to get house info (глубокие ссылки с информацией о доме)
    - deep link data (информация в глубокой ссылке):
        - area (район)
        - street (улица)
        - house_number (номер дома)
        - telegram support only latin, so use transliterate https://github.com/barseghyanartur/transliterate
    - https://t.me/simple_questionnaire_1_bot?start=123_Lenina_Leninskij
[] dont write house info if it's right
[] edit profile
[] inline keyboard
[] fast api
    - [] endpoint for create events
    - [] deploy on heroku

Этапы разработки проекта:
[x] проектирование БД и создание скрипта генерации БД на сервере;
[] разработка модуля генерации QR-кодов;
[] разработка модуля анкетирования;
[] разработка модуля интерактивного справочника;
[] разработка модуля опросов и голосований;
[] разработка модуля информирования пользователей о плановых и внеплановых работах, отключениях и авариях;
[] разработка модуля рассылка рекламы товаров и услуг.


Plot (сценарий):
/start -> register_user -> 