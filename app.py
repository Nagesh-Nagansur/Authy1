from flask import Flask,render_template,request,jsonify
from authy.api import AuthyApiClient
# from authy.api
# from flask_sqlalchemy import SQLAlchemy
#

app =Flask(__name__)
#
# class User(db.Model):
#     username = db.Column(db.String(80),primery_key=True)
#     password = db.Column(db.String(80))
#home of app
users=[
{
"name":"nagesh",
"password":"xyz"
}
]

authy_api = AuthyApiClient('AUTH_API_KEY')
user = authy_api.users.create(
    email='nagesh.nagansur@coditas.com',
    phone='8180933388', #in (xxx-xxx-xxxx)format
    country_code=+91)
authy_api = AuthyApiClient('Jk8o04b0SJ9x99x2IAzrlHBFKg1YoqAz')
sms = authy_api.users.request_sms(332712599)

if user.ok():
    authy_id = user.id
    print(user.id)

else:
    print(user.errors())



@app.route('/home',methods=["GET"])
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def log_in():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        # data=request.get_json()

        for user in users:
            if user["name"] == username:
                if user["password"] == password:

                    # return jsonify({"message":"Found"})
                    return render_template('verify.html',dummy="Correct Password")


                else:
                    return jsonify({"message":"wrong password"})

            else:
                return jsonify({"message":"no user Found"})

    else:
        return render_template('login.html')


@app.route('/verify',methods=['GET','POST'])
def verify():
    authy_id=332712599

    token=request.form['smscode']

    verification = authy_api.tokens.verify(authy_id, token=int(token))
    print(token)
    if verification.ok():
        return render_template("home.html",user=authy_id)
    else:
        return "wrong otp"











app.run(port=5002,debug=True)
