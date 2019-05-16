from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
import json
from flask_mail import Mail
from flask_mail import Message

with open('config.json','r') as c:
    params=json.load(c)["params"]

local_server=True
app = Flask(__name__)
app.secret_key='dont tell anyone'
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI']=params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['your_mail'],
    MAIL_PASSWORD=params['your_pass']
)

db=SQLAlchemy(app)
mail=Mail(app)
class Myreg(db.Model):
    id = db.Column(db.Integer, autoincrement=True, unique=True, nullable=False)
    name=db.Column(db.String(20),primary_key=True,unique=True,nullable=False)
    email=db.Column(db.String(20),unique=True,nullable=False)
    password=db.Column(db.String(8),unique=True,nullable=False)

class Mylist(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    type=db.Column(db.String(20),unique=False,nullable=False)
    title=db.Column(db.String(50),unique=True,nullable=False)
    price=db.Column(db.Integer,unique=False,nullable=False)
    img_file = db.Column(db.String(20), unique=False)
    slug = db.Column(db.String(20), unique=False)

class Mylistdress(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    type=db.Column(db.String(20),unique=False,nullable=False)
    title=db.Column(db.String(50),unique=True,nullable=False)
    price=db.Column(db.Integer,unique=False,nullable=False)
    img_file = db.Column(db.String(20), unique=False)
    slug = db.Column(db.String(20), unique=False)


@app.route("/go.html",methods=['GET','POST'])
def go():
    params['user_name']=""
    params['user_email'] =""
    result = Mylist.query.all()
    resultdress = Mylistdress.query.all()
    return render_template('go.html',result=result,resultdress=resultdress,params=params)

@app.route("/",methods=['GET','POST'])
@app.route("/home",methods=['GET','POST'])
@app.route("/index.html",methods=['GET','POST'])
def home():
    result = Mylist.query.all()
    resultdress = Mylistdress.query.all()
    return render_template('index.html',result=result,resultdress=resultdress)

@app.route("/product.html",methods=["GET","POST"])
def product():
    valve_title =request.args.get("valve_title")
    valve_price = request.args.get("valve_price")
    valve_img = request.args.get("valve_img")
    target_title=None
    target_price = None
    target_img = None
    result = Mylist.query.all()
    for r in result:
        if r.title==valve_title:
            target_title = valve_title
            target_price = valve_price
            target_img = valve_img
            break
    if target_title is None:
        resultdress = Mylistdress.query.all()
        for s in resultdress:
            if s.title == valve_title:
                target_title = valve_title
                target_price = valve_price
                target_img = valve_img
                break
    return render_template('product.html',title=target_title,price=target_price,img=target_img)

@app.route("/intrested.html",methods=["GET","POST"])
def intrested():
    valve_title =request.args.get("valve_title")
    valve_price = request.args.get("valve_price")
    valve_img = request.args.get("valve_img")
    target_title=None
    target_price = None
    target_img = None
    result = Mylist.query.all()
    for r in result:
        if r.title==valve_title:
            target_title = valve_title
            target_price = valve_price
            target_img = valve_img
            break
    if target_title is None:
        resultdress = Mylistdress.query.all()
        for s in resultdress:
            if s.title == valve_title:
                target_title = valve_title
                target_price = valve_price
                target_img = "/static/"+valve_img
                break
    if params['user_email'] is "":
        m = "Please Login!"
        return redirect(url_for("home",params=params))
    else:
        email = params['user_email']
        m = "check your mail for details"
        subject = "CHECK OUT-MODIST"
        msg = Message(
            sender=params['your_mail'],
            recipients=[email],
            subject=subject
        )
        msg.html = '''<div> 
                            <img src="'''+target_img+'''">
                            <h3>'''+target_title+'''</h3><hr>
    				         <p class="price"><span>$'''+target_price+'''.00</span></p><br>
    				         <p>A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth.</p>
    				         <p>On her way she met a copy. The copy warned the Little Blind Text, that where it came from it would have been rewritten a thousand times and everything that was left from its origin would be the word "and" and the Little Blind Text should turn around and return to its own, safe country. But nothing the copy said could convince her and so it didn’t take long until a few insidious Copy Writers ambushed her, made her drunk with Longe and Parole and dragged her into their agency, where they abused her for their.
						      </p>
                     </div>'''
        mail.send(msg)
    return ('',204)


#request.form.get("q")... this fnding inside the same page
@app.route("/search.html",methods=['GET'])
def search():
        q =request.args.get("q")
        d=str(q)
        var="%"+d + "%"
        myresult = (Mylist.query.filter(Mylist.type.like(var)| Mylist.title.like(var)|Mylist.price.like((var))).all())
        myresult2 = (Mylistdress.query.filter(Mylistdress.type.like(var)| Mylistdress.title.like(var)|Mylistdress.price.like((var))).all())
        myresult3=myresult+myresult2
        return render_template('search.html',result=myresult3)
        myresult3=None


@app.route("/shop.html")
def shop():
    return render_template('shop.html')

@app.route("/login.html",methods=['GET','POST'])
def login():
    if (request.method == 'POST'):
        email = request.form["email"]
        params['user_email']=email
        password = request.form["pass"]
        check = Myreg.query.filter_by(email=email,password=password).first()
        if not check:
            flash('Please check your login details and try again.')
        else:
            name=check.name
            params['user_name']=name
            return redirect(url_for("welcome",params=params))
    return render_template('login.html',params=params)

@app.route("/signup.html",methods=['GET','POST'])
def signup():
    if (request.method=='POST'):
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["pass"]
        entry=Myreg(name=name,email=email,password=password)
        db.session.add(entry)
        db.session.commit()
        subject = "MODIST WELCOMES YOU! "
        msg = Message(
            sender=params['your_mail'],
            recipients=[email],
            subject=subject
        )
        msg.html = "Hello,<br>New Member!!"
        mail.send(msg)
    return render_template('signup.html',params=params)

@app.route("/welcome.html",methods=["GET","POST"])
def welcome():
    result = Mylist.query.all()
    resultdress = Mylistdress.query.all()
    if params['user_email'] is "":
        email=None
    else:
        email = params['user_email']
    if email is None:
        return redirect(url_for("home", result=result, resultdress=resultdress))
    else:
        return render_template('welcome.html', result=result, resultdress=resultdress, params=params)




@app.route("/contact.html")
def contact():
    return render_template('contact.html')

if __name__=="__main__":
    app.run(debug=True)
