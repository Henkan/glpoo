
from flask import Flask
from model.database import DatabaseEngine
from vue.person_resource import person_resource
from vue.sport_resource import sport_resource
from vue.coach_resource import coach_resource
from vue.member_resource import member_resource


def main():
    print("Welcome of BDS Association")

    # Init db
    database_engine = DatabaseEngine(url='sqlite:///bds.db')
    database_engine.create_database()

    # Start api
    app = Flask(__name__)

    app.register_blueprint(person_resource)
    app.register_blueprint(sport_resource)
    app.register_blueprint(coach_resource)
    app.register_blueprint(member_resource)

    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
