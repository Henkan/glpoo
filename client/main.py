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
    else:
        parser.print_help()


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


if __name__ == "__main__":
    main()
