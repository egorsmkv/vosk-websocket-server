# VOSK WebSocket Server для украинского языка

#### Зависимости

Операционная система: Linux x64, например, Ubuntu 20.04

Программы:

- Python 3.8
- pipenv (`pip install pipenv`)
- sox

Установка программ:

```
sudo apt-get install python3 python3-pip sox wget unzip

pip install pipenv
```

Установка зависимостей:

```bash
pipenv install
```

Активация окружения:

```bash
pipenv shell
```

### Загрузка модели VOSK

Загрузка украинской модели:

```
cd libs/ukr

wget https://alphacephei.com/vosk/models/vosk-model-uk-v3.zip
unzip vosk-model-uk-v3.zip

mv vosk-model-uk-v3 model/

rm vosk-model-uk-v3.zip
```

Дальше нужно зайти в файл `libs/ukr/model/conf/mfcc.conf` и в конце добавить:

```
--allow_upsample
```

### Запуск сервера VOSK

Запуск сервера для украинского языка:

```
export PYTHONPATH=$PYTHONPATH:$PWD

python3 ./scripts/vosk_server.py
```

### Запуск микрофона для тестирования распознавания

```
export PYTHONPATH=$PYTHONPATH:$PWD

python3 ./scripts/microphone.py
```
