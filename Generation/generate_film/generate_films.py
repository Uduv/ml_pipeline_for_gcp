from faker import Faker
from faker.providers import BaseProvider
import random
import csv
import time
import progressbar
from datetime import datetime
import os


# Add new Faker provider
class GenereProvider(BaseProvider):
    def movie_genre(self):
        return random.choice(['Documentary', 'Thriller', 'Mystery', 'Horror', 'Action', 'Comedy', 'Drama', 'Romance'])

class LanguageProvider(BaseProvider):
    def language(self):
        return random.choice(['English', 'Chinese', 'Italian', 'Spanish', 'Hindi', 'Japanese'])

fake = Faker()

fake.add_provider(GenereProvider)
fake.add_provider(LanguageProvider)


class generate_film : 
    def __init__(self):
        self.film = [self.get_movie_name(), fake.movie_genre(), self.get_movie_date(), self.get_movie_len(), self.get_movie_rating(), fake.language()]

    def __iter__(self) :
        return iter(self.film)


    def capitalize(self,str):
        return str.capitalize()

    def get_movie_name(self):
        words = fake.words()
        capitalized_words = list(map(self.capitalize, words))
        return ' '.join(capitalized_words)

    def get_movie_date(self):
        return datetime.strftime(fake.date_time_this_decade(), "%B %d, %Y")

    def get_movie_len(self):
        return random.randrange(50, 150)

    def get_movie_rating(self):
        return round(random.uniform(1.0, 5.0), 1)

    def get_autor(self) :
        return fake.first_name() + fake.last_name()

rows_number = 1e7



bar = progressbar.ProgressBar(maxval=int(rows_number))

file_names = 'movie_data_' + str(rows_number) + '_rows_' + str(datetime.now().strftime("%Hh%Mm%Ss") ) + '.csv'
path = str('Generation/data/unnamed/' + file_names)

print(path)




if __name__ == '__main__' : 
    start_time = time.time()

    bar.start()
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Genre', 'Premiere', 'Runtime', 'Rating Score', 'Language'])
        for row in range(int(rows_number)) :
            writer.writerow(generate_film())
            bar.update(row)
    bar.finish()
    print("--- %s seconds ---" % (time.time() - start_time))

