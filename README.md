# merch-table-tool
Tracks item sales in Excel sheet across multiple vendors.
Users add sellers and items then use a dynamic form to record sales in Excel sheet.

![App Dashboard](https://user-images.githubusercontent.com/22055182/267450921-81c86501-4334-4c28-97d6-9a6fbfa65845.png)

![App Dashboard](https://user-images.githubusercontent.com/22055182/267450925-1f0c07fa-530f-4e2b-a58e-efff8fb3a941.png)

![App Dashboard](https://user-images.githubusercontent.com/22055182/267450928-47ac67a9-ecb7-4105-8a9c-7f1f36ea6c20.png)

![App Dashboard](https://user-images.githubusercontent.com/22055182/267450930-b0af7f42-ea5f-42e6-83fe-74e4f2cc9ea9.png)

![App Dashboard](https://user-images.githubusercontent.com/22055182/267450932-e6a5dd93-0e07-425f-8e2f-4e8ec855e27c.png)

Made in Django

Developed in venv
Created .env file for environment variables
.env has APP_ENV=development and SECRET_KEY="adjangosecret"

Dependencies are installed with:
pip install -r requirements.txt

SQLite DB is created with:
python manage.py makemigrations
python manage.py migrate

Server is run with:
python manage.py runserver