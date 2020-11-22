# Scooby

1. Clone the repository.
```
git clone https://github.com/choch-o/Scooby.git
```
2. Make a virtual environment.
3. Create `db` directory under the root directory `Scooby` and set permissions
```
# In Scooby
virtualenv venv --python=python3.8
source venv/bin/activate
mkdir db
sudo chmod a+w db
```

Copy .env files.
```
cp backend_env scooby_backend/.env
cp frontend_env scooby_frontend/.env
```
## Backend
Go to `Scooby/scooby_backend` and install Python packages.
```
cd scooby_backend
pip install -r requirements.txt
```

In `Scooby/scooby_backend`, perform migrations
```
python manage.py makemigrations
python manage.py migrate
```
Run the server.
```
python manage.py runserver 0.0.0.0:8000
```
Check that your server is running in browser `localhost:8000`.
Test if writing to database works well by posting something in `localhost:8000/api/posts`.

## Frontend
Go to `Scooby/scooby_frontends` and install npm/yarn packages.
```
cd scooby_frontend
yarn install
```
Run the development server.
```
yarn start
```

Check that your frontend code is running in browser `localhost:3000`.
Test if the sample post you wrote in the Backend step appears on the page.
