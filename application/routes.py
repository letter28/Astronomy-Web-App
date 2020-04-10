from application import app, jsonify, request
from flask import render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required
from application.db_models import db, Planet, Star, User, UserSchema, PlanetSchema, StarSchema
from application.forms import LoginForm, RegisterForm, PlanetNewForm

user_schema = UserSchema()
users_schema = UserSchema(many=True)

planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)

star_schema = StarSchema()
stars_schema = StarSchema(many=True)


# Routes
@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", title="Astronomy web application", index=True)


@app.route("/stars")
@login_required
def stars():
    stars_list = Star.query.all()
    star_data = stars_schema.dump(stars_list)
    return render_template("stars.html", title="Stars", star_data=star_data, stars=True)


@app.route("/planets")
@login_required
def planets():
    planet_list = Planet.query.all()
    planet_data = planets_schema.dump(planet_list)
    for i in range(len(planet_data)):
        planet_data[i] = {'planet_id': int(planet_data[i]['planet_id']),
                          'planet_name': planet_data[i]['planet_name'],
                          'home_star': planet_data[i]['home_star'],
                          'distance': int(planet_data[i]['distance']),
                          'mass': float(planet_data[i]['mass']),
                          'diameter': int(planet_data[i]['diameter']),
                          'no_of_moons': int(planet_data[i]['no_of_moons']),
                          'orbital_period': float(planet_data[i]['orbital_period'])}
    return render_template("planets_new.html", title="Planets", planets=True, planet_data=planet_data)


@app.route("/planet/<int:planet_id>", methods=['GET'])
@login_required
def planet_single(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        planet_data = {'planet_id': int(planet.planet_id),
                       'planet_name': planet.planet_name,
                       'home_star': planet.home_star,
                       'distance': int(planet.distance),
                       'mass': float(planet.mass),
                       'diameter': int(planet.diameter),
                       'no_of_moons': int(planet.no_of_moons),
                       'orbital_period': float(planet.orbital_period)}

        return render_template("planet.html", title=f"Planets - {planet_data['planet_name']}",
                               planets=True, planet=planet_data)
    else:
        return render_template("error.html")


@app.route("/add_planet", methods=['GET', 'POST'])
@login_required
def add_planet():
    form = PlanetNewForm()

    if form.validate_on_submit():
        planet_name = form.planet_name.data
        home_star = form.home_star.data
        distance = form.distance.data
        mass = form.mass.data
        diameter = form.diameter.data
        no_of_moons = form.no_of_moons.data
        orbital_period = form.orbital_period.data

        new_planet = Planet(planet_name=planet_name, home_star=home_star, distance=distance, mass=mass,
                            diameter=diameter, no_of_moons=no_of_moons, orbital_period=orbital_period)
        db.session.add(new_planet)
        db.session.commit()
        flash(f'Planet {planet_name} added successfully!', category='success')
        return redirect(url_for('index'))
    return render_template("add_planet.html", title='Add a new planet', form=form, planets=True)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        email: str = login_form.email.data
        password: str = login_form.password.data

        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash('Invalid username or password.', category='danger')
            return redirect(url_for('login'))
        login_user(user, remember=login_form.remember_me.data)
        flash(f"{user.user_name}, you're successfully logged in!", category="success")
        return redirect(url_for('index'))
    return render_template("login.html", title="Login", form=login_form, login=True)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    register_form = RegisterForm()

    if register_form.validate_on_submit():
        email = register_form.email.data
        password = register_form.password.data
        first_name = register_form.first_name.data
        last_name = register_form.last_name.data
        username = register_form.username.data

        user = User(user_name=username, first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash(f"{username}, you're successfully registered!", category="success")
        return redirect(url_for('index'))

    return render_template("register.html", form=register_form, title="Register", register=True)


@app.route('/account')
@app.route('/account/<string:username>')
@login_required
def account(username=None):
    if username is None:
        return redirect(url_for('index'))

    user = User.query.filter_by(user_name=username).first_or_404()
    return render_template("account.html", title=f"Account - {username}", account=True, user=user)


# @app.route('/retrieve_password/<string:email>', methods=['GET'])
# def retrieve_lost_pswd(email: str):
#     status_code = send_lost_pswd(email=email)
#     if status_code == 201:
#         return jsonify(message=f"Password sent to: {email}")
#     else:
#         return jsonify(message="That email isn't registered.")
#
#
# @app.route('/add_planet', methods=['POST'])
# @jwt_required
# def add_planet():
#     planet_name = request.form['planet_name']
#     planet = Planet.query.filter_by(planet_name=planet_name).first()
#     if planet:
#         return jsonify(message="There is already a planet by that name."), 409
#     else:
#         planet_type = request.form['planet_type']
#         home_star = request.form['home_star']
#         mass = float(request.form['mass'])
#         radius = float(request.form['radius'])
#         distance = float(request.form['distance'])
#
#         new_planet = Planet(planet_name=planet_name,
#                             planet_type=planet_type,
#                             home_star=home_star,
#                             mass=mass,
#                             radius=radius,
#                             distance=distance)
#
#         db.session.add(new_planet)
#         db.session.commit()
#
#         return jsonify(message=f"Planet {planet_name} added successfully!"), 201
#
#
# @app.route('/update_planet', methods=['PUT'])
# @jwt_required
# def update_planet():
#     planet_id = int(request.form['planet_id'])
#     planet = Planet.query.filter_by(planet_id=planet_id).first()
#     if planet:
#         if len(request.form) == 7:
#             planet.planet_name = request.form['planet_name']
#             planet.planet_type = request.form['planet_type']
#             planet.home_star = request.form['home_star']
#             planet.mass = float(request.form['mass'])
#             planet.distance = float(request.form['distance'])
#             planet.radius = float(request.form['radius'])
#             db.session.commit()
#             return jsonify(message=f"Planet with id: {planet_id} updated successfully."), 202 # change was accepted
#         else:
#             return jsonify(message=f"Planet could not be updated, wrong number of parameters."), 403
#     else:
#         return jsonify(message=f"Planet with id: {planet_id} does not exist in the database."), 404  # not found
#
#
# @app.route('/remove_planet/<int:planet_id>', methods=['DELETE'])
# @jwt_required
# def remove_planet(planet_id: int):
#     planet = Planet.query.filter_by(planet_id=planet_id).first()
#     if planet:
#         db.session.delete(planet)
#         db.session.commit()
#         return jsonify(message=f"Planet with id: {planet_id} deleted successfully."), 202
#     else:
#         return jsonify(message=f"Planet with id: {planet_id} does not exist in the database."), 404
#
#
# @app.route('/users/all', methods=['GET'])
# def all_users():
#     users_list = User.query.all()
#     result = users_schema.dump(users_list)
#     return jsonify(result)
