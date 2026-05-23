from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.shortcuts import resolve_url as r
from http import HTTPStatus
from core.models import LinkModel

class LinkListarTemplateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='aluno',
            email='aluno@cps.sp.gov.br',
            password='fatec'
        )
        self.link = LinkModel.objects.create(
            titulo="Curso Cisco",
            link="https://www.netacad.com/career-paths/cybersecurity?courseLang=pt-BR",
            observacao="Curso gratuito de cibersegurança"
        )

    def test_get_anonimo_redireciona(self):
        response = self.client.get(r('listar_links'))
        self.assertTrue(response.status_code == HTTPStatus.FOUND)
        self.assertIn('/login/', response.url)

    def test_get_logado_carrega_template(self):
        self.client.login(username='aluno', password='fatec')
        response = self.client.get(r('listar_links'))
        self.assertTrue(response.status_code == HTTPStatus.OK)
        self.assertTemplateUsed(response, 'listar.html')

    def test_get_logado_exibe_registro(self):
        self.client.login(username='aluno', password='fatec')
        response = self.client.get(r('listar_links'))
        self.assertIn(self.link, response.context['links'])

    def test_get_busca_filtra_titulo(self):
        self.client.login(username='aluno', password='fatec')
        response = self.client.get(r('listar_links'), {'busca': 'curso'})
        self.assertTrue(response.status_code == HTTPStatus.OK)
        self.assertIn(self.link, response.context['links'])

    def test_get_busca_filtra_url(self):
        self.client.login(username='aluno', password='fatec')
        response = self.client.get(r('listar_links'), {'busca': 'netacad'})
        self.assertTrue(response.status_code == HTTPStatus.OK)
        self.assertIn(self.link, response.context['links'])

    def test_get_busca_filtra_observacao(self):
        self.client.login(username='aluno', password='fatec')
        response = self.client.get(r('listar_links'), {'busca': 'cibersegurança'})
        self.assertTrue(response.status_code == HTTPStatus.OK)
        self.assertIn(self.link, response.context['links'])