import argparse
import requests
import sys


def main():
    parser = argparse.ArgumentParser(description='BDS Association CLI')
    parser.add_argument('--url', help="Application url", default="http://localhost:5000")
    subparsers = parser.add_subparsers(help='actions', dest='action')

    '''
    Authentication
    '''
    parser.add_argument('--username', help='Username to connect', default=None)
    parser.add_argument('--password', help='Connection password', default=None)

    '''
    Options for Person
    '''
    subparsers.add_parser('list_persons', aliases=['ls_persons'], description='List association persons',
                          help="Show association persons")

    get_parser = subparsers.add_parser('get_person', aliases=['show_person'], description='Get association person',
                                       help="Get person")
    get_parser.add_argument("firstname", help="Firstname")
    get_parser.add_argument("lastname", help="Lastname")

    new_parser = subparsers.add_parser('new_person', aliases=['add_person', 'create_person'],
                                       description='Create new association person',
                                       help="Create person")
    new_parser.add_argument("firstname", help="Firstname")
    new_parser.add_argument("lastname", help="Lastname")
    new_parser.add_argument("email", help="Email address")
    new_parser.add_argument("--street", help='Street', default=None)
    new_parser.add_argument("--city", help='City', default=None)
    new_parser.add_argument("--postal_code", help='Postal code', default=None)
    new_parser.add_argument("--country", help='Country', default=None)
    new_parser.add_argument("--username", help='Username', default=None)
    new_parser.add_argument("--password", help='Password', default=None)

    update_parser = subparsers.add_parser('update_person', aliases=['modify_person'],
                                          description='Update association person',
                                          help="Update person")
    update_parser.add_argument("identifier", help="id")
    update_parser.add_argument("--firstname", help="Update firstname", default=None)
    update_parser.add_argument("--lastname", help="Update lastname", default=None)
    update_parser.add_argument("--email", help="Update email address", default=None)
    update_parser.add_argument("--street", help='Street', default=None)
    update_parser.add_argument("--city", help='City', default=None)
    update_parser.add_argument("--postal_code", help='Postal code', default=None)
    update_parser.add_argument("--country", help='Country', default=None)
    update_parser.add_argument("--username", help='Username', default=None)
    update_parser.add_argument("--password", help='Password', default=None)

    remove_parser = subparsers.add_parser('remove_person', aliases=['delete_person', 'rm_person'],
                                          description='Remove association person',
                                          help="Remove person")
    remove_parser.add_argument("identifier", help="id")

    '''
    Options for Sport
    '''
    subparsers.add_parser('list_sports', aliases=['ls_sports'], description='List association sports',
                          help="Show association sports")

    get_sport_parser = subparsers.add_parser('get_sport', aliases=['show_sport'], description='Get association sport',
                                             help="Get sport")
    get_sport_parser.add_argument("name", help="Name")

    new_sport_parser = subparsers.add_parser('new_sport', aliases=['add_sport', 'create_sport'],
                                             description='Create new association sport',
                                             help="Create sport")
    new_sport_parser.add_argument("name", help="Name")
    new_sport_parser.add_argument("description", help="Description")

    update_sport_parser = subparsers.add_parser('update_sport', aliases=['modify_sport'],
                                                description='Update association sport',
                                                help="Update sport")
    update_sport_parser.add_argument("identifier", help="id")
    update_sport_parser.add_argument("--name", help="Update name", default=None)
    update_sport_parser.add_argument("--description", help="Update description", default=None)

    remove_sport_parser = subparsers.add_parser('remove_sport', aliases=['delete_sport', 'rm_sport'],
                                                description='Remove association sport',
                                                help="Remove sport")
    remove_sport_parser.add_argument("identifier", help="id")

    '''
    Options for Coach
    '''
    subparsers.add_parser('list_coachs', aliases=['ls_coachs'], description='List association coachs',
                          help="Show association coachs")

    get_coach_parser = subparsers.add_parser('get_coach', aliases=['show_coach'], description='Get association coach',
                                             help="Get coach")
    get_coach_parser.add_argument("firstname", help="Firstname")
    get_coach_parser.add_argument("lastname", help="Lastname")

    new_coach_parser = subparsers.add_parser('new_coach', aliases=['add_coach', 'create_coach'],
                                             description='Create new association coach',
                                             help="Create coach")
    new_coach_parser.add_argument("firstname", help="Firstname")
    new_coach_parser.add_argument("lastname", help="Lastname")
    new_coach_parser.add_argument("email", help="Email address")
    new_coach_parser.add_argument("degree", help="Degree")
    new_coach_parser.add_argument("--street", help='Street', default=None)
    new_coach_parser.add_argument("--city", help='City', default=None)
    new_coach_parser.add_argument("--postal_code", help='Postal code', default=None)
    new_coach_parser.add_argument("--country", help='Country', default=None)
    new_coach_parser.add_argument("--username", help='Username', default=None)
    new_coach_parser.add_argument("--password", help='Password', default=None)

    update_coach_parser = subparsers.add_parser('update_coach', aliases=['modify_coach'],
                                                description='Update association coach',
                                                help="Update coach")
    update_coach_parser.add_argument("identifier", help="id")
    update_coach_parser.add_argument("--firstname", help="Update firstname", default=None)
    update_coach_parser.add_argument("--lastname", help="Update lastname", default=None)
    update_coach_parser.add_argument("--email", help="Update email address", default=None)
    update_coach_parser.add_argument("--degree", help="Update degree", default=None)
    update_coach_parser.add_argument("--street", help='Street', default=None)
    update_coach_parser.add_argument("--city", help='City', default=None)
    update_coach_parser.add_argument("--postal_code", help='Postal code', default=None)
    update_coach_parser.add_argument("--country", help='Country', default=None)
    update_coach_parser.add_argument("--username", help='Username', default=None)
    update_coach_parser.add_argument("--password", help='Password', default=None)

    remove_coach_parser = subparsers.add_parser('remove_coach', aliases=['delete_coach', 'rm_coach'],
                                                description='Remove association coach',
                                                help="Remove coach")
    remove_coach_parser.add_argument("identifier", help="id")

    '''
    Options for Member
    '''
    subparsers.add_parser('list_members', aliases=['ls_members'], description='List association members',
                          help="Show association members")

    get_member_parser = subparsers.add_parser('get_member', aliases=['show_member'], description='Get association member',
                                       help="Get member")
    get_member_parser.add_argument("firstname", help="Firstname")
    get_member_parser.add_argument("lastname", help="Lastname")

    new_member_parser = subparsers.add_parser('new_member', aliases=['add_member', 'create_member'],
                                       description='Create new association member',
                                       help="Create member")
    new_member_parser.add_argument("firstname", help="Firstname")
    new_member_parser.add_argument("lastname", help="Lastname")
    new_member_parser.add_argument("email", help="Email address")
    new_member_parser.add_argument("medical_certificate", help="Medical certificate")
    new_member_parser.add_argument("--street", help='Street', default=None)
    new_member_parser.add_argument("--city", help='City', default=None)
    new_member_parser.add_argument("--postal_code", help='Postal code', default=None)
    new_member_parser.add_argument("--country", help='Country', default=None)
    new_member_parser.add_argument("--username", help='Username', default=None)
    new_member_parser.add_argument("--password", help='Password', default=None)

    update_member_parser = subparsers.add_parser('update_member', aliases=['modify_member'],
                                          description='Update association member',
                                          help="Update member")
    update_member_parser.add_argument("identifier", help="id")
    update_member_parser.add_argument("--firstname", help="Update firstname", default=None)
    update_member_parser.add_argument("--lastname", help="Update lastname", default=None)
    update_member_parser.add_argument("--email", help="Update email address", default=None)
    update_member_parser.add_argument("--medical_certificate", help="Medical certificate", default=None)
    update_member_parser.add_argument("--street", help='Street', default=None)
    update_member_parser.add_argument("--city", help='City', default=None)
    update_member_parser.add_argument("--postal_code", help='Postal code', default=None)
    update_member_parser.add_argument("--country", help='Country', default=None)
    update_member_parser.add_argument("--username", help='Username', default=None)
    update_member_parser.add_argument("--password", help='Password', default=None)

    remove_member_parser = subparsers.add_parser('remove_member', aliases=['delete_member', 'rm_member'],
                                          description='Remove association member',
                                          help="Remove member")
    remove_member_parser.add_argument("identifier", help="id")

    args = parser.parse_args()
    url = args.url
    auth = (args.username, args.password)

    if args.action in ['list_persons', 'ls_persons']:
        res = requests.get(url + '/persons', auth=auth)
        persons = json_response(res)
        print("Persons: ")
        for person in persons:
            print("* %s %s (%s)" % (person['firstname'].capitalize(),
                                    person['lastname'].capitalize(),
                                    person['email']))
    elif args.action in ['get_person', 'show_person']:
        firstname = args.firstname
        lastname = args.lastname
        res = requests.get(url + '/persons', params={"firstname": firstname, "lastname": lastname}, auth=auth)
        person = json_response(res)
        show_person(person)
    elif args.action in ['new_person', 'add_person', 'create_person']:
        data = {
            "firstname": args.firstname,
            "lastname": args.lastname,
            "email": args.email
        }

        for key in ["street", "city", "postal_code", "country", "username", "password"]:
            value = getattr(args, key)
            if value is not None:
                data[key] = getattr(args, key)

        res = requests.post(url + '/persons', json=data, auth=auth)
        person = json_response(res)
        show_person(person)
    elif args.action in ['update_person', 'modify_person']:

        person_id = args.identifier

        data = {}
        for key in ["firstname", "lastname", "email", "street", "city", "postal_code", "country", "username",
                    "password"]:
            value = getattr(args, key)
            if value is not None:
                data[key] = getattr(args, key)
        if len(data) == 0:
            print("No update data")
            sys.exit(1)
        res = requests.put(url + '/persons/' + person_id, json=data, auth=auth)
        person = json_response(res)
        show_person(person)
    elif args.action in ['remove_person', 'delete_person', 'rm_person']:
        person_id = args.identifier
        res = requests.delete(url + '/persons/' + person_id, auth=auth)
        json_response(res)
        print("Person deleted")
    elif args.action in ['list_sports', 'ls_sports']:
        res = requests.get(url + '/sports', auth=auth)
        sports = json_response(res)
        print("Sports: ")
        for sport in sports:
            print("* %s - %s" % (sport['name'].capitalize(), sport['description']))
    elif args.action in ['new_sport', 'add_sport', 'create_sport']:
        data = {
            "name": args.name,
            "description": args.description
        }

        res = requests.post(url + '/sports', json=data, auth=auth)
        sport = json_response(res)
        show_sport(sport)
    elif args.action in ['update_sport', 'modify_sport']:

        sport_id = args.identifier

        data = {}
        for key in ["name", "description"]:
            value = getattr(args, key)
            if value is not None:
                data[key] = getattr(args, key)
        if len(data) == 0:
            print("No update data")
            sys.exit(1)
        res = requests.put(url + '/sports/' + sport_id, json=data, auth=auth)
        sport = json_response(res)
        show_sport(sport)
    elif args.action in ['remove_sport', 'delete_sport', 'rm_sport']:
        sport_id = args.identifier
        res = requests.delete(url + '/sports/' + sport_id, auth=auth)
        json_response(res)
        print("Sport deleted")
    elif args.action in ['list_coachs', 'ls_coachs']:
        res = requests.get(url + '/coachs', auth=auth)
        persons = json_response(res)
        print("Coachs: ")
        for person in persons:
            print("* %s %s (%s)" % (person['firstname'].capitalize(),
                                    person['lastname'].capitalize(),
                                    person['email']))
    elif args.action in ['get_coach', 'show_coach']:
        firstname = args.firstname
        lastname = args.lastname
        res = requests.get(url + '/coachs', params={"firstname": firstname, "lastname": lastname}, auth=auth)
        person = json_response(res)
        show_person(person)
    elif args.action in ['new_coach', 'add_coach', 'create_coach']:
        data = {
            "firstname": args.firstname,
            "lastname": args.lastname,
            "email": args.email,
            "degree": args.degree
        }

        for key in ["street", "city", "postal_code", "country", "username", "password"]:
            value = getattr(args, key)
            if value is not None:
                data[key] = getattr(args, key)

        res = requests.post(url + '/coachs', json=data, auth=auth)
        coach = json_response(res)
        show_coach(coach)
    elif args.action in ['update_coach', 'modify_coach']:

        person_id = args.identifier

        data = {}
        for key in ["firstname", "lastname", "email", "street", "city", "postal_code", "country", "username",
                    "password", "degree"]:
            value = getattr(args, key)
            if value is not None:
                data[key] = getattr(args, key)
        if len(data) == 0:
            print("No update data")
            sys.exit(1)
        res = requests.put(url + '/coachs/' + person_id, json=data, auth=auth)
        person = json_response(res)
        show_coach(person)
    elif args.action in ['remove_coach', 'delete_coach', 'rm_coach']:
        person_id = args.identifier
        res = requests.delete(url + '/coachs/' + person_id, auth=auth)
        json_response(res)
        print("Coach deleted")
    elif args.action in ['list_members', 'ls_members']:
        res = requests.get(url + '/members', auth=auth)
        persons = json_response(res)
        print("Members: ")
        for person in persons:
            print("* %s %s (%s) - Certificate %s" % (person['firstname'].capitalize(),
                                    person['lastname'].capitalize(),
                                    person['email'],
                                    person['medical_certificate']))
    elif args.action in ['get_member', 'show_member']:
        firstname = args.firstname
        lastname = args.lastname
        res = requests.get(url + '/members', params={"firstname": firstname, "lastname": lastname}, auth=auth)
        person = json_response(res)
        show_person(person)
    elif args.action in ['new_member', 'add_member', 'create_member']:
        data = {
            "firstname": args.firstname,
            "lastname": args.lastname,
            "email": args.email,
            "medical_certificate": args.medical_certificate
        }

        for key in ["street", "city", "postal_code", "country", "username", "password", "medical_certificate"]:
            value = getattr(args, key)
            if value is not None:
                data[key] = getattr(args, key)

        res = requests.post(url + '/members', json=data, auth=auth)
        coach = json_response(res)
        show_person(coach)
    elif args.action in ['update_member', 'modify_member']:

        person_id = args.identifier

        data = {}
        for key in ["firstname", "lastname", "email", "street", "city", "postal_code", "country", "username",
                    "password", "medical_certificate"]:
            value = getattr(args, key)
            if value is not None:
                data[key] = getattr(args, key)
        if len(data) == 0:
            print("No update data")
            sys.exit(1)
        res = requests.put(url + '/members/' + person_id, json=data, auth=auth)
        person = json_response(res)
        show_person(person)
    elif args.action in ['remove_member', 'delete_member', 'rm_member']:
        person_id = args.identifier
        res = requests.delete(url + '/members/' + person_id, auth=auth)
        json_response(res)
        print("Member deleted")
    else:
        parser.print_help()
        print('There is a difference between person, member and coach:')
        print(' - A person represents both members and coaches')
        print(' - A member is someone from the association')
        print(' - A coach teaches a sport')


def json_response(response):
    if 400 <= response.status_code < 600:
        try:
            content = response.json()
            if "message" in content:
                print(content["message"])
            else:
                print("A server error occurred")
        except ValueError:
            print("A server error occurred")
        sys.exit(1)
    else:
        if response.status_code != 204:
            return response.json()


def show_person(person):
    print("Person profile: ")
    print(person['firstname'].capitalize(), person['lastname'].capitalize())
    print("Id: ", person['id'])
    print("Email:", person['email'])
    if person['address'] is not None:
        print("Address: {0}, {1} {2}, {3}".format(person['address']['street'], person['address']['postal_code'],
                                                  person['address']['city'], person['address']['country']))


def show_sport(sport):
    print("Sport information: ")
    print(sport["name"], " - ", sport["description"])


def show_coach(coach):
    print("Coach profile: ")
    print(coach['firstname'].capitalize(), coach['lastname'].capitalize())
    print("Id: ", coach['id'])
    print("Email:", coach['email'])
    print('Degree:', coach['degree'])


if __name__ == "__main__":
    main()
