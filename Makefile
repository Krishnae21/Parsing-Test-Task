start_app:
	python3.12 main.py

init_shell:
	pyenv install -s 3.12 && pyenv shell 3.12 && poetry env use python3.12 && poetry shell

copy_env:
	cp example.env .env

build_d:
	docker build -t task_gorbunov .

run_d:
	docker run task_gorbunov:latest
