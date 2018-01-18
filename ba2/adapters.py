from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpResponseRedirect


class AccountAdapter(DefaultAccountAdapter):
  def get_login_redirect_url(self, request):

    if request.POST and 'statut' in request.POST:
      statut = request.POST['statut']
      if 'next' in request.POST:
        path = "/{statut}/completer-profil/?next=" + request.POST['next']
      else :
        path = "/{statut}/completer-profil/?next="
      return path.format(statut=statut)
    elif request.POST and  'next' in request.POST:
      path = request.POST['next']
      return path
    else :
      path = "/"
      return path

