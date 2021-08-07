from django.test import TestCase, Client, RequestFactory
from django.urls import resolve 
from django.contrib.auth import get_user_model

from snippets.views import top, snippet_new, snippet_edit, snippet_detail
from snippets.models import Snippet

UserModel = get_user_model()

class TopPageTest(TestCase):
    def test_top_page_returns_200_and_expected_title(self):
        response = self.client.get("/")
        self.assertContains(response, "Django Snippet", status_code=200)

    def test_top_page_uses_expected_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "snippets/top.html")

class TopPageRenderSnippetsTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username = "test_user",
            email = "test@example.com",
            password = "top_secret_pass0001",
        )
        self.snippet = Snippet.objects.create(
            title = "title1",
            code = "print('hello')",
            description = "description1",
            created_by = self.user,
        )

    def test_should_return_snippet_title(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.snippet.title)

    def test_should_return_username(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.user.username)

class CreateSnippetTest(TestCase):
    def test_should_resolve_snippet_new(self):
        found = resolve('/snippets/new/')
        self.assertEqual(snippet_new, found.func)

class SnippetDetailTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
                username = "test_user",
                email = "test@example.com",
                password = "secret",
            )
        self.snippet = Snippet.objects.create(
                title = "title",
                code = "code",
                description = "description",
                created_by = self.user,
            )
        
    def test_should_user_expected_template(self):
        response = self.client.get("snippets/%s/" % self.snippet.id)
        self.assertTemplateUsed(response, "snippets/snippet_detail.html")

    def test_top_page_returns_200_and_expected_heading(self):
        response = self.client.get("/snippets/%s/" % self.snippet.id)
        self.assertContains(response, self.snippet.title, status_code = 200)

    def test_should_resolve_snippet_detail(self):
        found = resolve('/snippets/1/')
        self.assertEqual(snippet_detail, found.func)

class EditSnippetTest(TestCase):
    def test_should_resolve_snippet_edit(self):
        found = resolve('/snippets/1/edit/')
        self.assertEqual(snippet_edit, found.func)
