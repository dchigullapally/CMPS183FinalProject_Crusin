# -*- coding: utf-8 -*-
# try something like
from plugin_rating_widget import RatingWidget
from tables import *

db = DAL('sqlite:memory:')
db.define_table('rate',
    Field('rating', 'integer',
          requires=IS_IN_SET(range(1, 6)),  # "requires" is necessary for the rating widget
))

db.define_table('profile',
                Field('Name'),
                Field('Address'),
                Field('creator', db.auth_user, default=auth.user_id),
                Field('Own_a_Car'),
                Field('Driving_Experience'),
                Field('Profile_pic', 'upload'),
                Field('rating', 'double')
                )

################################ The core ######################################
# Inject the horizontal radio widget
db.profile.rating.widget = RatingWidget()
################################################################################

def index():
    profiles = db(db.profile).select()
    return dict(add_dict=profiles)

#to find the average for ratings
def review():
    
    forms = SQLFORM(db.review)
    if forms.process().accepted:
        #measure_ratings(form.vars.even)
        rating_val = form.vars.rating
        event_to_rate = form.vars.Name
        x = db.review.Name == event_to_rate
        n = len(x)
        for x in n:
            s = s + x.rating
        avg = s/n
        
        #session.flash = form.vars.rating
        #Successful processing.
        #session.flash = T('Registered Event')
        redirect(URL('default', 'index'))
        return dict(forms=forms)
