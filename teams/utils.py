from django.core.mail import send_mail
from users.models import JoinInvitation, JoinRequest

def send_email_invite(subject, message, email_from, email_to, fail, team, founder):
	return send_mail('Acabas de recibir una invitación - ' + subject,
					'Acaba de llegarte una invitación para unirte al equipo ' + team + ' su creador (' + founder + ') te manda el siguiente mensaje: ' + message, email_from, email_to, fail_silently=fail)

def create_invitation(user_to, from_user, team_to):
	new_invitation = JoinInvitation(to_user=user_to, from_user=from_user, team=team_to)
	new_request = JoinRequest(team=team_to, user=from_user)
	new_invitation.save()
	new_request.save()

def delete_invitation(to_user, team_from):
    old_invitation = JoinInvitation.objects.filter(to_user=to_user, team=team_from)
    old_request = JoinRequest.objects.filter(team=team_from, user=to_user)
    old_invitation.delete()
    old_request.delete()