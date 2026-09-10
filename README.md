# Практическая работа №4

## Вариант 3. Мокирование системного времени и переменных окружения

Проект демонстрирует модульное тестирование `TokenService`, который:

- генерирует временный токен в формате `base64(user_id:expiry_timestamp)`;
- получает срок жизни токена из переменной окружения `TOKEN_LIFETIME_SEC`;
- проверяет формат токена и сравнивает срок действия с текущим временем.

В тестах замокированы `src.service.time.time` и `src.service.os.getenv`.
Реальное системное время и окружение операционной системы не используются.

## Требования

- Python 3.8 и новее;
- `pip`.

## Установка и запуск

### Windows

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest tests -v
```

### Linux/macOS

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest tests -v
```

## Структура проекта

```text
src/service.py       реализация TokenService
tests/test_service.py модульные тесты с unittest.mock
report.md            краткий отчёт по работе
```

## Результат

Набор тестов проверяет:

1. генерацию токена при фиксированных времени и окружении;
2. валидность токена сразу после генерации;
3. валидность до истечения срока;
4. невалидность в момент истечения срока;
5. поведение при `TOKEN_LIFETIME_SEC=10` и `TOKEN_LIFETIME_SEC=60`;
6. битый base64 и другие ошибочные форматы;
7. неправильный формат токена.