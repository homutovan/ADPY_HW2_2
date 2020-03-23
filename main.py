import re
import csv
from pprint import pprint

phone_pattern = '(\+7|8)(\s?\(?)(\d{3})(\)?\s|-?)(\d{3})-?(\d{2})-?(\d{2})(\s*\(?(доб\.)\s)?(\d{4})?\)?'

class Contact:
    
    header = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']
    
    def __init__(self, contact_string):
        normalize_string = ' '.join(contact_string[:3]).strip().split() + contact_string[3:]
        self.__dict__ = dict(zip(Contact.header, normalize_string))
        self.phone = re.sub(phone_pattern, r'+7(\3)\5-\6-\7 \9\10', self.phone).strip()
        self.__dict__ = {key: value for key, value in self.__dict__.items() if len(value) > 1}
        
    def __eq__(self, other):
        if self.lastname == other.lastname:
            self.__dict__.update(other.__dict__)
        return self.lastname == other.lastname
    
    def __hash__(self):
        return 0
        
    def __str__(self):
        return str(self.__dict__)
    
    def __repr__(self):
        return str(list(self.__dict__.values()))
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if Contact.header:
            return self.__dict__.get(Contact.header.pop(0),'')
        else:
            Contact.header = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']
            raise StopIteration
    
if __name__ == '__main__':

    with open("phonebook_raw.csv", encoding='utf8') as f:
        rows = csv.reader(f, delimiter = ',')
        contacts_list = list(rows)
        
    clean_contacts_list = [contacts_list[0]] + list(set(Contact(contact_string) for contact_string in contacts_list[1:]))

    with open("phonebook.csv", "w", encoding='utf8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(clean_contacts_list)