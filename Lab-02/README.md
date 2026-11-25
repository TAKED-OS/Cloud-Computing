# Лабораторная работа №2. Amazon EC2

Архивный отчёт содержит задания 1–14 и исходные скриншоты. В заголовке архива стоит №4, а в Moodle эта работа по Amazon EC2 проходит под №2. Ниже приведены дополнения к заданиям 11 и 13.

[Архивный отчёт и скриншоты](https://github.com/cloudstudent-cloud/timecapsule/blob/539e40125cf9ea1f2d0273d3663858579a3c173b/README.md) · [Задание Moodle](https://elearning.usm.md/mod/assign/view.php?id=315493)

## Задание 11. Проверка nginx

На исходном учебном EC2 выполнил `sudo nginx -t`. Команда завершилась с кодом 0.

```text
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

Результат сохранён как текстовый вывод SSH. По завершении проверки EC2 остановлен. AWS подтвердил, что правила группы безопасности и параметры тома совпали с исходными.

## Задание 13. Откат приложения

При исходном эксперименте длительность простоя не замерял. В основном отчёте сохранены HTTP 500 и восстановление после отката.
