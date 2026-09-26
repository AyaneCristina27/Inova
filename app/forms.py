from django import forms
from .models import (
    Municipio, CategoriaAtor, Ator, Startup,
    Projeto, Evento, Especialista, CasoSucesso, Reuniao, Membro
)


class MunicipioForm(forms.ModelForm):
    class Meta:
        model = Municipio
        fields = '__all__'


class CategoriaAtorForm(forms.ModelForm):
    class Meta:
        model = CategoriaAtor
        fields = '__all__'


class AtorForm(forms.ModelForm):
    class Meta:
        model = Ator
        fields = '__all__'


class StartupForm(forms.ModelForm):
    class Meta:
        model = Startup
        fields = '__all__'


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = '__all__'


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'


class EspecialistaForm(forms.ModelForm):
    class Meta:
        model = Especialista
        fields = '__all__'


class CasoSucessoForm(forms.ModelForm):
    class Meta:
        model = CasoSucesso
        fields = '__all__'


class ReuniaoForm(forms.ModelForm):
    class Meta:
        model = Reuniao
        fields = ['titulo', 'data_hora', 'local', 'descricao']
        # "criado_por" fica de fora do formulário -
        # é preenchido automaticamente pela View, com o gestor logado.


class MembroForm(forms.ModelForm):
    class Meta:
        model = Membro
        fields = '__all__'
        
        
class EspecialistaCadastroPublicoForm(forms.ModelForm):
    class Meta:
        model = Especialista
        fields = ['nome', 'area_atuacao', 'tipo_apoio', 'bio', 'foto', 'email', 'telefone', 'linkedin']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }