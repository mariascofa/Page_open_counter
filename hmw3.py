from flask import Flask, render_template, make_response, session, request

app = Flask(__name__)
app.secret_key = b'=+e34'


@app.route ("/")
def index ():
    """This page will display how many times it has been opened by the user.
     Also it will show if user has been authorized on the site (added to the session) and his username."""
    visit_counter = 0
    if session.get('visited'):
        visit_counter = session['visited']
    else:
        session['visited'] = 0
    session['visited'] += 1
    us=session.get ('username')
    if 'username' in session:
        response = make_response(render_template('index2.html', username=us, visited=visit_counter,
                                                 ftitle = "You have entered the system under username:",
                                                 title = "You have been here", title2= "times"))
    if 'username' not in session:
        response = make_response(render_template('index2.html',visited=visit_counter, ftitle = "It is Anonymous user",
                                                 title = "You have been here", title2= "times"))
    return  response

@app.route('/login', methods=['GET', 'POST'])
def login():
    """This page will accept two types of GET and POST requests. When user open this page for the first time, page shows
    form for entering username. System add this user to the session, and display the result in template.
    If user wants to go to this page again and he is logged in, he will get info that he is logged in and his username."""
    us = session.get('username')
    if 'username' in session:
        response = make_response(render_template('index2.html',ftitle = "You have entered the system under username:",
                                                 username=us))
    elif request.method == 'GET':
        response = make_response(render_template('index.html'))
    elif request.method == 'POST':
        username = request.form['username']
        response = make_response(render_template('index2.html', ftitle = "You have entered the system under username:",
                                                 username = username))
        session['username'] = username
    return response

@app.route('/logout')
def logout():
    """This page should clean up the session if the user is authorized in the system."""
    if 'username' in session:
        del session ['username']
        response = make_response(render_template('logout.html', title = "Your session has been cleared!"))
    else:
        response = make_response(render_template('logout.html', title = "Session can't be cleaned. User didn't log in."))
    return response

# @app.route('/logout')
# def logout():
#     """This page should clean up the session if the user is authorized in the system."""
#     if 'username' in session:
#         session.clear()
#         response = make_response(render_template('logout.html', title = "Your session has been cleared!"))
#     else:
#         response = make_response(render_template('logout.html', title = "Session can't be cleaned. User didn't log in."))
#     return response

app.run(debug=True, port=5003)


