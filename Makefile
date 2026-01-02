launch-ai:
	uvicorn ai.main:app --host 0.0.0.0 --port 6969 --reload

launch-compose:
	docker compose up --build