1. Install FastAPI and Uvicorn packages:
pip install fastapi
pip install "uvicorn[standard]"

2. To run the Uvicorn server:
python -m uvicorn <filename>:<App-object> --reload

3. To get the Swagger UI docs for each created API, enter the following URL:
127.0.0.1:8000/docs

or

127.0.0.1:8000/redoc