import requests
import random


def create_job_posts(i):
    url = "http://127.0.0.1:8000/api/jobs/"
    title = f"J{random.randint(1, 99):02}"
    description = f"D{i:02}"
    dept = random.choice(['HR', 'ITS', 'FIN', 'ENG'])
    loc = random.choice(['IN-BAN', 'US-TXS', 'KR-SEO'])
    pos = random.choice(['INT', 'FTE'])
    is_open=random.choice([True,False])
    payload = {'title': title,
               'department': dept,
               'location': loc,
               'position_type': pos,
               'description': description,
               'is_open':is_open}
    files = [

    ]
    token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUzNzMzNDg1LCJpYXQiOjE2NTMxMjg2ODUsImp0aSI6IjMwOTI3YmM4ZDJlMzRiMDFiNGZiMDIyMGI1Y2FiNTQ0IiwidXNlcl9pZCI6NH0.JkjbRCUCxeoI4FizVkJb4MNuUDnAd_57XaAY0sfi59Y"
    headers = {
        'Authorization': 'Bearer '+token
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)


def register_users(i):
    url = "http://127.0.0.1:8000/api/user/register/"
    domains=['btech.nitdgp.ac.in','gmail.com','hmail.com','outlook.com']
    x=random.randint(1,1000)
    email=f"{x:04}@{random.choice(domains)}"
    first_name=str(x)
    payload = {'email': email,
               'first_name': first_name,
               'password': 'qwert@123',
               'password2': 'qwert@123'}
    files = [

    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)


def main():
    for i in range(0, 50):
        register_users(i)


if __name__ == '__main__':
    main()
