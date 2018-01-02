from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpResponseRedirect


class AccountAdapter(DefaultAccountAdapter):
  def get_login_redirect_url(self, request):
    if request.POST and 'statut' in request.POST:
      statut = request.POST['statut']
    else :
      statut = "etudiant"
    path = "/etudiants/completer-profil/{statut}/"
    return path.format(statut=statut)
