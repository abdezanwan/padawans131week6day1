from app import app, db
from flask import render_template, request, redirect, url_for
from .forms import LoginForm, SignUpForm, SearchPokemonForm
from .models import User, Pokemon, UserPokemon
from flask_login import current_user, login_user, logout_user, login_required

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

    return render_template('signup.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login_page():
    search_form = SearchPokemonForm()
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            pokemon_name = form.pokemon_name.data

            pokemon = Pokemon.query.filter_by(name=pokemon_name).first()

            if not pokemon:
                # If the Pokemon doesn't exist, you can add it to the database here
                # For example: pokemon = Pokemon(name=pokemon_name, ability='Thunder Shock')
                # Then add it to the UserPokemon table if the user has space in their collection
                pass

          
            if current_user.is_authenticated:
                user = User.query.get(current_user.id)
                if user and len(user.pokemons) < 5:
                    user_pokemon = UserPokemon(user_id=user.id, pokemon_id=pokemon.id)
                    db.session.add(user_pokemon)
                    db.session.commit()

            return redirect(url_for('display_pokemon', name=pokemon_name))
        else:
           
            # error 
            pass

    return render_template('login.html', form=form, search_form=search_form)

@app.route("/display_pokemon/<name>")
@login_required
def display_pokemon(name):
    user = User.query.get(current_user.id)
    return render_template('display_pokemon.html', user=user)
