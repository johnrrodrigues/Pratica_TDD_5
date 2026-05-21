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
            username='aluno',
            email='aluno@cps.sp.gov.br',
            password='fatec'
        )

    def test_get_anonimo_redireciona(self):
        response = self.client.get(r('cadastrar_link'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('/login/', response.url)

    def test_post_anonimo_nao_salva(self):
        dados = {
            'titulo': 'Link sem login',
            'link': 'https://www.figma.com/',
            'observacao': 'Tentativa sem login'
        }
        response = self.client.post(r('cadastrar_link'), dados)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(LinkModel.objects.filter(titulo='Link sem login').exists())

    def test_get_autenticado_retorna_200(self):
        self.client.login(username='aluno', password='fatec')
        response = self.client.get(r('cadastrar_link'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'cadastrar.html')
        self.assertIsInstance(response.context['form'], LinkForm)

    def test_post_dados_validos_salva_e_redireciona(self):
        self.client.login(username='aluno', password='fatec')
        dados = {
            'titulo': 'Linux Essentials',
            'link': 'https://www.netacad.com/courses/linux-essentials/?courseLang=en-US',
            'observacao': 'Curso de introdução ao linux'
        }
        response = self.client.post(r('cadastrar_link'), dados)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(LinkModel.objects.filter(titulo='Linux Essentials').exists())

    def test_post_dados_invalidos_nao_salva(self):
        self.client.login(username='aluno', password='fatec')
        dados = {
            'titulo': 'Link inválido',
            'link': 'site_sem_http',
            'observacao': 'Inválido'
        }
        response = self.client.post(r('cadastrar_link'), dados)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('link', response.context['form'].errors)
        self.assertFalse(LinkModel.objects.filter(titulo='Link inválido').exists())