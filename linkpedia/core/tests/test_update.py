from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.shortcuts import resolve_url as r
from http import HTTPStatus
from core.models import LinkModel
from core.forms import LinkForm


class LinkEdicaoTemplateTest(TestCase):

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

    def test_gerenciar_get_anonimo_redireciona(self):
        response = self.client.get(r("gerenciar_edicao"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn("/login/", response.url)

    def test_gerenciar_get_autenticado_retorna_200(self):
        self.client.login(username="aluno", password="fatec")
        response = self.client.get(r("gerenciar_edicao"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "editar_listar.html")
        self.assertIn(self.link, response.context["links"])

    def test_gerenciar_busca_filtra_resultados(self):
        self.client.login(username="aluno", password="fatec")
        LinkModel.objects.create(titulo="GitHub", link="https://github.com")

        response = self.client.get(r("gerenciar_edicao"), {"search": "Cisco"})
        self.assertEqual(len(response.context["links"]), 1)

        response = self.client.get(r("gerenciar_edicao"), {"search": "Inexistente"})
        self.assertEqual(len(response.context["links"]), 0)

    def test_editar_get_anonimo_redireciona(self):
        response = self.client.get(r("editar_link", pk=self.link.pk))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn("/login/", response.url)

    def test_editar_id_inexistente_retorna_404(self):
        self.client.login(username="aluno", password="fatec")
        response = self.client.get(r("editar_link", pk=999))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_editar_get_autenticado_carrega_form_preenchido(self):
        self.client.login(username="aluno", password="fatec")
        response = self.client.get(r("editar_link", pk=self.link.pk))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "editar.html")
        self.assertIsInstance(response.context["form"], LinkForm)
        self.assertEqual(response.context["form"].instance, self.link)

    def test_editar_post_valido_atualiza_e_redireciona(self):
        self.client.login(username="aluno", password="fatec")
        dados = {
            "titulo": "Cisco Atualizado",
            "link": "https://www.netacad.com/career-paths/cybersecurity?courseLang=pt-BR",
            "observacao": "Curso de ciberseguranca atualizado",
        }
        response = self.client.post(r("editar_link", pk=self.link.pk), dados)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, r("gerenciar_edicao"))
        self.link.refresh_from_db()
        self.assertEqual(self.link.titulo, "Cisco Atualizado")

    def test_editar_post_mesma_url_permite(self):
        self.client.login(username="aluno", password="fatec")
        dados = {
            "titulo": "Cisco Cybersecurity",
            "link": "https://www.netacad.com/career-paths/cybersecurity?courseLang=pt-BR",
            "observacao": "Apenas mudei o titulo",
        }
        response = self.client.post(r("editar_link", pk=self.link.pk), dados)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.link.refresh_from_db()
        self.assertEqual(self.link.titulo, "Cisco Cybersecurity")

    def test_editar_post_url_duplicada_barra(self):
        LinkModel.objects.create(titulo="GitHub", link="https://github.com")
        self.client.login(username="aluno", password="fatec")
        dados = {
            "titulo": "Cisco Fraudulento",
            "link": "https://github.com",
            "observacao": "Tentando forçar erro",
        }
        response = self.client.post(r("editar_link", pk=self.link.pk), dados)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("link", response.context["form"].errors)
        self.link.refresh_from_db()
        self.assertEqual(self.link.titulo, "Curso Cisco")
