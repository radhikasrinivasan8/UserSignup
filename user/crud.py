from user import get_model
from flask import Blueprint, Flask, redirect, render_template, request, url_for
import requests
from flask_oauthlib.client import OAuth
#from flask_dance.contrib.facebook import make_facebook_blueprint, facebook

oauth = OAuth()

# facebook = oauth.remote_app('facebook',
#     base_url='https://graph.facebook.com/',
#     request_token_url=None,
#     access_token_url='/oauth/access_token',
#     authorize_url='https://www.facebook.com/dialog/oauth',
#     consumer_key=2553887357960034,
#     consumer_secret="2239a99aad43eff28a8f59c93d856c2c",
#     request_token_params={'scope': 'email'}


crud = Blueprint('crud', __name__)

#facebook_blueprint = make_facebook_blueprint(consumer_key='2553887357960034', consumer_secret="2239a99aad43eff28a8f59c93d856c2c")
#crud.register(facebook_blueprint, url_prefix='/facebook_login')

@crud.route('/facebook')
def facebook_login():
    if not facebook.authorized:
        return redirect(url_for('crud.signup'))

#app = Flask(__name__)
@crud.route('/user/<id>')
def see(id):
    user = get_model().read(id)
    # print(user)
    print("User details are : crud.py:11")
    print(user)
    # print(")))))))))))")
    return render_template("user.html", users=user)
    
@crud.route('/', methods=['GET', 'POST'])
def home():
    
    return redirect(url_for('crud.signup'))


@crud.route('/form',methods=['GET','POST'])   
def form():
    return render_template("form.html")

@crud.route('/signup/',methods=['GET','POST'])
def signup():
    # print(request.method)
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        user = get_model().create(data)
        # print(user)
        url = "https://www.google.com/recaptcha/api/siteverify"
        cap_res = data.get("g-recaptcha-response")
        params = {
            'secret':'6LdUGpIUAAAAAO2ASyVLPqRIYBVDWoeNVXj1ljgm',
            'response':cap_res
        }
        res = requests.post(url,params=params)
        if res.json()['success']:
            return redirect(url_for('crud.form'))
        
    return render_template("signup.html", action="Signup", user={})

@crud.route('/login', methods = ['GET','POST'])
def login():
    error = None  
    if request.method == 'POST':
        
        user = get_model().nemail(str(request.form['email']))
        if request.form['email']==user['email'] and request.form['password']== user['password'] :
            if user['admin']=='yes':
                return redirect(url_for('crud.view'))
            else:
                return render_template('validuser.html',user=user['email'])
        else:    
             
            return render_template('form.html')
    #return render_template('crud.view')
    
@crud.route('/view',methods=['GET','POST'])
def view():
    
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    users, next_page_token = get_model().list1(cursor=token)
    
    return render_template(
        "view.html",
        users=users,
        next_page_token=next_page_token)

# [END list]



@crud.route('/user/<id>/edit', methods=['GET', 'POST'])
def see_edit(id):
    user = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        user = get_model().update(data, id)
        print("crud.py line 148")
        print(data)

        return redirect(url_for('.view', id=user['id']))

    return render_template("signup.html", action="Edit", user=user)

@crud.route('/user/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.view'))

if __name__ == "__main__":
    app.run(debug=True)