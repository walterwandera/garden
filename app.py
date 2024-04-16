from flask import *
import pymysql
from at_sms import *
from mpesa import *
app= Flask(__name__)

connection= pymysql.connect(host='localhost', user='root', password='', database='truham_db')

cursor= connection.cursor()

@app.route('/')
def home():
   '''
   Home route
   '''
   sql_detergents = 'SELECT * FROM  products WHERE product_category = "detergents" '

   cursor.execute(sql_detergents)
   detergents= cursor.fetchall()

   sql_laptops ='SELECT * FROM   products WHERE product_category="laptops" '

   cursor.execute(sql_laptops)
   laptops = cursor.fetchall()

   sql_electronics ='SELECT * FROM   products WHERE product_category="electronics" '

   cursor.execute(sql_electronics)
   electronics = cursor.fetchall()

   sql_bags ='SELECT * FROM   products WHERE product_category="bags" '

   cursor.execute(sql_bags)
   bags = cursor.fetchall()

   
   

   return render_template('home.html',  detergents= detergents ,laptops=  laptops, electronics= electronics, bags=bags )

@app.route('/upload',methods= ['GET', 'POST'])
def upload():
   '''
   Form display and upload route
   '''
   if request.method =='POST':
       product_name=request.form['product_name']
       product_desc=request.form['product_desc']
       product_cost=request.form['product_cost']
       product_image=request.files['product_image']
       product_category=request.form['product_category']   

       product_image.save('static/images/' + product_image.filename)   

       connection =pymysql.connect(host='localhost',user='root',password='',database='truham_db')

       cursor = connection.cursor()

       data = (product_name,product_desc,product_cost,product_image.filename,product_category)

       sql ='INSERT INTO products(product_name,product_desc,product_cost,product_image_name,product_category)  VALUES  (%s,%s,%s,%s,%s)'

       cursor.execute(sql,data)
       connection.commit()
       return render_template('upload.html',msg='Upload successful')
   else:
         
         return render_template  ('upload.html')
@app.route('/single_item/<product_id>' )
def single_item(product_id):  
         
        connection=pymysql.connect(host='localhost',user='root',password='',database='truham_db' )
        cursor=connection.cursor()
        sql = 'SELECT * FROM products WHERE product_id = %s'
        cursor.execute(sql,product_id)
        product = cursor.fetchone()

        return render_template('single_item.html', product=product)


@app.route('/register',methods=['GET','POST'])
def register():
   if request.method=='GET':
 
      return render_template('register.html')
   else:
       username=request.form['username']
       email=request.form['email']
       phone=request.form['phone']
       password=request.form['password']
       confirm_password=request.form['confirm_password']

       if  len(password) <8:
           return render_template('register.html' ,
           error="Password must be atleast 8 characters")
       elif password!=confirm_password:
           return render_template('register.html', error='Password do not match!!!')    
       else:
           connection=pymysql.connect(host='localhost', user='root',password='',database='truham_db')
           cursor=connection.cursor()
           sql='INSERT INTO users  (username,email,phone,password) VALUES (%s,%s,%s,%s)'
           cursor.execute(sql,(username,email,phone,password))
           connection.commit()
           send_sms(phone, 'Thank you for registering')
           return render_template('register.html',  success='Registration successful')
@app.route('/login',methods=['GET','POST'])      
def login():
    '''
    this is the login route
    '''
    if request.method=='GET':
        return render_template('login.html')
    else:
        username=request.form['username']
        password=request.form['password']
        connection=pymysql.connect(host='localhost',user='root',password='',database='truham_db')
        cursor=connection.cursor()
        sql='SELECT * FROM users WHERE username=%s AND password=%s'
        cursor.execute(sql,(username,password))
        if cursor.rowcount==0:
            return render_template('login.html',error='Invalid credentials')
        else:
            session['username']= username
            return redirect('/')
@app.route('/logout')   
def logout():
    """
    You've logged out
    """     
    session.clear()
    return redirect('/login')
@app.route('/mpesa', methods=['POST'])
def mpesa():
    phone=request.form['phone']
    amount=request.form['amount']
    stk_push(phone,amount)

    return '<h4>Complete your order payment and we will begin your transaction ASAP! You\'ll receive your order in minutes</h4> <a href=""> Go back to home page<a/>'

'''vendor route'''
@app.route('/vendor', methods = ['GET', 'POST'])
def vendor():
   
    if request.method == 'GET': 
      return render_template('vendor.html')
    else:
      firstname = request.form['firstname']
      lastname=request.form['lastname']
      county=request.form['county']
      password=request.form['password']
      confirm_password=request.form['confirm_password']
      email=request.form['email']

    if len(password) < 8:
         return render_template('vendor.html',error = 'Password must be atleast 8 characters long')
      
    elif password != confirm_password:
       return render_template('vendor.html', error= 'Passwords do not match')
      
    else:
      connection = pymysql.connect(host='localhost', user='root', password='', database='truham_db')

      cursor = connection.cursor()

      

      sql = 'INSERT INTO vendors(firstname,lastname,county,password,email) VALUES (%s, %s, %s, %s, %s)'

      cursor.execute(sql,(firstname,lastname,county,password,email))
      connection.commit()

      return render_template('vendor.html', msg= 'Entry successful')

 
app.secret_key= 'aab3047eb9ccfb3973f928d4ebdead9e60beb936b4d2838f7725c9cc165f0c8a'
app.run(debug=True)
