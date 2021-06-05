from datetime import date
from django.contrib.auth.models import User
from django.core.mail import send_mail
from users.models import JoinInvitation, JoinRequest, Notification, Team

def send_email_invite(subject, message, email_from, email_to, fail, team, founder):
	return send_mail('Acabas de recibir una invitación - ' + subject,
					'Acaba de llegarte una invitación para unirte al equipo ' + team + ' su creador (' + founder + ') te manda el siguiente mensaje: ' + message, email_from, email_to, fail_silently=fail)

def create_invitation(user_to, from_user, team_to):
	new_invitation = JoinInvitation(to_user=user_to, team=team_to)
	new_invitation.save()
	new_notification = Notification(
		user = user_to,
		category = "Invitación de equipo",
		text = f'{from_user} te ha invitado a unirte a su equipo: "{team_to}".',
		join_invitation = new_invitation
	)
	new_notification.save()
	

def delete_invitation(to_user, team_from):
    old_invitation = JoinInvitation.objects.filter(to_user=to_user, team=team_from)
    old_invitation.delete()