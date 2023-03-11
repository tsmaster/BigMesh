import capnp

import addressbook_capnp

print(addressbook_capnp.qux)

addresses = addressbook_capnp.AddressBook.new_message()

person = addressbook_capnp.Person.new_message(name='Alice')

people = addresses.init('people', 2)

alice = people[0]

alice.id = 123
alice.name = 'Alice'
alice.email = 'alice@example.com'

#enums

alicePhone = alice.init('phones', 1)[0]

alicePhone.type = 'mobile'

# unions

alice.employment.school = "MIT"

# writing to a file

f = open('example.bin', 'w+b')
addresses.write(f)

# reading from a file
f = open('example.bin', 'rb')
addresses = addressbook_capnp.AddressBook.read(f)

# reading fields

for pers_idx, person in enumerate(addresses.people):
    print("person", pers_idx)
    print(person.name, ':', person.email)
    for phone in person.phones:
        print(phone.type, ':', phone.number)

    which = person.employment.which()
    print(which)
    if which == 'unemployed':
        print('unemployed')
    elif which == 'employer':
        print('employer:', person.employment.employer)
    elif which == 'school':
        print('student at:', person.employment.school)
    elif which =='selfEmployed':
        print('self employed')
    print()
