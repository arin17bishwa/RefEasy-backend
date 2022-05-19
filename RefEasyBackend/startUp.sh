pip install -r requirements.txt
cp ../.env.example ../.env
sudo chmod +x loadData.sh
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata dump00.json
python manage.py runserver