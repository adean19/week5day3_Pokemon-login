from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from app import app
from .forms import PokemonForm, SignUpForm, LoginForm
from .models import User, Pokemon, Caught_Pokemon, db
import requests, json

@app.route('/', methods=["GET", "POST"])
def home_page():
    return render_template('index.html')

#User Authentication

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            #add user to the database
            user = User(username, email, password)

            db.session.add(user)
            db.session.commit()
            flash('Successfully created user.', 'Success')
            return redirect(url_for('login'))
        flash('An error has occured. Please submit a valid form', 'danger')
    return render_template('signup.html', form = form)

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data

            #find user from db
            user = User.query.filter_by(username=username).first()

            if user:
                if user.password == password:
                    login_user(user)
                    flash('Successfully logged in.', 'success')
                    return redirect(url_for('home_page'))
                else:
                    flash('Incorrect username/password', 'danger')
            else:
                flash('Incorrect username.', 'danger')
        else:
            flash('An error has occurred. Please submit a valid form', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_page'))

#Searching for Pokemon
@app.route('/pokemonsearch', methods=["GET","POST"])
def pokemon_search():
    form = PokemonForm()
    pokemon_info = {}
    if request.method == "GET":
        pass
    else:
        pokemon_info = Pokemon.query.filter_by(name=form.pokemon_name.data.lower()).first()
        if pokemon_info:
            return render_template('pokemon_search.html', title='Pokemon', form=form, pokemon_data=pokemon_info)
        else:
            pokemon_apicall = f'https://pokeapi.co/api/v2/pokemon/{form.pokemon_name.data.lower()}'
            pokemon_apicall_response = requests.get(pokemon_apicall)
            if pokemon_apicall_response.ok == True:
                # Call pokemon data from API
                pokemon_data = {'Name': pokemon_apicall_response.json()['forms'][0]['name'],
                                'Ability': pokemon_apicall_response.json()['abilities'][0]['ability']['name'],
                                'Stats': {'HP': pokemon_apicall_response.json()['stats'][0]['base_stat'],
                                        'Defense': pokemon_apicall_response.json()['stats'][2]['base_stat'],
                                        'Attack' : pokemon_apicall_response.json()['stats'][1]['base_stat']},
                                'Sprite': pokemon_apicall_response.json()['sprites']['front_shiny']}
                # Setting pokemon_data to individual variables
                pokemon_name = pokemon_data['Name']
                pokemon_ability = pokemon_data['Ability']
                pokemon_hp = pokemon_data['Stats']['HP']
                pokemon_attack = pokemon_data['Stats']['Attack']
                pokemon_defense = pokemon_data['Stats']['Defense']
                pokemon_sprite = pokemon_data['Sprite']
                # Setting individual pokemon variables to class
                pokemon_info = Pokemon(pokemon_name, pokemon_ability, pokemon_hp, pokemon_attack, pokemon_defense, pokemon_sprite)
                # Add pokemon_info to db
                if not Pokemon.query.filter_by(name=pokemon_name).first():
                    db.session.add(pokemon_info)
                    db.session.commit()
    return render_template('pokemon_search.html', title='Pokemon', form=form, pokemon_data=pokemon_info)

#Catching Pokemon
@app.route('/pokemonsearch/catchpokemon/<pokemon_id>', methods=["GET", "POST"])
@login_required
def catch_pokemon(pokemon_id):
    current_team_count = Caught_Pokemon.query.filter_by(user_id=current_user.user_id).count()

    if current_team_count < 5:
        catch = Caught_Pokemon.query.filter_by(pokemon_id=pokemon_id, user_id=current_user.user_id).first()

        if catch:
            flash(f'You already have a {Pokemon.query.get(catch.pokemon_id).name} on your team.')
        else:
            new_pokemon = Caught_Pokemon(user_id=current_user.user_id, pokemon_id=pokemon_id)
            db.session.add(new_pokemon)
            db.session.commit()
            flash(f'{Pokemon.query.get(pokemon_id).name} has been added to your team.')
    else:
        flash('Your team is full. You must release a Pokémon to add a new one.')

    return redirect(url_for('pokemon_search'))

#My Pokemon
@app.route('/pokemonsearch/myteam', methods=["GET"])
@login_required
def my_team():
    user_team = db.session.query(Caught_Pokemon, Pokemon).join(Pokemon).filter(Caught_Pokemon.user_id == current_user.user_id).all()
    return render_template('my_team.html', user_team=user_team)

#Releasing Pokemon
@app.route('/pokemonsearch/release/<int:pokemon_id>', methods=["POST"])
@login_required
def release_pokemon(pokemon_id):
    pokemon_to_release = Caught_Pokemon.query.filter_by(pokemon_id=pokemon_id, user_id=current_user.user_id).first()

    if pokemon_to_release:
        released_pokemon = Pokemon.query.get(pokemon_to_release.pokemon_id) 
        released_pokemon_name = released_pokemon.name 
        db.session.delete(pokemon_to_release)
        db.session.commit()
        flash(f'{released_pokemon_name} has been released from your party.') 
    else:
        flash('Pokemon not found in your team.')

    return redirect(url_for('my_team'))

#Battling Pokemon