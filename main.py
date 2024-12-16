from api.db import Database
from api.quiz_api import QuizAPI

if __name__ == '__main__':
    api = QuizAPI()
    cities = api.cities()
    print(cities)
    with Database() as db:
        for city in cities['data']['data']:
            print(city['id'], city['title'], city['map_type'])
            db.update_cities(city['id'], city['title'], city['map_type'])
