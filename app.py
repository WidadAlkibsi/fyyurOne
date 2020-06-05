#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
from datetime import datetime
import sys 
from itertools import groupby
from operator import itemgetter
from forms import *


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_pyfile('config.py')
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    description = db.Column(db.String(500), default='')
    seeking_talent = db.Column(db.Boolean, default=False)
    website = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    shows = db.relationship('Shows', backref='Venue', lazy=True)


    def __init__(self, name, city, address, state, phone, facebook_link, image_link, website,
     genres, seeking_talent=False, description=""):
        self.name = name
        self.city = city
        self.address = address
        self.state = state
        self.phone = phone
        self.website = website
        self.genres = genres
        self.seeking_talent= seeking_talent
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.description = description

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def venuedictionary(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'address': self.address,
            'genres': self.genres,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_talent': self.seeking_talent,
            'description': self.description,
        }

    # TODO: implement any missing fields, as a database migration using Flask-Migrate



class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500), default='')
    website = db.Column(db.String(120))
    shows = db.relationship('Shows', backref='Artist', lazy=True)

    def __init__(self, name, city, state, phone, facebook_link, image_link, website,
     genres, seeking_venue=False, seeking_description=""):
        self.name = name
        self.city = city
        self.state = state
        self.phone = phone
        self.website = website
        self.genres = genres
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.description = seeking_description

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def artistdictionary(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'genres': self.genres, 
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
          }

  # TODO: implement any missing fields, as a database migration using Flask-Migrate
    
    

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Shows(db.Model):
    __tablename__ = 'Shows'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    venue = db.relationship('Venue')
    artist = db.relationship('Artist')

    def __init__(self, venue_id,artist_id,start_time):
        self.venue_id = venue_id
        self.artist_id = artist_id
        self.start_time = start_time

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def Venuedesc(self):
        return {
            'venue_id': self.venue.id,
            'venue_name': self.venue.name,
            'venue_image_link': self.venue.image_link,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M')
        }

    def Artistdesc(self):
        return {
            'artist_id': self.artist.id,
            'artist_name': self.artist.name,
            'artist_image_link': self.artist.image_link,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M')
        }
    

   

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data. DONE 
    venues = Venue.query.all()  # get all venues
    data = []    # defining data
    # creating a set for cities and states
    CityState = set()

    for venue in venues:
        CityState.add( (venue.city, venue.state) ) # Add the city and state as set together
    
    CityState = list(CityState) # to make the set an ordered list 
    # makes the sorting to according to the 2nd column which is the state not the city
    CityState.sort(key=itemgetter(1,0)) 

    presenttime = datetime.now()   

    for loc in CityState:
        # Check if there is a venue in the cityState
        venues_list = []
        for venue in venues:
            if (venue.city == loc[0]) and (venue.state == loc[1]):
                # Check how many upcoming shows in the venue
                venue_shows = Shows.query.filter_by(venue_id=venue.id).all()
                num_upcoming = 0
                for show in venue_shows:
                    if show.start_time > presenttime:
                        num_upcoming += 1

                venues_list.append({
                    "id": venue.id,
                    "name": venue.name,
                    "upcoming_shows": num_upcoming
                })
        # add to date 
        data.append({
            "city": loc[0],
            "state": loc[1],
            "venues": venues_list
        })

    return render_template('pages/venues.html', areas=data)
  
  #   data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: Done.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '').strip()
    # Use filter, not filter_by when doing LIKE search (i=insensitive to case)
    venues = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()   # Wildcards search before and after
    #print(venues)
    venue_list = []
    now = datetime.now()
    for venue in venues:
        venue_shows = Shows.query.filter_by(venue_id=venue.id).all()
        num_upcoming = 0
        for show in venue_shows:
            if show.start_time > now:
                num_upcoming += 1

        venue_list.append({
            "id": venue.id,
            "name": venue.name,
            "upcoming_shows": num_upcoming
        })
    response = {
        "count": len(venues),
        "data": venue_list
    } 
 
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: DONE
  # shows the venue page with the given venue_id
  venue = Venue.query.get(venue_id)
  
  # Corresponding to that venue you will get all the past shows
  past_shows = list(filter(lambda x: x.start_time < datetime.today(), venue.shows))
  #Corresponding to that venue you will get all the past shows
  upcoming_shows = list(filter(lambda x: x.start_time > datetime.today(), venue.shows))
  
  # Now map the past_shows as well as upcoming shows by mapping their artists
  past_shows = list(map(lambda x: x.Artistdesc(), past_shows))
  upcoming_shows = list(map(lambda x: x.Artistdesc(), upcoming_shows))
  
  # Convert the venue into dictionary form which in turn initialises all the fields
  data = venue.venuedictionary()
  
  # Then overiding some bit of data if required for other fields also 
  data['past_shows'] = past_shows
  data['past_shows_count'] = len(past_shows)
  
  return render_template('pages/show_venue.html', venue=data)
  #  Data 1:  "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  
  #   data 2: "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3: "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
      error = False
      try:
        venue = Venue()
        venue.name = request.form['name']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.address = request.form['address']
        venue.phone = request.form['phone']
        venue.facebook_link = request.form['facebook_link']
        temp_genres = request.form.getlist('genres')
        venue.genres = ','.join(tmp_genres)
        db.session.add(venue)
        db.session.commit()
      except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
      finally:
        db.session.close()
        if error:
            flash('An error occured. Venue ' +
                  request.form['name'] + ' Could not be listed!')
        else:
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed!')
      return render_template('pages/home.html')
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  Artists = Artist.query.order_by(Artist.name).all()  # Sort alphabetically
  data = []
  for artist in Artists:
    data.append({
      "id": artist.id,
      "name": artist.name
        })
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.get(artist_id)
  data = artist.artistdictionary()
  # The artist's the past shows
  pastshows = list(filter(lambda x: x.start_time < datetime.today(), artist.shows))
  #The artist's upcoming shows 
  upcomingshows = list(filter(lambda x: x.start_time > datetime.today(), artist.shows))
  
  # map past shows and upcoming shows by venue
  pastshows = list(map(lambda x: x.venuedictionary(), pastshows))
  upcomingshows = list(map(lambda x: x.venuedictionary(), upcomingshows))
  
  data['pastshows'] = pastshows
  data['upcomingshows'] = upcomingshows


  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  
  data = Artist.query.get(artist_id)
  
  if data:
    artist = Artist.artistdictionary(data)
    form.name.data = artist["name"]
    form.genres.data = artist["genres"]
    form.city.data = artist["city"]
    form.state.data = artist["state"]
    form.phone.data = artist["phone"]
    form.facebook_link.data = artist["facebook_link"]
    form.website.data = artist["website"]
    form.image_link.data = artist["image_link"]
    form.seeking_venue.data = artist["seeking_venue"]
    form.seeking_description.data = artist["seeking_description"]
    return render_template('forms/edit_artist.html', form=form, artist=artist)  
  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  # TODO: populate form with fields from artist with ID <artist_id> DONE

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
    form = ArtistForm(request.form)
    artistquery= Artist.query.get(artist_id)

    if not artistquery: # if user put a not available venue id it woudl return to home page
      return redirect(url_for('index'))
    else: 
      if form.validate():
            seeking_venue = False
            seeking_description = ''
            if 'seeking_venue' in request.form:
                seeking_venue = request.form['seeking_venue'] == 'y'
            if 'seeking_description' in request.form:
                seeking_description = request.form['seeking_description']
            setattr(artistquery, 'name', request.form['name'])
            setattr(artistquery, 'genres', request.form.getlist('genres'))
            setattr(artistquery, 'city', request.form['city'])
            setattr(artistquery, 'state', request.form['state'])
            setattr(artistquery, 'phone', request.form['phone'])
            setattr(artistquery, 'website', request.form['website'])
            setattr(artistquery, 'facebook_link', request.form['facebook_link'])
            setattr(artistquery, 'image_link', request.form['image_link'])
            setattr(artistquery, 'seeking_description', seeking_description)
            setattr(artistquery, 'seeking_venue', seeking_venue)
            Artist.update(artistquery)
            return redirect(url_for('show_artist', artist_id=artist_id))
      else:
          print(form.errors)
      


  # artist record with ID <artist_id> using the new attributes

 # return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venuequery= Venue.query.get(venue_id)
  if not venuequery: # if user put a not available venue id it woudl return to home page
    return redirect(url_for('index'))
  else:
    form = VenueForm()
    
    venue = Venue.venuedictionary(venuequery)
    form.name.data = venue["name"]
    form.genres.data = venue["genres"]
    form.address.data = venue["address"]
    form.city.data = venue["city"]
    form.state.data = venue["state"]
    form.phone.data = venue["phone"]
    form.website.data = venue["website"]
    form.facebook_link.data = venue["facebook_link"]
    form.seeking_talent.data = venue["seeking_talent"]
    form.description.data = venue["description"]
    form.image_link.data = venue["image_link"]  
  # TODO: populate form with values from venue with ID <venue_id> done
    return render_template('forms/edit_venue.html', form=form, venue=data)
  

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
    data = []
    shows = Shows.query.all()
    for show in shows:
        data.append({
            'venue_id': show.venue_id,
            'venue_name': show.venue.name,
            'artist_id': show.artist_id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time.isoformat()
        }) 
    return render_template('pages/shows.html', shows=data)       
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]
  

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
    error = False
    # query only artists who seak venues
    artists = Artist.query.with_entities(
        Artist.id, Artist.name, Artist.seeking_venue).filter_by(seeking_venue=True)
    # query only venues who seak talent
    venues = Venue.query.with_entities(
        Venue.id, Venue.name, Venue.seeking_talent).filter_by(seeking_talent=True).all()
    artists_list = [(artist.id, artist.name) for artist in artists]
    venues_list = [(venue.id, venue.name) for venue in venues]
    form.artist_id.choices = artists_list
    form.venue_id.choices = venues_list
    if form.validate_on_submit():
        try:
            show = Show()
            form.populate_obj(show)
            db.session.add(show)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
            if error:  
              # e.g., flash('An error occurred. Show could not be listed.')
              # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
                flash(
                    'Oops! Something wrong happened, your show could not be listed!', 'error')
            else: # on successful db insert, flash success
                flash('Show was successfully listed!')
            return render_template('pages/home.html')  
  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
