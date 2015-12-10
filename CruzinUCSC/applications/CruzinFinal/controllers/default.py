# -*- coding: utf-8 # -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

from gluon import utils as gluon_utils
import time
from gluon.serializers import json
from gluon.tools import geocode

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    profiles = db(db.auth_user).select()
    #blank_list = request.vars['blank_profiles[]']
    #if blank_list is None:
    #    blank_list = []
    #elif type(blank_list) is str:
    #    blank_list = [blank_list]
    #rows = db(~db.profile.profile_id.belongs(blank_list)).select(db.profile.ALL, orderby=~db.profile.created_on)
    d =[]
    for r in profiles:
        location = geocode(r.Address)
        d = d + [{'profile_Fname': r.first_name,'profile_Lname': r.last_name, 'profile_address': r.Address, 'profile_car': r.Own_a_Car, 'profile_driving_experience':r.Driving_Experience, 'profile_pic':r.Profile_pic, 'lat': location[0], 'lng': location[1]}]
    return dict(profile_dict=json(d),add_dict=profiles)



#CREATE A PROFILE
def newprofile():
    form = SQLFORM(db.profile)
    if form.process().accepted:
       session.flash = T('The profile was created')
       redirect(URL('newprofile'))
    return dict(form=form)

#VIEW PROFILE
def view():
    """View profile."""
    response.flash = T("User Profile")
    form = ''
    something = db(db.auth_user.id == auth.user_id).select().first()
    url = URL('download')
    form = SQLFORM(db.auth_user, record = something, readonly=True, upload=url)
    return dict(something=something, form=form)

#EDIT PROFILE
def editprofile():
    return dict(form=auth.profile())

@auth.requires_login()
@auth.requires_signature()
def edit():
    p = db.auth_user(request.args(0)) or redirect(URL('default', 'index'))
    if p.user_id != auth.user_id:
        session.flash = T('Not authorized.')
        redirect(URL('default', 'index'))
    profile = SQLFORM(db.auth_user, record=p)
    if profile.process().accepted:
        session.flash = T('Updated')
        redirect(URL('default', 'index'))
    return dict(profile=profile)

#ABOUT US PAGE
def about():
    return dict()

#WORKING ON LEAVING A REVIEW FOR DRIVERS
def review():
    forms = SQLFORM(db.review, showid=False)
    if forms.process().accepted:
        redirect(URL('default', 'index'))
    return dict(forms=forms)

#EMAIL FORM
def chat():
    form = SQLFORM(db.email)
    if form.process().accepted:
        session.flash = T('Message Sent')
        redirect(URL('default', 'home'))
    return dict(form=form)

def modify():
    #return dict(form=auth.profile(edit= False))
    form = db.profile
    return dict(form=form)

#EMAIL HOME
def home():
    q = db.email.receiver == auth.user_id
    form = SQLFORM.grid(q, orderby=~db.email.sending_time, csv = False, deletable=True,
    editable=False,
    details=True,
    selectable=None,
    create=False,
    searchable=False,
    paginate=20)
    return locals()

@auth.requires_login()
def blah():
    return dict()

@auth.requires_login()
def board():
    board_id = request.args(0)
    return dict(board_id=board_id)


@auth.requires_signature()
def add_board():
    if not json.loads(request.vars.board_new):
        author = db().select(db.board.board_author).first().board_author
        if author != auth.user.id:
            return "ko"
    db.board.update_or_insert((db.board.board_id == request.vars.board_id),
            board_id=request.vars.board_id,
            board_title=request.vars.board_title)
    return "ok"


def checkAuth(board_author):
    """Check if logged user is the author."""
    if board_author==auth.user.id:
        return True
    return False


@auth.requires_signature()
def load_boards():
    """Loads all boards."""
    blank_list = request.vars['blank_boards[]']
    if blank_list is None:
        blank_list = []
    elif type(blank_list) is str:
        blank_list = [blank_list]
    rows = db(~db.board.board_id.belongs(blank_list)).select(db.board.ALL, orderby=~db.board.created_on)
    d = [{'board_id':r.board_id,'board_title': r.board_title,'board_is_author': checkAuth(r.board_author)}
         for r in rows]
    return response.json(dict(board_dict=d))

@auth.requires_signature()
def load_posts():
    """Loads all messages for the board."""
    blank_list = request.vars['blank_posts[]']
    if blank_list is None:
        blank_list = []
    elif type(blank_list) is str:
        blank_list = [blank_list]
    board_id = request.vars.board_id
    board = db(db.board.board_id==board_id).select()
    if board is None:
        session.flash = T("No such board")
    rows = db((~db.post.post_id.belongs(blank_list)) & (db.post.post_parent==board_id)).select(db.post.ALL, orderby=~db.post.created_on)
    d = [{'post_id':r.post_id,'post_title': r.post_title,'post_content': r.post_content,'post_is_author': checkAuth(r.post_author)}
         for r in rows]
    return response.json(dict(post_dict=d))


@auth.requires_signature()
def add_post():
    if not json.loads(request.vars.post_new):
        author = db().select(db.post.post_author).first().post_author
        if author != auth.user.id:
            return "ko"
    db.post.update_or_insert((db.post.post_id == request.vars.post_id),
                             post_id=request.vars.post_id,
                             post_title=request.vars.post_title,
                             post_content=request.vars.post_content,
                             post_parent=request.vars.post_parent)
    return "ok"


@auth.requires_signature()
def delete_post():
    delete_list = request.vars['delete_dict[]']
    if delete_list is None:
        delete_list = []
    elif type(delete_list) is str:
        delete_list = [delete_list]
    db(db.post.post_id.belongs(delete_list)).delete()

    return 'ok'

def load_profile_info():
    blank_list = request.vars['blank_profiles[]']
    if blank_list is None:
        blank_list = []
    elif type(blank_list) is str:
        blank_list = [blank_list]
    rows = db(~db.profile.profile_id.belongs(blank_list)).select(db.profile.ALL, orderby=~db.profile.created_on)
    d = [{'profile_id':r.profile_id,'profile_name': r.Name,'profile_address': r.Address, 'profile_creator': r.creator, 'profile_car': r.Own_a_Car, 'profile_driving_experience':r.Driving_Experience, 'profile_pic':r.Profile_pic, 'profile_rating': r.rating}
         for r in rows]
    return dict(profile_dict=d)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
