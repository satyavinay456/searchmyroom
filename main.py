from flask import Flask,render_template,url_for,request,redirect,jsonify,flash,session
from flask_uploads import UploadSet,configure_uploads,IMAGES
from pymongo import MongoClient
import datetime
from datetime import timedelta
import bcrypt
import traceback
import os
import random,string

app = Flask(__name__)
#secret key for application
app.secret_key="agbakghaoihhoba"
#logout after 10 minutes of inactivity
app.permanent_session_lifetime = timedelta(minutes=10)
photos=UploadSet('photos',IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] =os.path.join(os.path.dirname(os.path.realpath(__file__)), "static","uploads")
#app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'
configure_uploads(app,photos)

#generates random string
def random_string(length):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase+string.digits) for _ in range(length))

try:
    client=MongoClient('mongodb+srv://vinay_456:samsung.1@vinay-c6krv.mongodb.net/test?retryWrites=true')
    db=client['Search_My_Room_Git']
    properties_col=db['properties']
    landlord_registrations=db['landlord_registrations']
    tenant_registrations=db['tenant_registraions']
    sc_col=db['cities']
    states=list(sc_col.find().sort([('state',1)]).distinct('state'))
    states=['select state']+states
    states_info=''
    for i in states:
        states_info+="<option>"+i+"</option>"
except:
    traceback.print_exc()

#login page if session found => redirect to landord or tenant
@app.route('/')
def login():
    if session.get('landlord_name_ses',''):
        return redirect(url_for('landlord'))
    if session.get('tenant_name_ses',''):
        return redirect(url_for('tenant'))
    return render_template('Login.html')

#register page for both users
@app.route('/register')
def register():
   return render_template('Register.html')

#registration process for both landlord and tenant
@app.route('/registration',methods=['GET','POST'])
def registration():
    if request.method=='POST':
        client_name=request.form['name']
        client_email=request.form['email']
        client_password=request.form['password']
        try:
            radio=request.form['optradio']
        except:
            radio=None
            flash("please select your type of user","error")
            return redirect(url_for('register'))
        if radio=='Landlord':
            if list(landlord_registrations.find({'client_email': client_email})):
                flash("Your Email is already registered as a Landlord...Please login","error")
            else:
                client_hashed_password=bcrypt.hashpw(client_password.encode(encoding='UTF-8',errors='strict'), bcrypt.gensalt())
                #inserting record
                landlord_registrations.insert_one({"client_name":client_name,'client_email':client_email,'client_password':client_hashed_password,'date':datetime.datetime.now(),'verification':1})
                flash("Registered as Landlord...Please Login","success")
        else:
            if list(tenant_registrations.find({'client_email': client_email})):
                flash("Your Email is already registered as a Tenant","error")
            else:
                client_hashed_password=bcrypt.hashpw(client_password.encode(encoding='UTF-8',errors='strict'), bcrypt.gensalt())
                #inserting record
                #if need authentication : set verification to 0
                tenant_registrations.insert_one({"client_name":client_name,'client_email':client_email,'client_password':client_hashed_password,'date':datetime.datetime.now(),'bookmarks':[],'verification':1})
                flash("Registered as Tenant...Please Login","success")
        return redirect(url_for('register'))
    return redirect(url_for('register'))

#checks with whether credintials entered are correct or wrong
@app.route('/logging_in',methods=['GET','POST'])
def logging_in():
    if request.method=='POST':
        client_entered_email=request.form['email']
        client_entered_password=request.form['password']
        try:
            radio=request.form['optradio']
        except:
            radio=None
            flash("please select your type of user","error")
            return redirect(url_for('login'))
        if radio=='Landlord':
            landlord_reg_cur=landlord_registrations.find_one({'client_email':client_entered_email})
            #checking if any record present in db in the name of client_entered_email
            if landlord_reg_cur:
                if landlord_reg_cur['verification']==1:
                    #checking client_entered_password with db password
                    if bcrypt.checkpw(client_entered_password.encode('utf-8'), landlord_reg_cur['client_password']):
                        session.permanent = True
                        session['landlord_name_ses']=landlord_reg_cur['client_name']
                        session['landlord_email_ses']= landlord_reg_cur['client_email']
                        return redirect(url_for('landlord'))
                    else:
                        flash("wrong password","error")
                else:
                    flash("Entered email is not Verified","error")
            else:
                flash("Entered email is not registered as Landlord","error")
        else:
            tenant_reg_cur=tenant_registrations.find_one({'client_email':client_entered_email})
            #checking if any record present in db in t  he name of client_entered_email
            if tenant_reg_cur:
                if tenant_reg_cur['verification']==1:
                    session.permanent = True
                    #checking client_entered_password with db password
                    if bcrypt.checkpw(client_entered_password.encode('utf-8'), tenant_reg_cur['client_password']):
                        session['tenant_name_ses']=tenant_reg_cur['client_name']
                        session['tenant_email_ses']= tenant_reg_cur['client_email']
                        return redirect(url_for('tenant'))
                    else:
                        flash("wrong password","error")
                else:
                    flash("Entered email is not Verified","error")
            else:
                flash("Entered email is not registered as Tenant","error")
        return redirect(url_for('login'))
    return redirect(url_for('login'))

#landlor home page
@app.route('/landlord')
def landlord():
    if session.get('landlord_name_ses',''):
        landlord_name=session['landlord_name_ses']
        landlord_email=session['landlord_email_ses']
    else:
        return redirect(url_for('login'))
    return render_template('Landlord.html',landlord_name=landlord_name,landlord_email=landlord_email,states_info=states_info)

#tenant home page
@app.route('/tenant')
def tenant():
    if session.get('tenant_name_ses',''):
        tenant_name=session['tenant_name_ses']
        tenant_email=session['tenant_email_ses']
    else:
        return redirect(url_for('login'))
    #retrieving basic data from DB for home page
    show_all_data=0
    total_properties=0
    try:
        total_properties=list(properties_col.find({},{'_id':0}))
        Apartments=properties_col.find({'property_category': 'Apartments'}).count()
        Resort=properties_col.find({'property_category': 'Resort'}).count()
        Villas=properties_col.find({'property_category': 'Villas'}).count()
        Cottage=properties_col.find({'property_category': 'Cottage'}).count()
        Cabins=properties_col.find({'property_category': 'Cabins'}).count()
        show_all_data=len(total_properties)
        bookmarks_list=tenant_registrations.find({'client_email': session.get('tenant_email_ses','')}).distinct('bookmarks')
        for i in total_properties:
            if i['unique_id'] in bookmarks_list:
                i['bookmarked']='yes'
        available_states=list(properties_col.find().distinct('landlord_state'))
    except:
        show_all_data=[]
        available_states=[]
        total_properties=[]
        Cabins,Cottage,Villas,Resort,Apartments=[0,0,0,0,0]
        traceback.print_exc()
    return render_template('Tenant.html', show_all=show_all_data,total_properties=total_properties,Cabins=Cabins,Cottage=Cottage,Villas=Villas,Resort=Resort,Apartments=Apartments,states_info=available_states,tenant_name=tenant_name)

#shows bookmarks for tenants
@app.route('/bookmarks_properties')
def bookmarks_properties():
    if session.get('tenant_name_ses',''):
        bid_list=tenant_registrations.find({'client_email': session.get('tenant_email_ses','') }).distinct('bookmarks')
        bookmarks_properties=list(properties_col.find({ 'unique_id' : { '$in' : bid_list } }))
        for i in bookmarks_properties:
            i['bookmarked']='yes'
        print(bookmarks_properties)
    else:
        return redirect(url_for('login'))
    return render_template('tenant_bookmarks.html',bookmarks_properties=bookmarks_properties)


#adding property functionality for landlords is done here
@app.route('/add_property',methods=['POST','GET'])
def add_property():
    if request.method=='POST' and 'photo' in request.files:
        extension='.jpg' if request.files['photo'].content_type=='image/jpeg' else '.png'
        rand_str=random_string(8)
        filename = photos.save(request.files['photo'],name=rand_str+extension)

        landlord_name=request.form.get('landlord_name')
        landlord_email=request.form.get('landlord_email')
        property_name=request.form.get('property_name')
        property_category=request.form.get('property_category')

        landlord_city=request.form.get('landlord_city')
        landlord_state=request.form.get('landlord_state')
        property_total_rooms=request.form.get('property_total_rooms')
        property_available_rooms=request.form.get('property_available_rooms')
        property_average_rent=request.form.get('property_average_rent')
        Daily_breakfast=request.form.get('Daily_breakfast')
        property_amenities=request.form.get('property_amenities')
        #as we validated in jQuery there is no need to check '<' case
        if property_total_rooms>property_available_rooms:
            rooms_flag=1
        else :
            rooms_flag=0
        try:
            properties_col.insert_one({'filename':"uploads/"+filename,'unique_id':rand_str,'landlord_name':landlord_name, 'landlord_email': landlord_email ,'property_category':property_category , 'property_name':property_name ,'landlord_city':landlord_city , 'landlord_state' : landlord_state , 'property_total_rooms':int(property_total_rooms) , 'property_available_rooms':int(property_available_rooms), 'property_average_rent': int(property_average_rent),'Daily_breakfast':Daily_breakfast, 'property_amenities':property_amenities.split(","),'rooms_flag':rooms_flag ,'bookmarked':'no','created_at': datetime.datetime.now()})
            insert_status=1
        except:
            traceback.print_exc()
            insert_status=0
        return jsonify({'insert_status':insert_status, "bcg_image":url_for('static',filename='img/house-logo.jpg')})
    else:
        return "NOPHOTO"
    return render_template('404.html')

#showing properties of landlords
@app.route('/landlord_properties')
def landlord_properties():
    if session.get('landlord_name_ses',''):
        landlord_name=session['landlord_name_ses']
        landlord_email=session['landlord_email_ses']
        try:
            landlord_properties=list(properties_col.find({'landlord_name':landlord_name, 'landlord_email': landlord_email},{'property_name':1,'property_category':1,'property_average_rent':1,'filename':1,'_id':0}))
        except:
            traceback.print_exc()
            return redirect(url_for('landlord'))
    else:
        return redirect(url_for('login'))
    return render_template('landlord_properties.html',landlord_properties=landlord_properties)

#category selection in tenant home page
@app.route('/category_clicks',methods=["GET","POST"])
def category_clicks():
    if request.method=='POST':
        category_name=request.form.get('name')
        if category_name=='High-Low':
                category_properties=list(properties_col.find({},{'id':0,'created_at':0}).sort([('property_average_rent',-1)]))
        elif category_name=='Low-High':
                category_properties=list(properties_col.find({},{'id':0,'created_at':0}).sort([('property_average_rent',1)]))
        elif category_name in ('Apartments','Cottage','Resort','Cabins','Villas') :
            category_properties=list(properties_col.find({'property_category':category_name},{'id':0,'created_at':0}))
        else :
            category_properties=list(properties_col.find({},{'id':0,'created_at':0}))
        cards_html=''
        bookmarks_list=tenant_registrations.find({'client_email': session.get('tenant_email_ses','')}).distinct('bookmarks')
        for i in category_properties :
            if i['unique_id'] in bookmarks_list:
                i['bookmarked']='yes'
            if i['bookmarked']=='yes':
                cards_html+=' <div class="card" style="width: 18rem;height:20%;" id="main_card" > <img style="height:20%;" class="card-img-top card_size" src="/static/'+i['filename']+'" alt="Card image">   <div class="card-body">  <h4 class="card-title">'+i['property_name']+'</h4>  <small class="card-text">Category: <span> '+i['property_category']+'</span> </small><p class="card-text">Average Rent <span>'+str(i['property_average_rent'])+'</span> </p>  <img id="'+i['unique_id']+'bookmarked" style="position:relative;top:20px;left:97%;" class="'+i['unique_id']+'bookmarked" src="static/img/bookmarked.svg")}}" alt=""><img id='+i['unique_id']+'bookmark" style="position:relative;top:20px;left:97%;display:none;" class="'+i['unique_id']+'bookmark" src="static/img/bookmark.svg")}}" alt=""></div></div>'
            else:
                cards_html+=' <div class="card" style="width: 18rem;height:20%;" id="main_card" > <img style="height:20%;" class="card-img-top card_size" src="/static/'+i['filename']+'" alt="Card image">   <div class="card-body">  <h4 class="card-title">'+i['property_name']+'</h4>  <small class="card-text">Category: <span> '+i['property_category']+'</span> </small><p class="card-text">Average Rent <span>'+str(i['property_average_rent'])+'</span> </p>  <img id="'+i['unique_id']+'bookmarked" style="position:relative;top:20px;left:97%;display:none" class="'+i['unique_id']+'bookmarked" src="static/img/bookmarked.svg")}}" alt=""><img id='+i['unique_id']+'bookmark" style="position:relative;top:20px;left:97%;" class="'+i['unique_id']+'bookmark" src="static/img/bookmark.svg")}}" alt=""></div></div>'
        return jsonify({"cards_html":cards_html})

#get the cities list for landlord home page
@app.route('/getcities',methods=['POST','GET'])
def getcities():
    if request.method=='POST':
        selected_state=request.form.get('selected_state')
        cities=list(sc_col.find({'state':selected_state}).sort([('city',1)]).distinct('city'))
        cities_info=''
        for i in cities:
            cities_info+="<option>"+i+"</option>"
        return jsonify({'states':states_info,'cities':cities_info})
    return render_template('404.html')

#if tenant try to bookmark the properties
@app.route('/bookmarks_process',methods=['POST','GET'])
def bookmarks_process():
    if request.method=="POST":
        imageurl=request.form.get('imageurl')
        bookmark_client=session.get('tenant_email_ses')
        if imageurl.endswith('marked'):
            imageurl=imageurl[:imageurl.find('book')]
            try:
                tenant_registrations.update({'client_email':bookmark_client},{ '$pull': { 'bookmarks': imageurl } })
                return "bn_success"
            except:
                traceback.print_exc()
                return "bn_fail"
        else:
            imageurl=imageurl[:imageurl.find('book')]
            try:
                tenant_registrations.update({'client_email':bookmark_client},{ '$push': { 'bookmarks': imageurl } })
                return "by_success"
            except:
                traceback.print_exc()
                return "by_fail"

    return redirect(url_for('tenant'))

#filter functionality for tenants is donen here
@app.route('/filter_all',methods=['POST','GET'])
def filter_all():
    if request.method=='POST':
        location=request.form.get('location')
        rooms_available=request.form.get('rooms_available')
        amenities_list=request.form.getlist('amenities_list[]')
        breakfast_condition=request.form.get('breakfast_condition')
        #filter_list=final_filter(location,rooms_available,amenities_list,breakfast_condition)
        filter_list=list(properties_col.find({'landlord_state':location,'rooms_flag':int(rooms_available),'property_amenities':{'$all':amenities_list},'Daily_breakfast':breakfast_condition}))
        filter_cards=''
        bookmarks_list=tenant_registrations.find({'client_email': session.get('tenant_email_ses','')}).distinct('bookmarks')
        for i in filter_list:
            if i['unique_id'] in bookmarks_list:
                i['bookmarked']='yes'
            if i['bookmarked']=='yes':
                filter_cards+=' <div class="card" style="width: 18rem;height:20%;" id="main_card" > <img style="height:20%;" class="card-img-top card_size" src="/static/'+i['filename']+'" alt="Card image">   <div class="card-body">  <h4 class="card-title">'+i['property_name']+'</h4>  <small class="card-text">Category: <span> '+i['property_category']+'</span> </small><p class="card-text">Average Rent <span>'+str(i['property_average_rent'])+'</span> </p>  <img id="'+i['unique_id']+'bookmarked" style="position:relative;top:20px;left:97%;" class="'+i['unique_id']+'bookmarked" src="static/img/bookmarked.svg")}}" alt=""><img id='+i['unique_id']+'bookmark" style="position:relative;top:20px;left:97%;display:none;" class="'+i['unique_id']+'bookmark" src="static/img/bookmark.svg")}}" alt=""></div></div>'
            else:
                filter_cards+=' <div class="card" style="width: 18rem;height:20%;" id="main_card" > <img style="height:20%;" class="card-img-top card_size" src="/static/'+i['filename']+'" alt="Card image">   <div class="card-body">  <h4 class="card-title">'+i['property_name']+'</h4>  <small class="card-text">Category: <span> '+i['property_category']+'</span> </small><p class="card-text">Average Rent <span>'+str(i['property_average_rent'])+'</span> </p>  <img id="'+i['unique_id']+'bookmarked" style="position:relative;top:20px;left:97%;display:none" class="'+i['unique_id']+'bookmarked" src="static/img/bookmarked.svg")}}" alt=""><img id='+i['unique_id']+'bookmark" style="position:relative;top:20px;left:97%;" class="'+i['unique_id']+'bookmark" src="static/img/bookmark.svg")}}" alt=""></div></div>'

        return filter_cards
    return redirect(url_for('tenant'))

@app.route('/property/<id>')
def show_properties(id):
    if session.get('tenant_name_ses',''):
        property_dict=list(properties_col.find({'unique_id':id},{'_id':0,'bookmarked':0,'created_at':0}))[0]
        return render_template('tenants_properties.html',property_dict=property_dict)
    else:
        return render_template('404.html')
@app.route('/prop')
def tenant_properties():
    return render_template('tenants_properties.html')
#if tenant tries to logout
@app.route('/tenant_logout')
def tenant_logout():
    session.pop('tenant_name_ses','')
    session.pop('tenant_email_ses','')
    return redirect(url_for('login'))

#if landlord tries to logout
@app.route('/landlord_logout')
def landlord_logout():
    session.pop('landlord_name_ses','')
    session.pop('landlord_email_ses','')
    return redirect(url_for('login'))

if __name__ == '__main__':
   app.run()
