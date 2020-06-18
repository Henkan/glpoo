import argparse
import requests
import sys


def main():
    parser = argparse.ArgumentParser(description='BDS Association CLI')
    parser.add_argument('--url', help="Application url", default="http://localhost:5000")
    subparsers = parser.add_subparsers(help='actions', dest='action')

    subparsers.add_parser('list', aliases=['ls'], description='List association persons',
                          help="Show association persons")

    get_parser = subparsers.add_parser('get', aliases=['show'], description='Get association person',
                                       help="Get person")
    get_parser.add_argument("firstname", help="Firstname")
    get_parser.add_argument("lastname", help="Lastname")

    new_parser = subparsers.add_parser('new', aliases=['add', 'create'], description='Create new association person',
                                       help="Create person")
    new_parser.add_argument("firstname", help="Firstname")
    new_parser.add_argument("lastname", help="Lastname")
    new_parser.add_argument("email", help="Email address")

    update_parser = subparsers.add_parser('update', aliases=['modify'], description='update association person',
                                          help="Create person")
    update_parser.add_argument("identifier", help="id")
    update_parser.add_argument("--firstname", help="Update firstname", default=None)
    update_parser.add_argument("--lastname", help="Update lastname", default=None)
    update_parser.add_argument("--email", help="Update email address", default=None)

    remove_parser = subparsers.add_parser('remove', aliases=['delete', 'rm'], description='Remove association person',
                                          help="Remove person")
    remove_parser.add_argument("identifier", help="id")

    args = parser.parse_args()
    url = args.url

    if args.action in ['list', 'ls']:
        res = requests.get(url + '/persons')
        persons = json_response(res)
        print("Persons: ")
        for person in persons:
            print("* %s %s (%s)" % (person['firstname'].capitalize(),
                                    person['lastname'].capitalize(),
                                    person['email']))
    elif args.action in ['get', 'show']:
        firstname = args.firstname
        lastname = args.lastname
        res = requests.get(url + '/persons', params={"firstname": firstname, "lastname": lastname})
        person = json_response(res)

        show_person(person)
    elif args.action in ['new', 'add', 'create']:
        data = {
            "firstname": args.firstname,
            "lastname": args.lastname,
            "email": args.email
        }
        res = requests.post(url + '/persons', json=data)
        person = json_response(res)
        show_person(person)
    elif args.action in ['update', 'modify']:

        person_id = args.identifier

        data = {}
        for key in ["firstname", "lastname", "email"]:
            value = getattr(args, key)
            if value is not None:
                data[key] = getattr(args, key)
        if len(data) == 0:
            print("No update data")
            sys.exit(1)
        res = requests.put(url + '/persons/' + person_id, json=data)
        person = json_response(res)
        show_person(person)
    elif args.action in ['remove', 'delete', 'rm']:
        person_id = args.identifier
        res = requests.delete(url + '/persons/' + person_id)
        json_response(res)
        print("Person deleted")
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


if __name__ == "__main__":
    main()
