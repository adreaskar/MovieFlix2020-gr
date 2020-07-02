from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, render_template, request, jsonify, redirect, Response, url_for
import json, hashlib, os, re, time
 
mongodb_hostname = os.environ.get("MONGO_HOSTNAME","localhost")
client = MongoClient('mongodb://'+mongodb_hostname+':27017/')

db = client['MovieFlix']
users = db['Users']
movies = db['Movies']


app = Flask(__name__)


# Global variables
rating_count = 0
rating_val = 0

outcome =""
outcome2 =""
outcome3 =""

# Index --------------------------------------------------------------------------------------------------------------------
@app.route('/')
def index():

    # Hardcoded Admin User ------------------------------
    check = users.find().count()
    if check == 0:
        hc_pass = "admin"
        hc_pass = hc_pass.encode('utf-8')
        hc_pass = hashlib.sha256(hc_pass).hexdigest()

        hc_admin={}
        hc_admin= {
            "User name" : "Andreas",
            "User email" : "admin@admin.com",
            "User password" : hc_pass,
            "User comments": [
            ],
            "User category" : "admin",
            "User ratings" : [

            ]
        }

        ad = {"User name": hc_admin['User name'],
                "User email": hc_admin['User email'],
                "User password":hc_admin['User password'],
                "User comments":hc_admin['User comments'],
                "User category":hc_admin['User category'],
                "User ratings":hc_admin['User ratings']}
        users.insert_one(ad)

    return render_template('index.html')

# Register new user --------------------------------------------------------------------------------------------------------
@app.route('/', methods=['POST'])
def register():        

    register_name = request.form['name']
    register_email = request.form['email']
    register_password = request.form['password'].encode('utf-8')

    hashed_password = hashlib.sha256(register_password).hexdigest()

    data={}
    data= {
        "User name" : register_name,
        "User email" : register_email,
        "User password" : hashed_password,
        "User comments": [

        ],
        "User category" : "user",
        "User ratings" : [

        ]
    }

    if users.find({"User email":data["User email"]}).count() == 0 :
        user = {"User name": data['User name'], "User email": data['User email'], "User password":data['User password'], "User comments":data['User comments'],"User category":data['User category'], "User ratings":data['User ratings']}
        users.insert_one(user)
        return redirect(url_for("login"))
    else:
        return render_template('error.html', x = 1)    

# Login user ---------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':

        login_email = request.form['login_email']
        login_password = request.form['login_password'].encode('utf-8')
        
        hashed_login_password = hashlib.sha256(login_password).hexdigest()

        valid_user = users.find_one({"User email":login_email})
        valid_password = users.find_one({"User password":hashed_login_password})

        # Find user's name ----------------------------------------
        if valid_password is None or valid_user is None :
            return render_template('error.html', x=2)
        else:
            u = users.find_one({"User password":hashed_login_password})
            name = u['User name']
            u_type = u['User category']
            if u_type == "user":
                return redirect(url_for("user_home", user_name=name))
            else:
                return redirect(url_for("admin_home", user_name=name))    
    else:
        return render_template('login.html', title='Login')
    
# User home ----------------------------------------------------------------------------------------------------------------
@app.route('/user_home', methods=['POST', 'GET'])
def user_home():


    # Delete account ----------
    if request.method == 'POST':
        name = request.args['user_name']
        acc = users.find_one({"User name":name})
        users.remove({"_id":acc['_id']})
        return render_template('delete_user.html', name=name)
    else:
        name = request.args['user_name']
        usr = users.find_one({"User name":name})
        mail = usr['User email']
        return render_template('users/user_home.html', user_name= name, mail = mail, title='User Profile')

# Admin home ---------------------------------------------------------------------------------------------------------------
@app.route('/admin_home', methods=['POST', 'GET'])
def admin_home():

    # Delete account --------------------------------------------
    if request.method == 'POST':
        name = request.args['user_name']
        acc = users.find_one({"User name":name})
        users.remove({"_id":acc['_id']})
        return render_template('delete_user.html', name = name)
    else:
        name = request.args['user_name']
        usr = users.find_one({"User name":name})
        mail = usr['User email']

        return render_template('admin_home.html', user_name= name, mail=mail, title='User Profile')        

# Admin comment delete -----------------------------------------------------------------------------------------------------
@app.route('/admin_comment_delete', methods=['POST', 'GET'])
def admin_comment_delete():

    if request.method == 'POST':
        
        # Find and remove comment from movie ----------------------------------
        quer = request.form.get('adm_com_del')
        outcome = movies.find_one({"Comments":quer})
        titl = outcome['Title']
        movies.update_one({"_id":outcome['_id']}, {"$pull": {"Comments":quer}})

        # Cut the movie title from the comment
        usr = quer.split(maxsplit=2)
        usr_com = usr[2]

        # Find the user that typed the comment ------------------------
        outcomem = users.find_one({"User comments":{"$regex":usr_com}})
        usr_comment = titl + " : " + usr_com

        # Remove it from user's comments --------------------------------------------------
        users.update_one({"_id":outcomem['_id']}, {"$pull": {"User comments":usr_comment}})
        

        return render_template('message.html', y=8)
    else:
        comments = movies.distinct("Comments")
        return render_template('admin_comment_delete.html',comments = comments, title='Remove Comments')



# Movie Search -------------------------------------------------------------------------------------------------------------
@app.route('/movie_search', methods=['POST','GET'])
def movie_search():

    global outcome2
    global outcome3
    global outcome
    
    if request.method == 'POST':

        # Queries recieved from form --------
        quer = request.form['search_title']
        quer2 = request.form['search_year']
        quer3 = request.form['search_actors']

        # Find the movie with the requested query
        outcome = movies.find({"Title":{"$regex":re.compile(quer, re.IGNORECASE)}})
        outcome2 = movies.find({"Year":quer2})
        outcome3 = movies.find({"Actors":quer3})

        mail = request.args['user_mail']

        # Set outcome to None if field is empty
        if quer == "":
            outcome = None

        if quer2 == "":
            outcome2 = None

        if quer3 == "":
            outcome3 = None

        # Determine which field has been given input ---------------------------
        if outcome is not None:

            count = outcome.count()
            
            if count > 0:
                return redirect(url_for("movie_select_title", user_mail = mail))
            else:   
                return render_template('error.html', x=7, user_mail = mail)

        elif outcome2 is not None:

            count = outcome2.count()
            
            if count > 0:
                return redirect(url_for("movie_select_year", user_mail = mail))
            else:   
                return render_template('error.html', x=5, user_mail = mail)  

        elif outcome3 is not None:

            count = outcome3.count()

            if count > 0:
                return redirect(url_for("movie_select_actor", user_mail = mail))
            else:   
                return render_template('error.html', x=6, user_mail = mail)

        else:
            return render_template('error.html', x=4, user_mail = mail)
    else:
        return render_template('movies/movie_search.html', title='Movie Search')

# Movie Select by Title -----------------------------------------------------------------------------------------------------
@app.route('/movie_select_title', methods=['POST','GET'])
def movie_select_title():
    
    global outcome

    if request.method == 'POST':
        
        mail = request.args['user_mail']
        titl = request.form.get('movie_sel')
        ar = titl.split(" ",1)
        titl = ar[0]

        movie = movies.find_one({"Title":titl, "Year":ar[1]})

        ye = ar[1]
        pl = movie['Description']
        ac = movie['Actors']
        ra = movie['Rating']
        co = movie['Comments']

        return render_template('movies/movie_details.html', user_mail = mail, titl = titl, year = ye, plot = pl, actors = ac, rating = ra, comments = co, title='Movie Details')
    else:
        return render_template('movies/movie_select_title.html', title='Select Movie', title_movies = outcome)

# Movie Select by Year -----------------------------------------------------------------------------------------------------
@app.route('/movie_select_year', methods=['POST','GET'])
def movie_select_year():
    
    global outcome2

    if request.method == 'POST':
        
        mail = request.args['user_mail']
        titl = request.form.get('movie_sel')

        movie = movies.find_one({"Title":titl})

        ye = movie['Year']
        pl = movie['Description']
        ac = movie['Actors']
        ra = movie['Rating']
        co = movie['Comments']

        return render_template('movies/movie_details.html', user_mail = mail, titl = titl, year = ye, plot = pl, actors = ac, rating = ra, comments = co, title='Movie Details')
    else:
        return render_template('movies/movie_select_year.html', title='Select Movie', year_movies = outcome2)

# Movie Select by Actor -----------------------------------------------------------------------------------------------------
@app.route('/movie_select_actor', methods=['POST','GET'])
def movie_select_actor():
    
    global outcome3

    if request.method == 'POST':
        
        mail = request.args['user_mail']
        titl = request.form.get('movie_sel')
        ar = titl.split(" ",1)
        titl = ar[0]

        movie = movies.find_one({"Title":titl, "Year":ar[1]})

        ye = ar[1]
        pl = movie['Description']
        ac = movie['Actors']
        ra = movie['Rating']
        co = movie['Comments']

        return render_template('movies/movie_details.html', user_mail = mail, titl = titl, year = ye, plot = pl, actors = ac, rating = ra, comments = co, title='Movie Details')
    else:
        return render_template('movies/movie_select_actor.html', title='Select Movie', actor_movies = outcome3)

# Movie User Action --------------------------------------------------------------------------------------------------------
@app.route('/movie_user_action', methods=['POST','GET'])
def movie_user_action():

    global rating_count
    global rating_val

    if request.method == 'POST':
        comm = request.form['user_comment']
        usr_rat = request.form['user_rating']
        
        ti = request.args['title']
        mail = request.args['user_mail']

        outcome = movies.find_one({"Title":ti})
        outcome_usr = users.find_one({"User email":mail})
        
        if usr_rat:

            # Compute average rating ---------------------------------------------------------------------
            rating_count = rating_count + 1
            rating_val = rating_val + int(usr_rat)
            rating_total = rating_val / rating_count
            rating_total = round(rating_total,1)

            # Add rating to both db's --------------------------------------------------------------------
            movies.update_one({"_id":outcome['_id']} , {"$set": {"Rating":rating_total}})
            users.update_one({"_id":outcome_usr['_id']}, {"$push": {"User ratings":ti + " : " + usr_rat}})
        if comm:
            users.update_one({"_id":outcome_usr['_id']}, {"$push": {"User comments":ti + " : " + comm}})
            movies.update_one({"_id":outcome['_id']}, {"$push": {"Comments":mail + " : " + comm}})

        return render_template('message.html', y=6)
    else:
        return render_template('movies/movie_user_action.html', title='Comment / Rate Movie')

# Movie Actions ------------------------------------------------------------------------------------------------------------
@app.route('/movie_actions')
def movie_actions():

    return render_template('movies/movie_actions.html', title='Movies Actions') 

# Movie Add ----------------------------------------------------------------------------------------------------------------
@app.route('/movie_add', methods=['POST', 'GET'])
def movie_add():

    if request.method == 'POST':
        movie_title = request.form['title']
        movie_year = request.form['year']
        movie_plot = request.form['plot']
        movie_actors = request.form['actors']

        # Remove commas from actors string and keep the names
        counter = movie_actors.count(',')
        movie_actors = movie_actors.split(',',counter)

        movie_data={}
        movie_data={
            "Title":movie_title,
            "Year":movie_year,
            "Description":movie_plot,
            "Actors": [
                
            ],
            "Rating": 0,
            "Comments": [
                
            ]
        }

        # Add all given actors to DB ---------
        for actor in movie_actors:
            movie_data["Actors"].append(actor)

        movie = {"Title": movie_data['Title'], "Year": movie_data['Year'], "Description": movie_data['Description'], "Actors": movie_data['Actors'], "Rating": movie_data['Rating'], "Comments": movie_data['Comments']}
        movies.insert_one(movie)

        return render_template('message.html', y=4)
    else:
        return render_template('movies/movie_add.html', title='Add Movie')

# Movie Remove -------------------------------------------------------------------------------------------------------------
@app.route('/movie_remove', methods=['POST', 'GET'])
def movie_remove():

    if request.method == 'POST':
        
        l = []

        # Find all movies with same title --------------------------------------------
        movie_title = request.form['title_remove']
        mov = movies.find({"Title":{"$regex":re.compile(movie_title, re.IGNORECASE)}})

        # Make a list and sort to find oldest movie
        for x in mov:
            l.append(x["Year"])
        f = sorted(l)
        f = f[0]

        # Remove the movie ------
        movies.remove({"Year":f})

        return render_template('message.html',y=1)
    else:
        return render_template('movies/movie_remove.html', title='Remove Movie')

# Movie Update -------------------------------------------------------------------------------------------------------------
@app.route('/movie_update', methods=['POST', 'GET'])
def movie_update():

    if request.method == 'POST':
        
        movie_update_title = request.form['title_search']
        movupdt = movies.find_one({"Title":movie_update_title})

        if movupdt is not None:

            updated_title = request.form['title_update']
            updated_year = request.form['year_update']
            updated_plot = request.form['plot_update']
            updated_actors = request.form['actors_update']
            removed_actor = request.form['actors_remove']

            # Remove commas from actors string and keep the names
            counter = updated_actors.count(',')
            updated_actors = updated_actors.split(',',counter)
            
            if updated_title:
                movies.update_one({"_id":movupdt['_id']} , {"$set": {"Title":updated_title}})
            if updated_year:
                movies.update_one({"_id":movupdt['_id']} , {"$set": {"Year":updated_year}})
            if updated_plot:
                movies.update_one({"_id":movupdt['_id']} , {"$set": {"Description":updated_plot}})
            if updated_actors:
                for actor in updated_actors:
                    movies.update({"_id":movupdt['_id']}, {"$push": {"Actors":actor}})
            if removed_actor:
                movies.update({"_id":movupdt['_id']}, {"$pull": {"Actors":removed_actor}})

            return render_template('message.html', y=5)
            
        else:
            return render_template('error.html', x=4)  
    else:
        return render_template('movies/movie_update.html', title='Update Movie Details')



# User Comments ------------------------------------------------------------------------------------------------------------
@app.route('/user_com', methods=['POST', 'GET'])
def user_com():
   
    user = request.args['user_mail']
    outcome = users.find_one({"User email":user})
    coms = outcome['User comments']

    return render_template('users/user_com.html', title="User's Comments", comments = coms, mail = user)

# Delete Comment -----------------------------------------------------------------------------------------------------------
@app.route('/comment_delete', methods=['POST', 'GET'])
def comment_delete():
   
    if request.method == 'POST':
        
        # Delete comment from User db ----------------------------------------------
        select = request.form.get('com_del')
        user = request.args['user_mail']
        outcome = users.find_one({"User email":user})
        users.update_one({"_id":outcome['_id']}, {"$pull": {"User comments":select}})

        # Delete comment from Movies db --------------------------------------
        select = select.split(maxsplit=2)
        com = select[2]
        outcomem = movies.find_one({"Comments":{"$regex":com}})
        com = user + " : " + com
        movies.update_one({"_id":outcomem['_id']}, {"$pull": {"Comments":com}})

        return render_template('message.html', y=7)
    else:
        user = request.args['user_mail']
        outcome = users.find_one({"User email":user})
        coms = outcome['User comments']
        return render_template('comment_delete.html', title='Delete comment', comments = coms )

# User Ratings -------------------------------------------------------------------------------------------------------------
@app.route('/user_rat', methods=['POST', 'GET'])
def user_rat():
   
    user = request.args['user_mail']
    outcome = users.find_one({"User email":user})
    rats = outcome['User ratings']
    

    return render_template('users/user_rat.html', title="User's Ratings", ratings = rats, mail = user)

# Delete Rating ------------------------------------------------------------------------------------------------------------
@app.route('/rating_delete', methods=['POST', 'GET'])
def rating_delete():
   
    if request.method == 'POST':
        
        # Delete rating from User db ----------------------------------------------
        select = request.form.get('rat_del')
        user = request.args['user_mail']
        outcome = users.find_one({"User email":user})
        users.update_one({"_id":outcome['_id']}, {"$pull": {"User ratings":select}})

        return render_template('message.html', y=9)
    else:
        user = request.args['user_mail']
        outcome = users.find_one({"User email":user})
        rats = outcome['User ratings']
        return render_template('rating_delete.html', title='Delete comment', ratings = rats )

# User Actions -------------------------------------------------------------------------------------------------------------
@app.route('/user_actions')
def user_actions():

    return render_template('users/user_actions.html', title='Users Actions')            

# User Category ------------------------------------------------------------------------------------------------------------
@app.route('/user_category', methods=['POST', 'GET'])
def user_category():

    if request.method == 'POST':
        
        user_cemail = request.form['user_promote']
        usc = users.find_one({"User email":user_cemail})
        users.update_one({"_id":usc['_id']} , {"$set": {"User category":"admin"}})

        return render_template('message.html', y=3)
    else:
        return render_template('users/user_category.html', title='Promote User')

# User Remove --------------------------------------------------------------------------------------------------------------
@app.route('/user_remove', methods=['POST', 'GET'])
def user_remove():

    if request.method == 'POST':
        
        user_email = request.form['user_remove']
        us = users.find_one({"User email":user_email})
        us_cat = us['User category']

        if us_cat == "user":
            users.remove({"_id":us['_id']})
            return render_template('message.html', y=2)
        else:
            return render_template('error.html', x=3)
    else:
        return render_template('users/user_remove.html', title='Remove User')       



# Run Flask App ------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
