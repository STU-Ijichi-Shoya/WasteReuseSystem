from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login.utils import expand_login_view
from flask_migrate import current
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.utils import send_file
from werkzeug.wrappers.response import Response
from .models import Item, ItemLike, ItemPhoto, User,ItemBlob
from . import db
from .form import ItemAdd
import io
items_app = Blueprint('items', __name__)

@items_app.route('/items/blob/<int:blob_id>')
def sendPhotoID(blob_id):
    blob=db.Query(ItemBlob).filter_by(id=blob_id)
    if blob is not None:
        return send_file(
            io.BytesIO(blob.blob),
            mimetype='image/jpeg',
            as_attachment=False,
        )
    return Response(status=400)

@items_app.route("/items/search")
def searchItems():
    tag=request.args.get('tag')
    keyword=request.args.get('keyword')
    # validation
    if tag is not None:
        tag=tag.replace(' ','')
    if keyword is not None:
        # 全角を半角にして、分割
        keyword=keyword.replace('　',' ').split(' ').replace(' ','')
    # find by tag
    if len(tag)>0:
        pass
    # find by keyword
    elif len(keyword)>0:
        search_items=db.session.query(Item.id,Item.item_name,ItemPhoto.URI,ItemLike.is_like,Item.place,Item.user_id,Item.handing_method)\
                                    .join(ItemPhoto,ItemPhoto.item_id==Item.id)\
                                    .join(ItemLike,Item.id==ItemLike.item_id)\
                                    .join(User,Item.user_id==User.id)\
                                    .filter_by(is_like=True,univercity_id==current_user.univercity_id).all()
        #TODO:tag
    
    render_template()



@items_app.route("/items")
def showItems():
    #     User.idと、UserSocial.user_idで内部結合し、
    # ユーザ全てをList型で取得する。
    # user_nameはこの形式で取得される。
    # 返り値：[(User, UserSocial)]
    # user_name = session.query(User, UserSocial).\
    # join(UserSocial, User.id==UserSocial.user_id).\
    # all()
    if current_user.is_authenticated:
        # いいねしたアイテム
        like_items=db.session.query(Item.id,Item.item_name,ItemPhoto.URI,ItemLike.is_like)\
                                    .join(ItemPhoto,ItemPhoto.item_id==Item.id)\
                                    .join(ItemLike,Item.id==ItemLike.item_id)\
                                    .join(User,Item.user_id==User.id)\
                                    .filter_by(is_like=True,univercity_id==current_user.univercity_id).limit(10).all()
        
        recommend_items=db.session.query(Item.id,Item.item_name,ItemPhoto.URI,ItemLike.is_like)\
                                    .join(ItemPhoto,ItemPhoto.item_id==Item.id)\
                                    .join(ItemLike,Item.id==ItemLike.item_id)\
                                    .join(User,Item.user_id==User.id)\
                                    .filter_by(univercity_id==current_user.univercity_id).limit(10).all()
        
        #検索履歴
        #TODO
        search_his_items=[]
        # new Item
        new_items=db.session.query(Item.id,Item.item_name,ItemPhoto.URI,ItemLike.is_like)\
                                    .join(ItemPhoto,ItemPhoto.item_id==Item.id)\
                                    .join(ItemLike,Item.id==ItemLike.item_id)\
                                    .join(User,Item.user_id==User.id)\
                                    .filter_by(univercity_id==current_user.univercity_id).limit(10).order_by(Item.created_at.amount.desc()).all()
    else:
        recommend_items=db.session.query(Item.id,Item.item_name,ItemPhoto.URI,ItemLike.is_like)\
                                    .join(ItemPhoto,ItemPhoto.item_id==Item.id)\
                                    .join(ItemLike,Item.id==ItemLike.item_id)\
                                    .join(User,Item.user_id==User.id)\
                                    .limit(100).all()
        


