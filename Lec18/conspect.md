## Лекция 18. Перенос на ngrok

```ngrok``` - тоннельная утилита, которая позволяет пробивать удаленный хост, который в то же время будет связан с каким-то портом на локальной машине.

* Регистрируемся :https://dashboard.ngrok.com/get-started/setup
* Скачиваем утилиту
* Настриваем командой ```ngrok authtoken <token>
* Запускаем сконнекченные поры ```ngrok http 8000``` (при условии что приложение тоже запущено на порте 8000)