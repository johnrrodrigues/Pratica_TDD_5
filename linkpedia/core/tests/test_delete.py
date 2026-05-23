from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.shortcuts import resolve_url as r
from http import HTTPStatus
from core.models import LinkModel


class LinkExclusaoTemplateTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="aluno", email="aluno@cps.sp.gov.br", password="fatec"
        )
        self.link = LinkModel.objects.create(
            titulo="Curso Cisco",
            link="https://www.netacad.com/career-paths/cybersecurity?courseLang=pt-BR",
            observacao="Curso de ciberseguranca",
        )

    def test_get_anonimo_redireciona(self):
        response = self.client.get(r("gerenciar_exclusao"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn("/login/", response.url)

    def test_get_autenticado_retorna_200(self):
        self.client.login(username="aluno", password="fatec")
        response = self.client.get(r("gerenciar_exclusao"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "excluir_listar.html")
        self.assertIn(self.link, response.context["links"])

    def test_get_busca_filtra_resultados(self):
        self.client.login(username="aluno", password="fatec")
        LinkModel.objects.create(titulo="GitHub", link="https://github.com")
        response = self.client.get(r("gerenciar_exclusao"), {"search": "Cisco"})
        self.assertEqual(len(response.context["links"]), 1)

    def test_post_anonimo_nao_exclui(self):
        response = self.client.post(r("excluir_link", pk=self.link.pk))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(LinkModel.objects.filter(pk=self.link.pk).exists())

    def test_post_autenticado_exclui(self):
        self.client.login(username="aluno", password="fatec")
        response = self.client.post(r("excluir_link", pk=self.link.pk))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(LinkModel.objects.filter(pk=self.link.pk).exists())

    def test_post_id_inexistente_retorna_404(self):
        self.client.login(username="aluno", password="fatec")
        response = self.client.post(r("excluir_link", pk=999))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
