### Общее:
* **LATER** Перемещение участников, по которым уже получена оценка в конец списка??? (mashup)
      Комм.: на ванильном js это будет непросто,
      предлагаю в последнюю очередь делать если прям скажут что необходимо
* **LATER** Реализовать аутентификацию приложения самостоятельно (вместо пункта выше):
       Приложение QS отдаёт секретную переменную в mashup только пользователям
       из белого списка SectionAccess, которую mashup отправляет каждый раз при
       записи данных на AKU5, в скрипте AKU5 реализовать проверку хэша этой
       секретной переменной на соответствие хранимому хэшу, заранее
       вычисленному (QS, mashup, AKU5)
       Волнует стабильность использования переменной, можно хранить в кэше браузера
* **LATER** Реализовать хранение переменной для создания пароля к итоговому файлу excel на QS, дополнить параметры функции вызова скрипта AKU5 для сохранения итога, реализовать скрипт AKU5 с сохранением запароленного excel (QS, mashup, AKU5)
       Комм.: нереализуемо с текущим набором библиотек AKU5 (11.08.2024)

### AKU5:
* **LATER** Проверить возможность ограничения вызова скрипта на АКУ5 одним приложением QS, вопрос к ОРЦД
* Перенести использование публичного ключа в метод записи данных
* Вынести дефолтные ключи из класса (протестировать)
* Обработка ошибок использования несоответствующего приватного ключа rsa (InvalidKey)
* Убрать сохранение длины ключа fernet в файл с данными
* **LATER** Использовать подпись rsa ключом?
* **LATER** По возможности добавить ранжирование результатов участников по сумме
