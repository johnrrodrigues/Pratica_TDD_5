from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.shortcuts import resolve_url as r
from http import HTTPStatus
from core.models import LinkModel
from core.forms import LinkForm

class LinkCadastroTemplateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="aluno", 
            email="aluno@cps.sp.gov.br", 
            password="fatec"
        )

    def test_get_anonimo_redireciona(self):
        response = self.client.get(r("cadastrar_link"))
        self.assertTrue(response.status_code == HTTPStatus.FOUND)
        self.assertIn("/login/", response.url)

    def test_post_anonimo_nao_salva(self):
        dados = {
            "titulo": "Sem login",
            "link": "https://figma.com",
            "observacao": "Tentativa",
        }
        response = self.client.post(r("cadastrar_link"), dados)
        self.assertTrue(response.status_code == HTTPStatus.FOUND)
        self.assertFalse(LinkModel.objects.filter(titulo="Sem login").exists())

    def test_get_autenticado_carrega_template(self):
        self.client.login(username="aluno", password="fatec")
        response = self.client.get(r("cadastrar_link"))
        self.assertTrue(response.status_code == HTTPStatus.OK)
        self.assertTemplateUsed(response, "cadastrar.html")
        self.assertIsInstance(response.context["form"], LinkForm)

    def test_post_dados_validos_salva(self):
        self.client.login(username="aluno", password="fatec")
        dados = {
            "titulo": "Linux Essentials",
            "link": "https://netacad.com",
            "observacao": "Curso linux",
        }
        response = self.client.post(r("cadastrar_link"), dados)
        self.assertTrue(response.status_code == HTTPStatus.FOUND)
        self.assertTrue(LinkModel.objects.filter(titulo="Linux Essentials").exists())

    def test_post_dados_invalidos_barra(self):
        self.client.login(username="aluno", password="fatec")
        dados = {
            "titulo": "Invalido",
            "link": "site_sem_http",
            "observacao": "Erro",
        }
        response = self.client.post(r("cadastrar_link"), dados)
        self.assertTrue(response.status_code == HTTPStatus.OK)
        self.assertIn("link", response.context["form"].errors)
        self.assertFalse(LinkModel.objects.filter(titulo="Invalido").exists())

    def test_post_duplicado_retorna_erro(self):
        self.client.login(username="aluno", password="fatec")
        LinkModel.objects.create(titulo="Original", link="https://original.com")
        dados = {"titulo": "Copia", "link": "https://original.com", "observacao": ""}
        response = self.client.post(r("cadastrar_link"), dados)
        self.assertTrue(response.status_code == HTTPStatus.OK)
        self.assertIn("link", response.context["form"].errors)