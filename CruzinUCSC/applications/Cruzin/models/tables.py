#########################################################################
## Define your tables below; for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
from datetime import datetime

from plugin_rating_widget import RatingWidget
db.define_table('rate',
    Field('rating', 'integer',
          requires=IS_IN_SET(range(1,6)), # "requires" is necessary for the rating widget
))

def get_first_name():
    name = 'Unidentified user'
    if auth.user:
        name = auth.user.first_name
    return name

def get_first_email():
    email = 'None'
    if auth.user:
        email = auth.user.email
    return email

def get_user_info():
    value = 'None'
    if auth.user:
        value = auth.user.id
    return value

CAR = ['Yes', 'No']

db.define_table('profile',
                Field('Name'),
                Field('Address'),
                Field('creator', db.auth_user, default=auth.user_id),
                Field('Own_a_Car'),
                Field('Driving_Experience'),
                Field('Profile_pic', 'upload'),
                Field('rating', 'double')
                )
db.profile.creator.readable = db.profile.creator.writable = False
db.profile.Profile_pic.requires = IS_EMPTY_OR(IS_IMAGE(error_message="Oops! That's not an image file."))
db.profile.rating.readable = db.profile.rating.writable = False
db.profile.Driving_Experience.requires = IS_INT_IN_RANGE(0, 50, error_message='The years of experience should be in the range 0...50')
db.profile.Own_a_Car.requires = IS_IN_SET(CAR)
db.profile.Own_a_Car.default = 'Yes'
db.profile.Own_a_Car.required = True

db.define_table('email',
                Field('sender', db.auth_user),
                Field('receiver', db.auth_user),
                Field('text_message','text'),
                Field('sending_time','datetime',default = datetime.utcnow())
                )

db.email.receiver.requires = IS_EMPTY_OR(IS_IN_DB(db(db.auth_user), 'auth_user.id', '%(first_name)s'))
db.email.sending_time.writable = False
db.email.sender.writable = False
db.email.sender.default = get_user_info()
db.email.id.readable = False

db.define_table('review',
                Field('sender', db.auth_user),
                Field('Address'),
                Field('text_message','text'),
                Field('sending_time','datetime',default = datetime.utcnow()),
                Field('rating', 'integer', requires=IS_IN_SET(range(1,6)))
                )
db.review.rating.widget = RatingWidget()
db.review.sending_time.writable = False
db.review.sender.writable = False
db.review.sender.default = get_user_info()
db.review.id.readable = False

db.define_table('board',
             Field('board_author', db.auth_user, default=auth.user_id),
             Field('board_title'),
             Field('board_id'),
             Field('created_on', 'datetime', default=datetime.utcnow()),
            )

db.define_table('post',
             Field('post_author', db.auth_user, default=auth.user_id),
             Field('post_parent'),
             Field('post_title'),
             Field('post_content', 'text'),
             Field('created_on', 'datetime', default=datetime.utcnow()),
             Field('post_id')
            )
