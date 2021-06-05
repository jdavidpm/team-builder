from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('teams/', views.teams, name='teams-list'),
    path('teams/chats/<int:chat_id>/service', views.teams_chat_service, name='teams-chat-service'),
    path('teams/chats/', views.teams_chat_list, name='teams-chat-list'),
    path('teams/chats/new/', views.teams_chat_add, name='teams-chat-add'),
    path('teams/chats/<int:chat_id>/', views.teams_chat_conversation, name='teams-chat-conversation'),
    path('teams/messages/inbox/', views.teams_chat_inbox, name='teams-chat-inbox'),
    path('teams/messages/new/', views.teams_chat_new, name='teams-chat-new'),
    path('teams/messages/new/<int:team_id>/', views.teams_chat_new, name='teams-chat-new'),
    path('teams/messages/<int:message_id>/', views.teams_chat_item, name='teams-chat-item'),
    path('teams/create/', views.team_create, name='teams-create'),
    path('teams/creation/', views.teams_creation, name='teams-creation'),
    path('teams/invitations/', views.teams_join_request, name='teams-join-request'),
    path('teams/invitation/new', views.teams_join_invitation, name='teams-join-invitation'),
    path('teams/invitation/done/', views.teams_join_invitation_done, name='teams-join-invitation-done'),
    path('teams/<int:id>/evaluate/', views.team_evaluate, name='teams-evaluate'),
    path('teams/<int:id>/', views.teams_item, name='teams-item'),
    path('teams/<int:id>/update/', views.team_update, name='team-update'),
    path('teams/<int:id>/update/members/', views.team_update_members, name='teams-update-members'),
]