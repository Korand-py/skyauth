<div align="center">

  <img src="assets\icon_app.png" width="100" alt="SkyAuth Shield"/>
  
  <h1>SkyAuth <span style="color:#2485F4">Beta 2.0</span></h1>

  <p><strong>Простое Android приложение для генерации OTP-кодов (2FA)</strong><br>
  Аналог Google Authenticator, который работает <strong>без интернета</strong> и не требует регистрации.</p>

  <br>
  
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flet-0.82%2B-FF4B4B?style=for-the-badge&logo=flet&logoColor=white"/>
  <img src="https://img.shields.io/badge/PyOTP-2FA-blueviolet?style=for-the-badge"/>

  <br><br>
  > [!WARNING]
> Перед обновлением скачайте ваши OTP ключи и сохраните их, после обновления записи удаляются

  <br><br>
  **Все ключи хранятся только на вашем устройстве. Никакой регистрации, рекламы и слежки.**

</div>

---

### ✨ Основные возможности

- Офлайн-режим (работает без интернета)
- Поддержка TOTP (стандарт 2FA)
- Скрытие кодов
- Закрепление карточек
- Простой и красивый интерфейс

---

### Скриншоты проекта

<p align="center">
  <img src="assets/foto.png" width="600" alt="Главный экран"/>
  
</p>

---

## Как запустить?

### Windows 💻
 
Распакуйте архив и запустите `main.py`

Виртуальное пространство (.venv)
```python
.venv\Scripts\activate.bat
```

### Android 📱

**Способ 1:**  
Установите `skyauth-android.apk`

**Способ 2 (через Flet):**  
```python
flet build apk
```
## Стуктура проекта
📁 Korand-py<br>
├── 📁 assets/               # изображения проекта<br>
├── 📄 LICENSE.md            # Лицензия<br>
├── 📄 README.md             # Описание проекта и инструкция<br>
├── 📄 keys.json             # Файл с 2FA ключами<br>
├── 🐍 main.py               # Основной скрипт проекта<br>
├── 📄 pyproject.toml        # Конфигурация проекта<br>
├── 📄 readme.md             # Дополнительный README (если нужен)<br>
└── 📄 requirements.txt      # Зависимости проекта (pip)<br>


## Лицензия

Проект распространяется под **SlySquad Non-Commercial License v1.0**.

Коммерческое использование **запрещено**.  
Подробности — в файле [LICENSE](LICENSE.md).
