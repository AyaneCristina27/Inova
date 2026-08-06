from django.conf import settings
from django.db import models


class Municipio(models.Model):
    nome = models.CharField(
        max_length=100, unique=True, verbose_name="Nome do município"
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Município"
        verbose_name_plural = "Municípios"


class CategoriaAtor(models.Model):
    nome = models.CharField(
        max_length=100, unique=True, verbose_name="Nome da categoria"
    )
    icone = models.CharField(
        max_length=50, blank=True, verbose_name="Ícone (Font Awesome)"
    )
    descricao = models.TextField(blank=True, verbose_name="Descrição da categoria")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria de Ator"
        verbose_name_plural = "Categorias de Atores"


class Ator(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome do ator")
    categoria = models.ForeignKey(
        CategoriaAtor, on_delete=models.PROTECT, verbose_name="Categoria do ator"
    )
    municipio = models.ForeignKey(
        Municipio, on_delete=models.PROTECT, verbose_name="Município do ator"
    )
    descricao = models.TextField(blank=True, verbose_name="Descrição do ator")
    site = models.CharField(max_length=200, blank=True, verbose_name="Site do ator")
    contato_email = models.CharField(
        max_length=100, blank=True, verbose_name="Email de contato"
    )
    contato_telefone = models.CharField(
        max_length=20, blank=True, verbose_name="Telefone de contato"
    )
    eh_parceiro_estrategico = models.BooleanField(
        default=False, verbose_name="É parceiro estratégico"
    )
    ativo = models.BooleanField(default=True, verbose_name="Status do ator")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    atualizado_em = models.DateTimeField(
        auto_now=True, verbose_name="Data de atualização"
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Ator"
        verbose_name_plural = "Atores"


class Startup(models.Model):
    ESTAGIO_CHOICES = [
        ("ideacao", "Ideação"),
        ("validacao", "Validação"),
        ("tracao", "Tração"),
        ("escala", "Escala"),
    ]

    nome = models.CharField(max_length=200, verbose_name="Nome da startup")
    municipio = models.ForeignKey(
        Municipio, on_delete=models.PROTECT, verbose_name="Município da startup"
    )
    setor_atuacao = models.CharField(
        max_length=150, blank=True, verbose_name="Setor de atuação"
    )
    estagio = models.CharField(
        max_length=20,
        choices=ESTAGIO_CHOICES,
        default="ideacao",
        verbose_name="Estágio da startup",
    )
    data_fundacao = models.DateField(
        blank=True, null=True, verbose_name="Data de fundação"
    )
    descricao = models.TextField(blank=True, verbose_name="Descrição da startup")
    site = models.CharField(max_length=200, blank=True, verbose_name="Site da startup")
    ativo = models.BooleanField(default=True, verbose_name="Status da startup")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    atualizado_em = models.DateTimeField(
        auto_now=True, verbose_name="Data de atualização"
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Startup"
        verbose_name_plural = "Startups"


class Projeto(models.Model):
    STATUS_CHOICES = [
        ("planejado", "Planejado"),
        ("em_andamento", "Em andamento"),
        ("concluido", "Concluído"),
    ]

    titulo = models.CharField(max_length=200, verbose_name="Título do projeto")
    descricao = models.TextField(blank=True, verbose_name="Descrição do projeto")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planejado",
        verbose_name="Status do projeto",
    )
    data_inicio = models.DateField(blank=True, null=True, verbose_name="Data de início")
    data_fim = models.DateField(blank=True, null=True, verbose_name="Data de fim")
    instituicoes = models.ManyToManyField(
        Ator, blank=True, verbose_name="Instituições do projeto"
    )
    startups = models.ManyToManyField(
        Startup, blank=True, verbose_name="Startups do projeto"
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    atualizado_em = models.DateTimeField(
        auto_now=True, verbose_name="Data de atualização"
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"


class Evento(models.Model):
    MODALIDADE_CHOICES = [
        ("presencial", "Presencial"),
        ("online", "Online"),
        ("hibrido", "Híbrido"),
    ]

    titulo = models.CharField(max_length=200, verbose_name="Título do evento")
    descricao = models.TextField(blank=True, verbose_name="Descrição do evento")
    data_inicio = models.DateTimeField(verbose_name="Data/hora de início")
    data_fim = models.DateTimeField(
        blank=True, null=True, verbose_name="Data/hora de fim"
    )
    local = models.CharField(max_length=200, blank=True, verbose_name="Local do evento")
    municipio = models.ForeignKey(
        Municipio,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Município do evento",
    )
    modalidade = models.CharField(
        max_length=20,
        choices=MODALIDADE_CHOICES,
        default="presencial",
        verbose_name="Modalidade do evento",
    )
    link_inscricao = models.CharField(
        max_length=200, blank=True, verbose_name="Link de inscrição"
    )
    imagem_capa = models.ImageField(
        upload_to="eventos/capas/", blank=True, null=True, verbose_name="Imagem de capa"
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    atualizado_em = models.DateTimeField(
        auto_now=True, verbose_name="Data de atualização"
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"


class Especialista(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome do especialista")
    area_atuacao = models.CharField(
        max_length=150, blank=True, verbose_name="Área de atuação"
    )
    bio = models.TextField(blank=True, verbose_name="Biografia")
    foto = models.ImageField(
        upload_to="especialistas/fotos/", blank=True, null=True, verbose_name="Foto"
    )
    email = models.CharField(max_length=100, blank=True, verbose_name="Email")
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    linkedin = models.CharField(max_length=200, blank=True, verbose_name="LinkedIn")
    ator = models.ForeignKey(
        Ator,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Instituição vinculada",
    )
    ativo = models.BooleanField(default=True, verbose_name="Status do especialista")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Especialista"
        verbose_name_plural = "Especialistas"


class CasoSucesso(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título do caso de sucesso")
    resumo = models.CharField(max_length=300, blank=True, verbose_name="Resumo")
    conteudo = models.TextField(blank=True, verbose_name="Conteúdo")
    imagem = models.ImageField(
        upload_to="casos_sucesso/", blank=True, null=True, verbose_name="Imagem"
    )
    startup = models.ForeignKey(
        Startup,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Startup relacionada",
    )
    ator = models.ForeignKey(
        Ator,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Ator relacionado",
    )
    data_publicacao = models.DateField(
        auto_now_add=True, verbose_name="Data de publicação"
    )
    publicado = models.BooleanField(default=True, verbose_name="Status de publicação")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Caso de Sucesso"
        verbose_name_plural = "Casos de Sucesso"


class Reuniao(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título da reunião")
    data_hora = models.DateTimeField(verbose_name="Data e hora da reunião")
    local = models.CharField(max_length=200, blank=True, verbose_name="Local da reunião")
    descricao = models.TextField(blank=True, verbose_name="Descrição/pauta da reunião")
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Gestor que marcou a reunião",
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Reunião"
        verbose_name_plural = "Reuniões"
        ordering = ["data_hora"]