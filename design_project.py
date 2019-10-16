import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# nltk.download("stopwords")
# nltk.download('punkt')

from flask import Flask, render_template
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'MyDB'

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/recommend")
def recommend():
    return render_template("recommend.html")

@app.route("/signup")
def signup():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        dob = details['dob']
        mail = details['mail']
        phone = details['phone']
        password = details['password']
        gender = details['gender']
        address = details['address']
        district = details['district']
        town = details['town']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO MyUsers(FNAME,LNAME,DOB,EMAIL,PHONE,PASSWORD,GENDER,ADDRESS,DISTRICT,TOWN) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, )", (firstName, lastName,dob,mail,phone,password,gender,address,district,town))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template("signup")

    
if __name__ == "__main__":
    app.run(debug=True)


def Recommender(sentance):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentance)
    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    Specialists = ['Addiction psychiatrist', 'Immunologist', 'Cardiologist', 'Dermatologist', 'Developmental pediatrician',
                   'Gastroenterologist', 'Gynecologist', 'Hematologist', 'Nephrologist', 'Neurologist',
                   'Oncologist', 'Ophthalmologist', 'Orthopedic surgeon', 'ENT', 'Pediatrician', 'Psychiatrist', 'Urologist']

    Collection = {0: ['addiction', 'alcohol', 'drugs', 'concentration'],
                  1: ['allergy', 'immunity', 'pollen', 'sneezing', 'itchy', 'rash', 'swollen'],
                  2: ['heart', 'blood', 'pain', 'beat', 'chest', 'dizzy', 'dizziness', 'faint', 'cholesterol', 'leg'],
                  3: ['skin', 'hair', 'nail', 'acne'],
                  4: ['autism', 'inactive', 'child', 'kid', 'baby', 'disabilities', 'mental', 'communication', 'response', 'delay', 'attention'],
                  5: ['heartburn', 'digestion', 'stomach', 'pain', 'cramps'],
                  6: ['pregnancy', 'birth', 'fertility', 'women', 'menstruation', 'disorders'],
                  7: ['blood', 'clotting', 'blood-clotting', 'anemia', 'weakness', 'weight', 'infection', 'bruising', 'excessive', 'bleeding', 'energy'],
                  8: ['pressure', 'high', 'blood', 'diabetes', 'kidney', 'urine', 'back', 'smelly', 'appetite', 'skin', 'yellow', 'weight'],
                  9: ['headache', 'chronic', 'pain', 'dizziness', 'movement', 'problems', 'weakness', 'loss', 'consciousness', 'memory', 'confusion', 'sleep'],
                  10: ['cancer'],
                  11: ['eye', 'vision', 'eyes', 'see', 'pain'],
                  12: ['shoulder', 'pain', 'bone', 'twisted', 'angles', 'joints', 'numb', 'hands', 'swollen', 'bend', 'wrist', 'neck', 'broken', 'painful', 'stiff', 'muscles'],
                  13: ['ear', 'ears', 'nose', 'throat', 'balance', 'hearing', 'infection', 'dizziness'],
                  14: ['child', 'kid', 'baby', 'new', 'born', 'fever', 'cough'],
                  15: ['mental', 'depression', 'concentration', 'addiction', 'temper', 'anxiety', 'disorder', 'illogical', 'thoughts', 'memory'],
                  16: ['urine', 'infection', 'urinating', 'pelvic', 'pain', 'fertility', 'men', 'erectile']
                  }
    Recom_list = [0] * 17
    for i in filtered_sentence:
        for k, v in Collection.items():
            if i in v:
                Recom_list[k] += 1
    print('Please consult :', Specialists[Recom_list.index(max(Recom_list))])


sent = input('Enter your symptoms:')
Recommender(sent)
