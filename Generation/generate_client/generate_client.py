from faker import Faker
from faker_credit_score import CreditScore
from faker_vehicle import VehicleProvider
from faker.providers import BaseProvider
import random
import csv
import time
import progressbar
from datetime import datetime


fake = Faker()

fake.add_provider(CreditScore)
fake.add_provider(VehicleProvider)
# fake.credit_score_provider()
# 'TransUnion'
# fake.credit_score()
# 791

class generate_client : 
    def __init__(self):
        self.client_name = str(','.join(fake.profile(['name']).values()))
        self.film = [self.get_client_name(),self.get_client_sex(),self.get_client_mail(),self.get_client_movie_genres(), self.get_client_language_spoken(),self.get_client_car(),fake.credit_score()]

    def __iter__(self) :
        return iter(self.film)

    # not used because it s Resources demanding
    def get_client_username(self) : 
        profile = fake.profile(['username'])
        return str(','.join(profile.values()))
    
    def get_client_name(self) : 
        return self.client_name

    def get_client_mail(self) : 
        return self.client_name.replace(' ', '').lower() + random.choice(['@gmail.com','@outlook.fr','@orange.com','@hotmail.com','@wanadoo.com']) 
    
    def get_client_sex(self) : 
        if bool(random.getrandbits(1)) :
            return ('Male')
        else : 
            return ('Female')
        # profile = fake.profile(['sex'])
        # return str(','.join(profile.values()))

    def get_client_car(self) :
        return fake.vehicle_make_model()

    def get_client_date(self):
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

    def get_client_movie_genres(self) : 
        list_movies =  random.sample(['Documentary', 'Thriller', 'Mystery', 'Horror', 'Action', 'Comedy', 'Drama', 'Romance'],random.randint(1,8))
        return ",".join(list_movies)


    def get_client_language_spoken(self) : 
        list_language = random.sample(('English', 'Chinese', 'Italian', 'Spanish', 'Hindi', 'Japanese'),random.randint(1,5))
        return  ",".join(list_language)

            

    def get_movie_rating(self):
        return random.gauss(5, 2.5)


    def generate_client_csvfile(rows_number = 1e6) : 
        file_names = 'client_' + str(rows_number) + '_rows_' + str(datetime.now().strftime("%Hh%Mm%Ss") ) + '.csv'
        path = str('Generation/data/client/' + file_names)
        bar = progressbar.ProgressBar(maxval=int(rows_number))
        print("Generating %s"%file_names)
        start_time = time.time()
        bar.start()
        with open(path, 'w',newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['name', 'sex', 'mail', 'client_movie_genres','client_language_spoken','client_car','credit_score'])
            for row in range(int(rows_number)) :
                writer.writerow(generate_client())
                bar.update(row)
        bar.finish()

        print("--- %s seconds ---" % (time.time() - start_time))
        print("File %s generated"%file_names)
        return file_names,path


