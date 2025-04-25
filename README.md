### TODO

По хорошему найти на сайте чё за куки используются и правильные подсовывать чтоб не банили, нормальные прокси прописать.

## В качестве менеджера завимостей используется uv.

## Установка зависимостей
```
uv sync
```

## Запуск
```
uv run scrapy crawl spider_name -O result.json
```

Запуск с указанием пути до файла с ссылками

```
uv run scrapy crawl spider_name -O result.json -a filename=<path/to/urls.txt>
```

Запуск с указанием ссылок. В качестве разделителя- запятая

```
uv run scrapy crawl spider_name -O result.json -a urls="https://alkoteka.com/catalog/slaboalkogolnye-napitki-2,https://alkoteka.com/catalog/krepkiy-alkogol,https://alkoteka.com/catalog/vino" 
```

Запуск с указанием города

```
uv run scrapy crawl spider_name -O result.json -a city=Мухосранск
```