from faker import Faker
from faker.providers import BaseProvider
import random
import csv
import time
import progressbar
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


class generate_film : 
    def __init__(self):
        self.film = [self.get_movie_name(), fake.movie_genre(), self.get_movie_date(), self.get_movie_len(), self.get_movie_rating(), fake.language(), self.get_author(),self.get_timestamp()]

    def __iter__(self) :
        return iter(self.film)


    def capitalize(self,str):
        return str.capitalize()

    def get_movie_name(self):
        words = fake.words()
        capitalized_words = list(map(self.capitalize, words))
        return ' '.join(capitalized_words)

    def get_movie_date(self):
        return fake.date()

    def get_movie_len(self):
        # add noise
        len = random.randrange(40, 160)
        if (len  <= 50 ) : 
            return  random.randrange(20,50)
        elif (len >= 150) : 
            return  random.randrange(150,400)
        else : 
            return len 
            

    def get_movie_rating(self):
        return random.gauss(5, 2.5)

    def get_author(self) :
        return fake.first_name() + ' ' + fake.last_name()

    def get_timestamp(self) :
        return datetime.now()

    def generate_film_csvfile(rows_number = 1e6) : 
        """generate film csv file with n rows numbers 

        Args:
            rows_number (float, optional): _description_. Defaults to 1e6.

        Returns:
            string file_name: file name
            string path : path of csv file
        """

        file_name = 'movie_data_' + str(rows_number) + '_rows_' + str(datetime.now().strftime("%Hh%Mm%Ss") ) + '.csv'
        path = str('Generation/data/named/' + file_name)
        bar = progressbar.ProgressBar(maxval=int(rows_number))
        print("\n Generating %s \n"%file_name )

        start_time = time.time()
        bar.start()
        with open(path, 'w',newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Title', 'Genre', 'Premiere', 'Runtime', 'Rating Score', 'Language','Author','Timestamp'])
            for row in range(int(rows_number)) :
                writer.writerow(generate_film())
                bar.update(row)
        bar.finish()

        print("--- %s seconds ---" % (time.time() - start_time))
        print("File %s generated"%file_name)
        return file_name,path


