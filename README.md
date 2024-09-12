# Система рекомендации музыкальных треков: создание и тестирование


## Клонирование репозитория

Для начала клонируем репозиторий проекта:

```
git clone git@github.com:spolivin/mle-project-sprint-4-v001.git
```

## Виртуальное окружение

Активируем окружение следующей серией команд:

```bash
sudo apt-get update
sudo apt-get install python3.10-venv
python3.10 -m venv .venv_recsys_app
source .venv_recsys_app/bin/activate
pip install --no-cache-dir -r requirements.txt
```
> NOTE: При возникновении ошибок на этапе установки библиотек в вирутальную среду может быть необходимо установить другие необходимые пакеты для среды Ubuntu командой `sudo apt-get install build-essential`.

## Подготовка к запуску микросервиса

Перед тем как запустить микросервис, необходимо сначала загрузить файлы с данными рекомендаций из *S3*. Файлы являются довольно тяжелыми, так что такой способ подготовки был выбран для избежания перегруженности репозитория без надобности.

Для загрузки всех необходимых для работы микросервиса файлов, можно запустить следующий скрипт:

```bash
python s3_scripts/prepare_datasets.py
```

После выполнения скрипта все требуемые данные будут загружены в директорию `data`.


Bucket name `s3-student-mle-20240523-34f645dbbf`

## Запуск микросервиса

Микросервис поделен на 4 модуля в папке `services`:

* [`recommendations_service.py`](service/recommendations_service.py) => Основное приложение, из которого запускается генерация рекомендаций всех типов 
* [`events_service.py`](service/events_service.py) => Сервис для добавления онлайн событий пользователю 
* [`features_service.py`](service/features_service.py) => Сервис для расчета онлайн рекомендаций, основанных на схожести треков
* [`recs_offline_service.py`](service/recs_offline_service.py) => Сервис для расчет офлайн рекомендаций
* [`constants.py`](service/constants.py) => Файл с основными константами, необходимыми для работы приложения.

Для запуска сервиса рекомендаций был подготовлен [единый скрипт](./run_service.py), который запускает каждый из приведенных выше сервисов по флагу `--service-name`: 

```bash
# Terminal window 1
python run_service.py --service-name=main_app
```
```bash
# Terminal window 2
python run_service.py --service-name=recs_store
```
```bash
# Terminal window 3
python run_service.py --service-name=features_store
```
```bash
# Terminal window 4
python run_service.py --service-name=events_store
```

После того как все сервисы успешно запустились (о чем будет свидетельствовать вывод в терминале об успешности запуска сервера), можно начать делать запросы к микросервису.

## Тестирования микросервиса

Тестирование сервиса можно запустить при помощи следующей команды:

```python
# Terminal window 5 (testing)
python test_service.py
```

## Стратегия смешивания рекомендаций

Как можно видеть в [коде основного приложения](service/recommendations_service.py), при наличии онлайн истории запускается смешивание онлайн и оффлайн рекомендаций. В данном случае ставим онлайн-рекомендации на нечетные места финального списка рекомендаций, а оффлайн - на четные.

## Остановка сервисов

По окончании работы сервисы можно остановить через `Ctrl+C` в каждом терминальном окне.
