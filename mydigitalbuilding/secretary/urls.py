"""digitalsociety URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('watchman-home/',views.watchman_home, name="watchman-home"),
    path('register/',views.register, name="register"),
    path('login/',views.login, name="login"),
    path('',views.mainhome, name="mainhome"),
    path('image-gallery/',views.image_gallery,name="image-gallery"),
    path('image-gallery-chairman/',views.image_gallery_chairman, name="image-gallery-chairman"),
    path('image-gallery-watchman/',views.image_gallery_watchman, name="image-gallery-watchman"),
    path('reset-password/',views.reset_password, name="reset-password"),
    path('logout/',views.logout, name="logout"),
    path('myprofile/',views.myprofile, name="myprofile"),
    path('resetprofile/',views.resetprofile, name="resetprofile"),
    path('reset-profile-password/',views.reset_profile_password, name="reset-profile-password"),
    path('memberprofile/',views.memberprofile, name="memberprofile"),
    path('watchmanprofile/',views.watchmanprofile, name="watchmanprofile"),
    path('memberresetprofile/',views.memberresetprofile, name="memberresetprofile"),
    path('watchmanresetprofile/',views.watchmanresetprofile, name="watchmanresetprofile"),
    path('memberreset-profile-password/',views.memberreset_profile_password, name="memberreset-profile-password"),
    path('watchmanreset_profile_password/',views.watchmanreset_profile_password, name="watchmanreset_profile_password"),
    path('mem/',views.mem, name="mem"),
    path('allmembers/',views.allmembers, name="allmembers"),
    path('allmember/',views.allmember, name="allmember"),
    path('view-profile/<int:pk>',views.view_profile, name="view-profile"),
    path('c-view-memprofile/<int:pk>',views.c_view_memprofile, name="c-view-memprofile"),
    path('watchman_can_see_member_view_profile/<int:pk>',views.watchman_can_see_member_view_profile, name="watchman_can_see_member_view_profile"),
    path('watchman-request/',views.watchman_request, name="watchman-request"),
    path('watchman_status/<int:pk>/<slug:status>',views.watchman_status, name="watchman_status"),
    path('add-my-member/',views.add_my_member, name="add-my-member"),
    path('myfamilyprofile/',views.myfamilyprofile, name="myfamilyprofile"),
    path('Editmyfamilyprofile/<int:pk>',views.Editmyfamilyprofile, name="Editmyfamilyprofile"),
    path('chairman-add-my-member/',views.chairman_add_my_member, name="chairman-add-my-member"),
    path('chairmanmyfamilyprofile/',views.chairmanmyfamilyprofile, name="chairmanmyfamilyprofile"),
    path('chairmanEditmyfamilyprofile/<int:pk>',views.chairmanEditmyfamilyprofile, name="chairmanEditmyfamilyprofile"),
    path('watchman_all_members/',views.watchman_all_members, name="watchman_all_members"),
    path('notice/',views.notice, name="notice"),
    path('notice-view/',views.notice_view, name="notice-view"),
    path('chat/',views.chat, name="chat"),
    path('chat-view/',views.chat_view, name="chat-view"),
    path('delete-chat/<int:pk>',views.delete_chat, name="delete-chat"),
    path('all-delete-chat/<int:pk>',views.all_delete_chat, name="all-delete-chat"),
    path('memnotice-view/',views.memnotice_view, name="memnotice-view"),
    path('watchman-notice-view/',views.watchman_notice_view, name="watchman-notice-view"),
    path('delete-notice/<int:pk>',views.delete_notice, name="delete-notice"),
    path('delete-visitor/<int:pk>',views.delete_visitor, name="delete-visitor"),
    path('events/',views.events, name="events"),
    path('event-view/',views.event_view, name="event-view"),
    path('watchman-event-view/',views.watchman_event_view, name="watchman-event-view"),
    path('member-event-view/',views.memeber_event_view, name="memeber-event-view"),
    path('delete-event/<int:pk>',views.delete_event, name="delete-event"),
    path('add-complain/',views.add_complain, name="add-complain"),
    path('complain-details/',views.complain_details, name="complain-details"),
    path('delete-complain/<int:pk>',views.delete_complain, name="delete-complain"),
    path('members-request/',views.members_request, name="members-request"),
    path('members_status/<int:pk>/<slug:status>',views.members_status, name="members_status"),
    path('chairman-complain-details/',views.chairman_complain_details, name="chairman-complain-details"),
    path('watchman-complain-details/',views.watchman_complain_details, name="watchman-complain-details"),
    path('watchman-add-complain/',views.watchman_add_complain, name="watchman-add-complain"),
    path('watchman-delete-complain/<int:pk>',views.watchman_delete_complain, name="watchman-delete-complain"),
    path('members-suggestion-box/',views.members_suggestion_box, name="members-suggestion-box"),
    path('view-members-suggestion-box/',views.view_members_suggestion_box, name="view-members-suggestion-box"),
    path('delete-members-suggestion/<int:pk>',views.delete_members_suggestion, name="delete-members-suggestion"),
    path('watchman-suggestion-box/',views.watchman_suggestion_box, name="watchman-suggestion-box"),
    path('view-watchman-suggestion-box/',views.view_watchman_suggestion_box, name="view-watchman-suggestion-box"),
    path('delete-watchman-suggestion/<int:pk>',views.delete_watchman_suggestion, name="delete-watchman-suggestion"),
    path('view-chairman-suggestion-box/',views.view_chairman_suggestion_box, name="view-chairman-suggestion-box"),
    path('delete-chairman-suggestion/<int:pk>',views.delete_chairman_suggestion, name="delete-chairman-suggestion"),
    path('add-vistiors/',views.add_vistiors, name="add-vistiors"),    
    path('allvisitors/',views.allvisitors , name="allvisitors"),  
    path('vistiordetails/<int:d_pk>',views.vistiordetails,name="vistiordetails"), 
    # path('my-vistiordetails/<int:pk>',views.my_vistiordetails,name="my-vistiordetails"), 
    # path('add-photo/',views.add_photo,name="add-photo"),  
    path('house-on-rent/',views.house_on_rent,name="house-on-rent"),
    path('house-on-rent-view/',views.house_on_rent_view, name="house-on-rent-view"),
    path('delete-member-house-on-rent/<int:pk>',views.delete_member_house_on_rent, name="delete-member-house-on-rent"),
    path('chairman-house-on-rent/',views.chairman_house_on_rent,name="chairman-house-on-rent"),
    path('chairman-house-on-rent-view/',views.chairman_house_on_rent_view, name="chairman-house-on-rent-view"),
    path('delete-chairman-house-on-rent/<int:pk>',views.delete_chairman_house_on_rent, name="delete-chairman-house-on-rent"),
    path('paytmhome/',views.paytmhome, name="paytmhome"),
    path('initiate_payment/',views.initiate_payment, name="initiate_payment"),
    path('callback/',views.callback, name="callback"),
    path('forgot-password',views.forgot_password, name="forgot-password"),
    path('reset-password-view/',views.reset_password_view, name="reset-password-view"),
    path('payment_view/',views.payment_view, name="payment_view"),
    path('contacts/',views.contacts, name="contacts"),
    path('approve-members/<int:pk>', views.approve_members, name="approve-members"),
    
]