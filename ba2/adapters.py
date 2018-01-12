from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpResponseRedirect


class AccountAdapter(DefaultAccountAdapter):
  def get_login_redirect_url(self, request):

    if request.POST and 'statut' in request.POST:
      statut = request.POST['statut']
      path = "/{statut}/completer-profil/?next=/qdsfqdfs/"
      return path.format(statut=statut)
    else :
      path = "/"
      return path

