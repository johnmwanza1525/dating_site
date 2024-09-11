<<<<<<< HEAD
from django.urls import path, re_path, include
from chat.views import (chat, new_message_check,
                        wink, chat_ajax, chat_home,
                        read_messages, winks,
                        read_wink, read_view,
                        views, reject,
                        block_user,unblock_user,
                        delete_conversation
                        )

urlpatterns = [
    path('<int:id>/', chat, name="chat"),
    path('home/', chat_home, name="chat_home"),
    path('ajax/winks/', wink, name="wink"),
    path('ajax/reject/', reject, name="reject"),
    path('block_user/<int:user_id>/', block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', unblock_user, name='unblock_user'),
    path('ajax/new_message_check/', new_message_check, name='new_message_check'),
    path('ajax/read/', read_messages, name="read_messages"),
    path('ajax/new_message/', chat_ajax, name="new_message"),
    path('winks/', winks, name="winks"),
    path('views/', views, name="views"),
    path('ajax/read-view/', read_view, name='read_view'),
    path('ajax/read-wink/', read_wink, name='read_wink'),
    path('delete_conversation/<int:conversation_id>/', delete_conversation, name='delete_conversation'),
]

# For the commented section, you can update it similarly:

# from profiles.views import index, logout, login, register, user_profile, create_profile, validate_username
# from profiles import url_reset

# urlpatterns += [
#     path('cart/', view_cart, name="view_cart"),
#     path('cart/add/<int:id>/', add_to_cart, name="add_to_cart"),
#     path('cart/adjust/<int:id>/', adjust_cart, name="adjust_cart"),
# ]
=======
from django.conf.urls import url, include
from chat.views import chat, create, new_message_check, wink, chat_ajax, chat_home, read_messages, winks, read_wink, read_view, views

urlpatterns = [
    url(r'^(?P<id>\d+)', chat, name="chat"),
    url(r'^home/', chat_home, name="chat_home"),
    url(r'^ajax/winks/$', wink, name="wink"),
    url(r'^ajax/new_message_check/$', new_message_check, name='new_message_check'),
    url(r'^ajax/read/$', read_messages, name="read_messages"),
    url(r'^ajax/new_message/$', chat_ajax, name="new_message"),
    url(r'^winks/$', winks, name="winks"),
    url(r'^views/$', views, name="views"),
    url(r'^ajax/read-view/', read_view),
    url(r'^ajax/read-wink/', read_wink),
    url(r'^$', create, name="create"),
]


# from django.conf.urls import url, include
# from profiles.views import index, logout, login, register, user_profile, create_profile, validate_username
# from profiles import url_reset


# urlpatterns = [
#     url(r'^$', view_cart, name="view_cart"),
#     url(r'^add/(?P<id>\d+)', add_to_cart, name="add_to_cart"),
#     url(r'^adjust/(?P<id>\d+)', adjust_cart, name="adjust_cart")
#     ]
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
