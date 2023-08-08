from django.shortcuts import render,redirect,reverse
from .models import Filme,Usuario
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CriarContaForm, FormHomepage
# Create your views here.
from django.views.generic import TemplateView,ListView,DetailView,FormView,UpdateView
#def homepage(request):
#   return render(request,"homepage.html")

class Homepage(FormView):
    template_name = "homepage.html"
    form_class = FormHomepage

    def get(self, request, *args, **Kwargs):
        if request.user.is_authenticated:
            return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **Kwargs)

    def get_success_url(self):
        email= self.request.POST.get('email')
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')


class Homefilmes(LoginRequiredMixin, ListView):
    template_name = "homefilme.html"
    model = Filme


class DetalhesFilme(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilme.html"
    model = Filme

    def get(self, request, *args, **Kwargs):
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save()
        usuario = request.user
        usuario.filme_vistos.add(filme)

        return super().get(request, *args, **Kwargs)




    def get_context_data(self, **kwargs):
        context =super(DetalhesFilme, self).get_context_data(**kwargs)
        filmes_relacionados =Filme.objects.filter(categoria=self.get_object().categoria)[0:5]
        context['filmes_relacionados']= filmes_relacionados
        return context

class PesquisaFilme(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Filme

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list =Filme.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None

class Paginaperfil(LoginRequiredMixin,UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ['first_name','last_name','email']

    def get_success_url(self):
        return reverse('filme:homefilmes')

class Criarconta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('filme:login')