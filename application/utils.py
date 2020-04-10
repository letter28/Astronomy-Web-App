from application.db_models import db, Planet, User, Star


def create_db():
    db.create_all()
    print("Database created.")


def drop_db():
    db.drop_all()
    print("Database deleted.")


def seed_db():
    # stars
    sol = Star(star_name='Sol',
               location=0,
               mass=1988500e24,  # kg
               diameter=695700,  # km
               abs_magnitude='+4.83')

    # planets
    mercury = Planet(planet_name='Mercury',
                     no_of_moons=0,
                     home_star='Sol',
                     mass=0.330e24,
                     diameter=4879,
                     distance=57.9e6,
                     orbital_period=88)

    venus = Planet(planet_name='Venus',
                   no_of_moons=0,
                   home_star='Sol',
                   mass=4.87e24,
                   diameter=12104,
                   distance=108.2e6,
                   orbital_period=224.7)

    earth = Planet(planet_name='Earth',
                   no_of_moons=1,
                   home_star='Sol',
                   mass=5.97e24,
                   diameter=12756,
                   distance=149.6e6,
                   orbital_period=365.2)

    mars = Planet(planet_name='Mars',
                  no_of_moons=2,
                  home_star='Sol',
                  mass=0.642e24,
                  diameter=6792,
                  distance=227.9e6,
                  orbital_period=687)

    jupiter = Planet(planet_name='Jupiter',
                     no_of_moons=79,
                     home_star='Sol',
                     mass=1898e24,
                     diameter=142984,
                     distance=778.6e6,
                     orbital_period=4331)

    saturn = Planet(planet_name='Saturn',
                    no_of_moons=82,
                    home_star='Sol',
                    mass=568e24,
                    diameter=120536,
                    distance=1433.5e6,
                    orbital_period=10747)

    uranus = Planet(planet_name='Uranus',
                    no_of_moons=27,
                    home_star='Sol',
                    mass=86.8e24,
                    diameter=51118,
                    distance=2872.5e6,
                    orbital_period=30589)

    neptune = Planet(planet_name='Neptune',
                     no_of_moons=14,
                     home_star='Sol',
                     mass=102e24,
                     diameter=49528,
                     distance=4495.1e6,
                     orbital_period=59800)

    pluto = Planet(planet_name='Pluto',
                   no_of_moons=5,
                   home_star='Sol',
                   mass=0.0146e24,
                   diameter=2370,
                   distance=5906.4e6,
                   orbital_period=90560)

    db.session.add_all([sol, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto])
    db.session.commit()
    print("Database seeded.")
