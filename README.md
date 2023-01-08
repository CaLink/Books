Для запуска паука необходимо в корневой директории вызвать терминал и написать:
	scrapy crawl labirint -o Data/test.json -t jsonlines
		labirint - имя паука
		Data/test.json - место сохранения собранных данных
	
	DB Diagram - нагладное изображение БД
	db_scheme - скрипт для создания схемы БД (ms sql)

Решение (неполное):
	База данных:
		Взял за основу ms sql, потому что можно быстро и просто соединить с C#
		При создании БД старался придерживаться Третьей нормальной формы
		
		Во время создания и работы с парсерами были идеи о дополнении таблицы Book дополнительными полями: Издатель, Язык, Возрастные ограничения, Информация откуда была спаршена книга
		Но отсутствие многих параметров (иногда и изначальных) в карточках книг => нет смысла сейчас в этом шаге
	
	Парсеры:
		Использовал фреймворк scrapy для python
		
		Выбрал сайты Литрес, Лабиринт, для которых создал "пауков". Так же был рассмотрен Читай-Город
		(Одни из самых популярных сайтов как в городе, так и в стране)
		Хорошим бонусом было возможности поиска по ISBN на всех трех сайтах
		
		Литрес (имя паука "litress"):
			Во время изучения сайт приглянулся тем, что получилось найти часть его api. Оно позволило получать список книг в каком-то жанре.
			Ответ, получаемый от сайта, содержал список книг и частичную информацию о них, а так же ссылку на следующую "страницу" (та же ссылка, но с измененным параметром offset). Из этого ответа бралась ссылка на карточку книги, где уже собиралась основная информация о книге, т.к. в api были не все поля, необходимые для бд (из-за этого был создан другой вариант решения)
			Так же запрос позволяет исключить из выдачи аудиокниги
						
			На данный момент паук настроен на сбор информации в категории "Серьезное Чтиво" (201591)
			
		Лабиринт (имя паука "labirint"):
			Изучая сайт, не было найдено api проекта. Поэтому пришлось перебором идти по всем страницам. 
			Для этого паук идет на страницу "Все книги", где переходит по страницам, пока работает кнопка "следующая".
			Однако количество страниц ограничено 17-ю. При попытке перейти на 18, возвращался результат с 1-ой.
			Один из вариантов решения, который пришел в голову: перебор всех книг по id: 
				Можно найти id самой новой книги на сайте (на соответствующей вкладке). И в цикле от 1 до X перебирать все книги. Но на сайте имеется более 900000 товаров (если верить id'никам), книг из которых 250000. Из-за этой разницы от решения решил отказаться
			
			Ещё одной проблемой сайта стало нестабильное наличие некоторых свойств книги (жанры, страницы)
		
		Читай-Город:
			Здесь так же не было найдено api. Однако сайт обладает довольно простой структурой.
			Необходимо выбрать категорию (жанр), а дальше перебирать все книги, имеющиеся на текущей странице
			
		Так же был написан парсер для сайта ИграСлов
		
	Веб-приложение и api:
		К сожалению, эта часть сервиса не была реализована.
		Возникли вопросы по объединению всех частей проекта в единое целое, а так же возможность переноса всего сервиса

