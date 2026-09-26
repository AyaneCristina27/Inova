from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from datetime import timedelta
from django.http import HttpResponse
from django.utils import timezone

from .models import (
    Municipio, CategoriaAtor, Ator, Startup,
    Projeto, Evento, Especialista, CasoSucesso, Reuniao, Membro
)
from .forms import (
    MunicipioForm, CategoriaAtorForm, AtorForm, StartupForm,
    ProjetoForm, EventoForm, EspecialistaForm, EspecialistaCadastroPublicoForm,
    CasoSucessoForm, ReuniaoForm, MembroForm
)


# ---------------------------------------------------------------------
# Site público
# ---------------------------------------------------------------------

class IndexView(View):
    def get(self, request, *args, **kwargs):
        parceiros = Ator.objects.filter(ativo=True, eh_parceiro_estrategico=True)
        startups = Startup.objects.filter(ativo=True)[:6]
        municipios_startups = Municipio.objects.filter(
            startup__ativo=True
        ).distinct().order_by('nome')
        total_municipios = Municipio.objects.count()
        total_instituicoes = Ator.objects.filter(ativo=True).count()
        total_startups = startups.count()
        total_parceiros = parceiros.count()
        return render(request, 'index.html', {
            'parceiros': parceiros,
            'startups': startups,
            'municipios_startups': municipios_startups,
            'total_municipios': total_municipios,
            'total_instituicoes': total_instituicoes,
            'total_startups': total_startups,
            'total_parceiros': total_parceiros,
        })


# ---------------------------------------------------------------------
# Login / Logout do Gestor ("Área de membros")
# ---------------------------------------------------------------------

class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        lembrar_me = request.POST.get('lembrar_me')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)

            if lembrar_me:
                # sessão dura 2 semanas (em segundos)
                request.session.set_expiry(1209600)
            else:
                # expira quando o navegador for fechado
                request.session.set_expiry(0)

            return redirect('painel')

        messages.error(request, 'Usuário ou senha inválidos, ou sem permissão de gestor.')
        return render(request, 'login.html')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')


@method_decorator(login_required, name='dispatch')
class PainelView(View):
    def get(self, request, *args, **kwargs):
        proximas_reunioes = Reuniao.objects.filter(
            data_hora__gte=timezone.now()
        ).order_by('data_hora')[:3]
        return render(request, 'painel.html', {'proximas_reunioes': proximas_reunioes})
    
    
# ---------------------------------------------------------------------
# Municípios
# ---------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class MunicipiosView(View):
    def get(self, request, *args, **kwargs):
        municipios = Municipio.objects.all()
        return render(request, 'municipios.html', {'municipios': municipios})


@method_decorator(login_required, name='dispatch')
class CadastrarMunicipioView(View):
    def get(self, request, *args, **kwargs):
        form = MunicipioForm()
        return render(request, 'cadastrar_municipio.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = MunicipioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Município cadastrado com sucesso!')
            return redirect('municipios')
        return render(request, 'cadastrar_municipio.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditarMunicipioView(View):
    def get(self, request, id, *args, **kwargs):
        municipio = get_object_or_404(Municipio, id=id)
        form = MunicipioForm(instance=municipio)
        return render(request, 'editar_municipio.html', {'municipio': municipio, 'form': form})

    def post(self, request, id, *args, **kwargs):
        municipio = get_object_or_404(Municipio, id=id)
        form = MunicipioForm(request.POST, instance=municipio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Município atualizado com sucesso!')
            return redirect('municipios')
        return render(request, 'editar_municipio.html', {'municipio': municipio, 'form': form})


@method_decorator(login_required, name='dispatch')
class ExcluirMunicipioView(View):
    def get(self, request, id, *args, **kwargs):
        municipio = get_object_or_404(Municipio, id=id)
        municipio.delete()
        messages.success(request, 'Município excluído com sucesso!')
        return redirect('municipios')


# ---------------------------------------------------------------------
# Categorias de Ator
# ---------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class CategoriasView(View):
    def get(self, request, *args, **kwargs):
        categorias = CategoriaAtor.objects.all()
        return render(request, 'categorias.html', {'categorias': categorias})


@method_decorator(login_required, name='dispatch')
class CadastrarCategoriaView(View):
    def get(self, request, *args, **kwargs):
        form = CategoriaAtorForm()
        return render(request, 'cadastrar_categoria.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CategoriaAtorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria cadastrada com sucesso!')
            return redirect('categorias')
        return render(request, 'cadastrar_categoria.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditarCategoriaView(View):
    def get(self, request, id, *args, **kwargs):
        categoria = get_object_or_404(CategoriaAtor, id=id)
        form = CategoriaAtorForm(instance=categoria)
        return render(request, 'editar_categoria.html', {'categoria': categoria, 'form': form})

    def post(self, request, id, *args, **kwargs):
        categoria = get_object_or_404(CategoriaAtor, id=id)
        form = CategoriaAtorForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('categorias')
        return render(request, 'editar_categoria.html', {'categoria': categoria, 'form': form})


@method_decorator(login_required, name='dispatch')
class ExcluirCategoriaView(View):
    def get(self, request, id, *args, **kwargs):
        categoria = get_object_or_404(CategoriaAtor, id=id)
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('categorias')
    
    
# ---------------------------------------------------------------------
# Atores
# ---------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class AtoresView(View):
    def get(self, request, *args, **kwargs):
        atores = Ator.objects.all()
        return render(request, 'atores.html', {'atores': atores})


@method_decorator(login_required, name='dispatch')
class CadastrarAtorView(View):
    def get(self, request, *args, **kwargs):
        form = AtorForm()
        return render(request, 'cadastrar_ator.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AtorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ator cadastrado com sucesso!')
            return redirect('atores')
        return render(request, 'cadastrar_ator.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditarAtorView(View):
    def get(self, request, id, *args, **kwargs):
        ator = get_object_or_404(Ator, id=id)
        form = AtorForm(instance=ator)
        return render(request, 'editar_ator.html', {'ator': ator, 'form': form})

    def post(self, request, id, *args, **kwargs):
        ator = get_object_or_404(Ator, id=id)
        form = AtorForm(request.POST, request.FILES, instance=ator)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ator atualizado com sucesso!')
            return redirect('atores')
        return render(request, 'editar_ator.html', {'ator': ator, 'form': form})


@method_decorator(login_required, name='dispatch')
class ExcluirAtorView(View):
    def get(self, request, id, *args, **kwargs):
        ator = get_object_or_404(Ator, id=id)
        ator.delete()
        messages.success(request, 'Ator excluído com sucesso!')
        return redirect('atores')


# ---------------------------------------------------------------------
# Startups
# ---------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class StartupsView(View):
    def get(self, request, *args, **kwargs):
        startups = Startup.objects.all()
        return render(request, 'startups.html', {'startups': startups})


@method_decorator(login_required, name='dispatch')
class CadastrarStartupView(View):
    def get(self, request, *args, **kwargs):
        form = StartupForm()
        return render(request, 'cadastrar_startup.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = StartupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Startup cadastrada com sucesso!')
            return redirect('startups')
        return render(request, 'cadastrar_startup.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditarStartupView(View):
    def get(self, request, id, *args, **kwargs):
        startup = get_object_or_404(Startup, id=id)
        form = StartupForm(instance=startup)
        return render(request, 'editar_startup.html', {'startup': startup, 'form': form})

    def post(self, request, id, *args, **kwargs):
        startup = get_object_or_404(Startup, id=id)
        form = StartupForm(request.POST, request.FILES, instance=startup)
        if form.is_valid():
            form.save()
            messages.success(request, 'Startup atualizada com sucesso!')
            return redirect('startups')
        return render(request, 'editar_startup.html', {'startup': startup, 'form': form})


@method_decorator(login_required, name='dispatch')
class ExcluirStartupView(View):
    def get(self, request, id, *args, **kwargs):
        startup = get_object_or_404(Startup, id=id)
        startup.delete()
        messages.success(request, 'Startup excluída com sucesso!')
        return redirect('startups')
   
    
# ---------------------------------------------------------------------
# Projetos
# ---------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class ProjetosView(View):
    def get(self, request, *args, **kwargs):
        projetos = Projeto.objects.all()
        return render(request, 'projetos.html', {'projetos': projetos})


@method_decorator(login_required, name='dispatch')
class CadastrarProjetoView(View):
    def get(self, request, *args, **kwargs):
        form = ProjetoForm()
        return render(request, 'cadastrar_projeto.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ProjetoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Projeto cadastrado com sucesso!')
            return redirect('projetos')
        return render(request, 'cadastrar_projeto.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditarProjetoView(View):
    def get(self, request, id, *args, **kwargs):
        projeto = get_object_or_404(Projeto, id=id)
        form = ProjetoForm(instance=projeto)
        return render(request, 'editar_projeto.html', {'projeto': projeto, 'form': form})

    def post(self, request, id, *args, **kwargs):
        projeto = get_object_or_404(Projeto, id=id)
        form = ProjetoForm(request.POST, request.FILES, instance=projeto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Projeto atualizado com sucesso!')
            return redirect('projetos')
        return render(request, 'editar_projeto.html', {'projeto': projeto, 'form': form})
    

@method_decorator(login_required, name='dispatch')
class ExcluirProjetoView(View):
    def get(self, request, id, *args, **kwargs):
        projeto = get_object_or_404(Projeto, id=id)
        projeto.delete()
        messages.success(request, 'Projeto excluído com sucesso!')
        return redirect('projetos')


# ---------------------------------------------------------------------
# Eventos
# ---------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class EventosView(View):
    def get(self, request, *args, **kwargs):
        eventos = Evento.objects.all()
        return render(request, 'eventos.html', {'eventos': eventos})


@method_decorator(login_required, name='dispatch')
class CadastrarEventoView(View):
    def get(self, request, *args, **kwargs):
        form = EventoForm()
        return render(request, 'cadastrar_evento.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento cadastrado com sucesso!')
            return redirect('eventos')
        return render(request, 'cadastrar_evento.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditarEventoView(View):
    def get(self, request, id, *args, **kwargs):
        evento = get_object_or_404(Evento, id=id)
        form = EventoForm(instance=evento)
        return render(request, 'editar_evento.html', {'evento': evento, 'form': form})

    def post(self, request, id, *args, **kwargs):
        evento = get_object_or_404(Evento, id=id)
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento atualizado com sucesso!')
            return redirect('eventos')
        return render(request, 'editar_evento.html', {'evento': evento, 'form': form})


@method_decorator(login_required, name='dispatch')
class ExcluirEventoView(View):
    def get(self, request, id, *args, **kwargs):
        evento = get_object_or_404(Evento, id=id)
        evento.delete()
        messages.success(request, 'Evento excluído com sucesso!')
        return redirect('eventos')


# ---------------------------------------------------------------------
# Especialistas
# ---------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class EspecialistasView(View):
    def get(self, request, *args, **kwargs):
        especialistas = Especialista.objects.all()
        return render(request, 'especialistas.html', {'especialistas': especialistas})


@method_decorator(login_required, name='dispatch')
class CadastrarEspecialistaView(View):
    def get(self, request, *args, **kwargs):
        form = EspecialistaForm()
        return render(request, 'cadastrar_especialista.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = EspecialistaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Especialista cadastrado com sucesso!')
            return redirect('especialistas')
        return render(request, 'cadastrar_especialista.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditarEspecialistaView(View):
    def get(self, request, id, *args, **kwargs):
        especialista = get_object_or_404(Especialista, id=id)
        form = EspecialistaForm(instance=especialista)
        return render(request, 'editar_especialista.html', {'especialista': especialista, 'form': form})

    def post(self, request, id, *args, **kwargs):
        especialista = get_object_or_404(Especialista, id=id)
        form = EspecialistaForm(request.POST, request.FILES, instance=especialista)
        if form.is_valid():
            form.save()
            messages.success(request, 'Especialista atualizado com sucesso!')
            return redirect('especialistas')
        return render(request, 'editar_especialista.html', {'especialista': especialista, 'form': form})


@method_decorator(login_required, name='dispatch')
class ExcluirEspecialistaView(View):
    def get(self, request, id, *args, **kwargs):
        especialista = get_object_or_404(Especialista, id=id)
        especialista.delete()
        messages.success(request, 'Especialista excluído com sucesso!')
        return redirect('especialistas')


# ---------------------------------------------------------------------
# Casos de Sucesso
# ---------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class CasosSucessoView(View):
    def get(self, request, *args, **kwargs):
        casos_sucesso = CasoSucesso.objects.all()
        return render(request, 'casos_sucesso.html', {'casos_sucesso': casos_sucesso})


@method_decorator(login_required, name='dispatch')
class CadastrarCasoSucessoView(View):
    def get(self, request, *args, **kwargs):
        form = CasoSucessoForm()
        return render(request, 'cadastrar_caso_sucesso.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CasoSucessoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Caso de sucesso cadastrado com sucesso!')
            return redirect('casos_sucesso')
        return render(request, 'cadastrar_caso_sucesso.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditarCasoSucessoView(View):
    def get(self, request, id, *args, **kwargs):
        caso = get_object_or_404(CasoSucesso, id=id)
        form = CasoSucessoForm(instance=caso)
        return render(request, 'editar_caso_sucesso.html', {'caso': caso, 'form': form})

    def post(self, request, id, *args, **kwargs):
        caso = get_object_or_404(CasoSucesso, id=id)
        form = CasoSucessoForm(request.POST, request.FILES, instance=caso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Caso de sucesso atualizado com sucesso!')
            return redirect('casos_sucesso')
        return render(request, 'editar_caso_sucesso.html', {'caso': caso, 'form': form})


@method_decorator(login_required, name='dispatch')
class ExcluirCasoSucessoView(View):
    def get(self, request, id, *args, **kwargs):
        caso = get_object_or_404(CasoSucesso, id=id)
        caso.delete()
        messages.success(request, 'Caso de sucesso excluído com sucesso!')
        return redirect('casos_sucesso')


# ---------------------------------------------------------------------
# Reuniões
# ---------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class ReunioesView(View):
    def get(self, request, *args, **kwargs):
        reunioes = Reuniao.objects.all()
        return render(request, 'reunioes.html', {'reunioes': reunioes})


@method_decorator(login_required, name='dispatch')
class CadastrarReuniaoView(View):
    def get(self, request, *args, **kwargs):
        form = ReuniaoForm()
        return render(request, 'cadastrar_reuniao.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ReuniaoForm(request.POST)
        if form.is_valid():
            reuniao = form.save(commit=False)
            reuniao.criado_por = request.user
            reuniao.save()
            messages.success(request, 'Reunião marcada com sucesso!')
            return redirect('reunioes')
        return render(request, 'cadastrar_reuniao.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditarReuniaoView(View):
    def get(self, request, id, *args, **kwargs):
        reuniao = get_object_or_404(Reuniao, id=id)
        form = ReuniaoForm(instance=reuniao)
        return render(request, 'editar_reuniao.html', {'reuniao': reuniao, 'form': form})

    def post(self, request, id, *args, **kwargs):
        reuniao = get_object_or_404(Reuniao, id=id)
        form = ReuniaoForm(request.POST, instance=reuniao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reunião atualizada com sucesso!')
            return redirect('reunioes')
        return render(request, 'editar_reuniao.html', {'reuniao': reuniao, 'form': form})


@method_decorator(login_required, name='dispatch')
class ExcluirReuniaoView(View):
    def get(self, request, id, *args, **kwargs):
        reuniao = get_object_or_404(Reuniao, id=id)
        reuniao.delete()
        messages.success(request, 'Reunião excluída com sucesso!')
        return redirect('reunioes')
    

# ---------------------------------------------------------------------
# Membros
# ---------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class MembrosView(View):
    def get(self, request, *args, **kwargs):
        membros = Membro.objects.all()
        return render(request, 'membros.html', {'membros': membros})


@method_decorator(login_required, name='dispatch')
class CadastrarMembroView(View):
    def get(self, request, *args, **kwargs):
        form = MembroForm()
        return render(request, 'cadastrar_membro.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = MembroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membro cadastrado com sucesso!')
            return redirect('membros')
        return render(request, 'cadastrar_membro.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditarMembroView(View):
    def get(self, request, id, *args, **kwargs):
        membro = get_object_or_404(Membro, id=id)
        form = MembroForm(instance=membro)
        return render(request, 'editar_membro.html', {'membro': membro, 'form': form})

    def post(self, request, id, *args, **kwargs):
        membro = get_object_or_404(Membro, id=id)
        form = MembroForm(request.POST, request.FILES, instance=membro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membro atualizado com sucesso!')
            return redirect('membros')
        return render(request, 'editar_membro.html', {'membro': membro, 'form': form})


@method_decorator(login_required, name='dispatch')
class ExcluirMembroView(View):
    def get(self, request, id, *args, **kwargs):
        membro = get_object_or_404(Membro, id=id)
        membro.delete()
        messages.success(request, 'Membro excluído com sucesso!')
        return redirect('membros')
    
    
class MembrosPublicoView(View):
    def get(self, request, *args, **kwargs):
        membros = Membro.objects.filter(ativo=True)
        return render(request, 'membros_publico.html', {'membros': membros})
    

class EventosPublicoView(View):
    def get(self, request, *args, **kwargs):
        eventos = Evento.objects.all().order_by('data_inicio')
        return render(request, 'agenda.html', {
            'eventos': eventos,
            'tipo_evento_choices': Evento.TIPO_EVENTO_CHOICES,
        })


class ProjetosPublicoView(View):
    def get(self, request, *args, **kwargs):
        projetos = Projeto.objects.all().order_by('-criado_em')
        return render(request, 'projetos_publico.html', {'projetos': projetos})


class CasosSucessoPublicoView(View):
    def get(self, request, *args, **kwargs):
        casos_sucesso = CasoSucesso.objects.filter(publicado=True).order_by('-data_publicacao')
        return render(request, 'casos_sucesso_publico.html', {'casos_sucesso': casos_sucesso})
    
class EspecialistasPublicoView(View):
    def get(self, request, *args, **kwargs):
        especialistas = Especialista.objects.filter(ativo=True).select_related('ator', 'ator__municipio')

        areas = set()
        for especialista in especialistas:
            if especialista.area_atuacao:
                for area in especialista.area_atuacao.split(','):
                    area = area.strip()
                    if area:
                        areas.add(area)

        instituicoes = sorted({
            especialista.ator.nome for especialista in especialistas if especialista.ator
        })

        return render(request, 'especialistas_publico.html', {
            'especialistas': especialistas,
            'areas_atuacao': sorted(areas),
            'instituicoes': instituicoes,
            'tipo_apoio_choices': Especialista.TIPO_APOIO_CHOICES,
        })


class CadastrarEspecialistaPublicoView(View):
    def get(self, request, *args, **kwargs):
        form = EspecialistaCadastroPublicoForm()
        return render(request, 'cadastrar_especialista_publico.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = EspecialistaCadastroPublicoForm(request.POST, request.FILES)
        if form.is_valid():
            especialista = form.save(commit=False)
            especialista.ativo = False
            especialista.save()
            return redirect('cadastro_especialista_sucesso')
        return render(request, 'cadastrar_especialista_publico.html', {'form': form})


class CadastroEspecialistaSucessoView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cadastro_especialista_sucesso.html')
    
    
# ---------------------------------------------------------------------
# Integração com calendário pessoal (.ics)
# ---------------------------------------------------------------------

def gerar_ics(titulo, data_inicio, data_fim, local, descricao, uid):
    fmt = '%Y%m%dT%H%M%SZ'
    inicio = data_inicio.astimezone(timezone.utc).strftime(fmt)
    fim = data_fim.astimezone(timezone.utc).strftime(fmt)
    agora = timezone.now().astimezone(timezone.utc).strftime(fmt)
    local_ics = local or ""
    descricao_ics = (descricao or "").replace("\n", "\\n")
    linhas = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//INova Sudoeste de Minas//PT-BR",
        "BEGIN:VEVENT",
        "UID:%s@inovasudoestedeminas" % uid,
        "DTSTAMP:%s" % agora,
        "DTSTART:%s" % inicio,
        "DTEND:%s" % fim,
        "SUMMARY:%s" % titulo,
        "LOCATION:%s" % local_ics,
        "DESCRIPTION:%s" % descricao_ics,
        "END:VEVENT",
        "END:VCALENDAR",
        "",
    ]
    return "\r\n".join(linhas)


@method_decorator(login_required, name='dispatch')
class ReuniaoICSView(View):
    def get(self, request, id, *args, **kwargs):
        reuniao = get_object_or_404(Reuniao, id=id)
        data_fim = reuniao.data_hora + timedelta(hours=1)
        conteudo = gerar_ics(
            reuniao.titulo, reuniao.data_hora, data_fim,
            reuniao.local, reuniao.descricao, "reuniao-%s" % reuniao.id
        )
        response = HttpResponse(conteudo, content_type="text/calendar")
        response["Content-Disposition"] = "attachment; filename=\"reuniao-%s.ics\"" % reuniao.id
        return response


class EventoICSView(View):
    def get(self, request, id, *args, **kwargs):
        evento = get_object_or_404(Evento, id=id)
        data_fim = evento.data_fim or (evento.data_inicio + timedelta(hours=2))
        conteudo = gerar_ics(
            evento.titulo, evento.data_inicio, data_fim,
            evento.local, evento.descricao, "evento-%s" % evento.id
        )
        response = HttpResponse(conteudo, content_type="text/calendar")
        response["Content-Disposition"] = "attachment; filename=\"evento-%s.ics\"" % evento.id
        return response
    
    
class StartupsPublicoView(View):
    def get(self, request, *args, **kwargs):
        startups = Startup.objects.filter(ativo=True)
        municipios_startups = Municipio.objects.filter(
            startup__ativo=True
        ).distinct().order_by('nome')
        return render(request, 'nossas_startups.html', {
            'startups': startups,
            'municipios_startups': municipios_startups,
        })