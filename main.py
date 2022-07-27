import pandas as pd
import re

email1 = pd.read_csv('email-pack-1.txt', header = None)
email2 = pd.read_csv('emails-pack-2.txt', header = None)
email3 = pd.read_csv('emails3.txt', header = None)

email4 = pd.read_csv('last-email-pack.csv', sep = ';', index_col ='username')
email4.reset_index(drop = True, inplace = True)
email4.rename(columns = {'email' :0}, inplace = True)

email5 = pd.read_csv('other-emails4.txt', header = None)

df = email1.append([email2, email3, email4, email5], ignore_index = True)

class Email():
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def invalid_emails(self):
        wrong_emails = self.dataframe[self.dataframe[0].apply(lambda x: False if re.search('[a-zA-Z0-9.]+@[a-zA-Z]+\.[a-zA-Z0-9]{1,4}', x) else True)]
        print('There are', len(wrong_emails[0]), 'invalid e-mails')
        for row in wrong_emails[0]:
            print(row)

    def search_email(self):
        searching_phrase = input('Write text, which you would like to serach: ')
        search_result = self.dataframe[self.dataframe.apply(lambda x: x.astype(str).str.contains(searching_phrase).any(), axis = 1)]
        print('Found emails with ', searching_phrase, 'in email (', len(search_result[0]),')')
        for row in search_result[0]:
            print(row)
    def sorting_domains(self):
        good_emials = self.dataframe[self.dataframe[0].apply(lambda x: True if re.search('[a-zA-Z0-9.]+@[a-zA-Z]+\.[a-zA-Z0-9]{1,4}', x) else False)]
        good_emials['domains'] = good_emials[0].apply(lambda x: x.split('@')[-1])
        good_emials = good_emials.groupby('domains')[0].apply(lambda tags: ','.join(tags))
        for ind in good_emials.index:
            print('Domain', ind, '(', good_emials[ind].count('@'), ')', ':')
            print(good_emials[ind].split(','), '\n')
    def not_send(self):
        logs = new = pd.read_csv('email-sent.logs', header = None, sep = '\'')
        good_emials = self.dataframe[self.dataframe[0].apply(lambda x: True if re.search('[a-zA-Z0-9.]+@[a-zA-Z]+\.[a-zA-Z0-9]{1,4}', x) else False)]
        good_emials['cos'] = good_emials[0].isin(logs[1])
        print('Emails not sent', '(',good_emials['cos'].values.sum(),')')


# load df with emails
e = Email(df)
# Showing invalid emails
e.invalid_emails()

# Seraching for e-mail in df with user input
e.search_email()

# Sorting emails with thier domains
e.sorting_domains()

# using logs search if emails was send or not
e.not_send()