from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from app import app
from .forms import PokemonForm, SignUpForm, LoginForm
from .models import User, db
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
    pokemon_data = {}
    if request.method == "GET":
        pass
    else:
        pokemon_apicall = f'https://pokeapi.co/api/v2/pokemon/{form.pokemon_name.data.lower()}'
        pokemon_apicall_response = requests.get(pokemon_apicall)
        if pokemon_apicall_response.ok == True:
            pokemon_data = {'Name': pokemon_apicall_response.json()['forms'][0]['name'],
                            'Ability': pokemon_apicall_response.json()['abilities'][0]['ability']['name'],
                            'Stats': {'HP': pokemon_apicall_response.json()['stats'][0]['base_stat'],
                                      'Defense': pokemon_apicall_response.json()['stats'][2]['base_stat'],
                                      'Attack' : pokemon_apicall_response.json()['stats'][1]['base_stat']},
                            'Sprite': pokemon_apicall_response.json()['sprites']['front_shiny']}
    return render_template('pokemon_search.html', title='Pokemon', form=form, pokemon_data=pokemon_data)

#My Team

#Battling Pokemon