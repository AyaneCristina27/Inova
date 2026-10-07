from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from app.views import *
from django.contrib.auth import views as auth_views

import app.dash_app  # noqa: F401  (registra o dashboard Dash)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Dashboard em Dash (usado pelo {% plotly_direct %} no template)
    path('django_plotly_dash/', include('django_plotly_dash.urls')),

    # Site público
    path('', IndexView.as_view(), name='index'),

    # Login / Logout / Painel do Gestor
    path('login/', LoginView.as_view(), name='login'),

    path('esqueci-senha/', auth_views.PasswordResetView.as_view(
        template_name='password_reset_form.html',
        email_template_name='password_reset_email.html',
        html_email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt',
        success_url='/esqueci-senha/enviado/'
    ), name='password_reset'),

    path('esqueci-senha/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),

    path('esqueci-senha/confirmar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
        success_url='/esqueci-senha/concluido/'
    ), name='password_reset_confirm'),

    path('esqueci-senha/concluido/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),

    path('logout/', LogoutView.as_view(), name='logout'),
    path('painel/', PainelView.as_view(), name='painel'),

    # Municípios
    path('municipios/', MunicipiosView.as_view(), name='municipios'),
    path('municipios/cadastrar/', CadastrarMunicipioView.as_view(), name='cadastrar_municipio'),
    path('municipios/editar/<int:id>/', EditarMunicipioView.as_view(), name='editar_municipio'),
    path('municipios/excluir/<int:id>/', ExcluirMunicipioView.as_view(), name='excluir_municipio'),

    # Categorias de Ator
    path('categorias/', CategoriasView.as_view(), name='categorias'),
    path('categorias/cadastrar/', CadastrarCategoriaView.as_view(), name='cadastrar_categoria'),
    path('categorias/editar/<int:id>/', EditarCategoriaView.as_view(), name='editar_categoria'),
    path('categorias/excluir/<int:id>/', ExcluirCategoriaView.as_view(), name='excluir_categoria'),

    # Atores
    path('atores/', AtoresView.as_view(), name='atores'),
    path('atores/cadastrar/', CadastrarAtorView.as_view(), name='cadastrar_ator'),
    path('atores/editar/<int:id>/', EditarAtorView.as_view(), name='editar_ator'),
    path('atores/excluir/<int:id>/', ExcluirAtorView.as_view(), name='excluir_ator'),

    # Startups
    path('startups/', StartupsView.as_view(), name='startups'),
    path('startups/cadastrar/', CadastrarStartupView.as_view(), name='cadastrar_startup'),
    path('startups/editar/<int:id>/', EditarStartupView.as_view(), name='editar_startup'),
    path('startups/excluir/<int:id>/', ExcluirStartupView.as_view(), name='excluir_startup'),

    # Projetos
    path('projetos/', ProjetosView.as_view(), name='projetos'),
    path('projetos/cadastrar/', CadastrarProjetoView.as_view(), name='cadastrar_projeto'),
    path('projetos/editar/<int:id>/', EditarProjetoView.as_view(), name='editar_projeto'),
    path('projetos/excluir/<int:id>/', ExcluirProjetoView.as_view(), name='excluir_projeto'),

    # Eventos
    path('eventos/', EventosView.as_view(), name='eventos'),
    path('eventos/cadastrar/', CadastrarEventoView.as_view(), name='cadastrar_evento'),
    path('eventos/editar/<int:id>/', EditarEventoView.as_view(), name='editar_evento'),
    path('eventos/excluir/<int:id>/', ExcluirEventoView.as_view(), name='excluir_evento'),

    # Especialistas
    path('especialistas/', EspecialistasView.as_view(), name='especialistas'),
    path('especialistas/cadastrar/', CadastrarEspecialistaView.as_view(), name='cadastrar_especialista'),
    path('especialistas/editar/<int:id>/', EditarEspecialistaView.as_view(), name='editar_especialista'),
    path('especialistas/excluir/<int:id>/', ExcluirEspecialistaView.as_view(), name='excluir_especialista'),

    # Casos de Sucesso
    path('casos-sucesso/', CasosSucessoView.as_view(), name='casos_sucesso'),
    path('casos-sucesso/cadastrar/', CadastrarCasoSucessoView.as_view(), name='cadastrar_caso_sucesso'),
    path('casos-sucesso/editar/<int:id>/', EditarCasoSucessoView.as_view(), name='editar_caso_sucesso'),
    path('casos-sucesso/excluir/<int:id>/', ExcluirCasoSucessoView.as_view(), name='excluir_caso_sucesso'),

    # Reuniões
    path('reunioes/', ReunioesView.as_view(), name='reunioes'),
    path('reunioes/cadastrar/', CadastrarReuniaoView.as_view(), name='cadastrar_reuniao'),
    path('reunioes/editar/<int:id>/', EditarReuniaoView.as_view(), name='editar_reuniao'),
    path('reunioes/excluir/<int:id>/', ExcluirReuniaoView.as_view(), name='excluir_reuniao'),

    # Membros
    path('membros/', MembrosView.as_view(), name='membros'),
    path('membros/cadastrar/', CadastrarMembroView.as_view(), name='cadastrar_membro'),
    path('membros/editar/<int:id>/', EditarMembroView.as_view(), name='editar_membro'),
    path('membros/excluir/<int:id>/', ExcluirMembroView.as_view(), name='excluir_membro'),

    # Integração com calendário pessoal (.ics)
    path('reunioes/<int:id>/calendario/', ReuniaoICSView.as_view(), name='reuniao_ics'),
    path('eventos/<int:id>/calendario/', EventoICSView.as_view(), name='evento_ics'),

    # Página pública de Membros
    path('nossos-membros/', MembrosPublicoView.as_view(), name='membros_publico'),

    # Páginas públicas: Eventos, Projetos, Casos de Sucesso, Startups, Especialistas
    path('agenda/', EventosPublicoView.as_view(), name='eventos_publico'),
    path('nossos-projetos/', ProjetosPublicoView.as_view(), name='projetos_publico'),
    path('casos-de-sucesso/', CasosSucessoPublicoView.as_view(), name='casos_sucesso_publico'),
    path('nossas-startups/', StartupsPublicoView.as_view(), name='startups_publico'),
    path('nossos-especialistas/', EspecialistasPublicoView.as_view(), name='especialistas_publico'),
    path('nossos-especialistas/cadastrar/', CadastrarEspecialistaPublicoView.as_view(), name='cadastrar_especialista_publico'),
    path('nossos-especialistas/cadastro-enviado/', CadastroEspecialistaSucessoView.as_view(), name='cadastro_especialista_sucesso'),
]

# Serve arquivos de mídia (fotos, capas de eventos etc.) em desenvolvimento.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)