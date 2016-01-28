.PHONY: server
server:
	@python manage.py runserver

.PHONY: shell
shell:
	@python manage.py shell

.PHONY: tests
tests:
	@py.test

.PHONY: cov
cov:
	@py.test --cov bookmarks/ --cov-report=term-missing
