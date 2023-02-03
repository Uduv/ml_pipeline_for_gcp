from faker import Faker
from faker.providers import BaseProvider
import random
import csv
from multiprocessing import Pool
import time
from datetime import datetime

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



def generate(arg):
    return [get_movie_name(), fake.movie_genre(), get_movie_date(), get_movie_len(), get_movie_rating(), fake.language()]

def capitalize(str):
    return str.capitalize()

def get_movie_name():
    words = fake.words()
    capitalized_words = list(map(capitalize, words))
    return ' '.join(capitalized_words)

def get_movie_date():
    return datetime.strftime(fake.date_time_this_decade(), "%B %d, %Y")

def get_movie_len():
    return random.randrange(50, 150)

def get_movie_rating():
    return round(random.uniform(1.0, 5.0), 1)






rows_number = 5e6

file_names = 'movie_data_parralize_' + str(rows_number) + '_rows_' + str(datetime.now().strftime("%Hh%Mm%Ss") ) + '.csv'
path = str('Generation/data/unnamed/' + file_names)



if __name__ == '__main__' : 
    start_time = time.time()
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Genre', 'Premiere', 'Runtime', 'Rating Score', 'Language'])
        

        with Pool() as pool : 
            for row in pool.imap(generate,range(int(rows_number))) :
                writer.writerow(row)

    print("--- %s seconds ---" % (time.time() - start_time))

