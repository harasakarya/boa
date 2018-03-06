import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    def __init__(self):
        #prod email list should be retrieved from hosted file in future
        self.prod_email_list = ["officialemre@gmail.com", "cryptoboa@exode.com", "lechalex1@gmail.com",
           "bhomsi@gmail.com", "bskb04@gmail.com",
           "zotthewizard@gmail.com", "dnhvcrpt@gmail.com", "nicastrh@gmail.com",
            "jonathanng222@gmail.com", "alexswenews@gmail.com", "dvddvdsn777@gmail.com", "akoruth95@gmail.com",
           "miroslavstricevic@gmail.com","kninjas@gmail.com","biggt620@gmail.com","davidbeddow92@gmail.com",
           "ignjatovic@gmail.com", "robert.kamerer@gmail.com","skrussel15@gmail.com", "pupo.robert@gmail.com",
           "obpatel96@gmail.com","ivancvetkovic83@gmail.com","vaibhav.shrishail@gmail.com", "milandotlic@gmail.com",
            "james.w.fant@wellsfargo.com",
           "sixohofficial@gmail.com"]
        self.dev_email_list = ["akoruth95@gmail.com"]
        self.test_email_list = ["akoruth95@gmail.com"]

    def getEnvironment(self):
        if 'APP_SETTINGS' in os.environ:
            return os.environ['APP_SETTINGS']
        return 'local'

    def getEmailList(self):
        if 'APP_SETTINGS' in os.environ:
            if os.environ['APP_SETTINGS'] == 'production':
                return self.prod_email_list
            if os.environ['APP_SETTINGS'] == 'staging':
                return self.dev_email_list
        return self.test_email_list

    def updateProdEmailList(self):
        #should update hosted email list in future?
        return