from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from .models import *

User = get_user_model()

# Create your tests here.
class BookmarksTests(TestCase):
    def setUp(self):
        # create user 1
        user_1 = User.objects.create_user(
            username='user_1',
            password='1234'
        )
        user_1.save()

        # create user 2
        user_2 = User.objects.create_user(
            username='user_2',
            password='1234'
        )
        user_2.save()

        # create test_bookmark 1
        bookmark_1 = Bookmark(
            title= "test",
            url= "www.test.com",
            private= False,
            owner=user_1
        )
        bookmark_1.save()

        # create test_bookmark 2
        bookmark_2 = Bookmark(
            title= "test2",
            url= "www.test2.com",
            private= True,
            owner= user_2
        )
        bookmark_2.save()

    # Helping functions ====================================
    def create_bookmark(self, data=None):
        if not data:
            data = {
                "title": "sebas_bookmark",
                "url": "www.depor.pe",
                "private": False,
                "owner": 1
            }
        url = reverse('api:bookmark-list')
        return self.client.post(url, data, format='json')  


    def view_bookmark(self):
        url = reverse('api:bookmark-list')
        return self.client.get(url, format='json')


    def retrieve_bookmark(self, pk=2):
        url = reverse('api:bookmark-detail', kwargs={'pk': pk})
        return self.client.get(url, format='json')


    def update_bookmark(self, data=None, pk=2):
        if not data:
            data = {
                "title": "sebas_bookmark_updated",
                "url": "www.depor_updated.pe"
            }
        url = reverse('api:bookmark-detail', kwargs={'pk':pk})
        return self.client.put(url, data, content_type='application/json')


    def delete_bookmark(self, pk=2):
        url = reverse('api:bookmark-detail', kwargs={'pk': pk})
        return self.client.delete(url, format='json')


    # Tests ====================================
    def test_create_bookmark(self):
        # anon: can't create as anon
        resp = self.create_bookmark()
        self.assertEqual(resp.status_code, 403)

        # user: can create
        self.client.login(username="user_1", password="1234")
        resp = self.create_bookmark()
        self.assertEqual(resp.status_code, 201)


    def test_view_bookmark(self):
        # anon: can view public // can't view private
        resp = self.view_bookmark()
        private_flag = False
        for item in resp.json():
            if item['private'] == True:
                private_flag = True
                break
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual(private_flag, False)

        # user: can view public / can't view other user's private bookmarks
        self.client.login(username="user_1", password="1234")
        resp = self.view_bookmark()
        public_flag = False
        for item in resp.json():
            if not item['private']:
                public_flag = True
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(public_flag, True)
        self.assertEqual(len(resp.json()), 1)

        # user: can view own private bookmark
        self.client.login(username="user_2", password="1234")
        resp = self.view_bookmark()
        private_flag = False
        for item in resp.json():
            if item['private'] == True and item['owner'] == 2:
                private_flag = True
                break
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(private_flag, True)


    def test_update_bookmark(self):
        # anon: can't update
        resp = self.update_bookmark()
        self.assertEqual(resp.status_code, 403)

        # user: can update own private bookmark
        self.client.login(username="user_2", password="1234")
        resp = self.update_bookmark({'title': 'new_title', 'url': 'new_url', 'private': True})
        resp2 = self.retrieve_bookmark(pk=2)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp2.json()['title'], 'new_title')

        # user: can't change the owner of the bookmark
        self.update_bookmark({'owner': 1})
        resp = self.retrieve_bookmark(pk=2)    
        self.assertEqual(resp.json()['owner'], 2)

        # user: can't update other user's private/public bookmarks
        self.client.login(username="user_1", password="1234")
        resp = self.update_bookmark({'title': 'new_title', 'url': 'new_url', 'private': True})
        self.assertEqual(resp.status_code, 404)


    def test_delete_bookmark(self):
        # anon: can't delete
        resp = self.delete_bookmark()
        self.assertEqual(resp.status_code, 403)

        # user: can delete own private bookmark
        self.client.login(username="user_1", password="1234")
        resp = self.delete_bookmark(pk=1)
        self.assertEqual(resp.status_code, 204)

        # user: can't delete other user's private/public bookmarks
        self.client.login(username="user_1", password="1234")
        resp = self.delete_bookmark(pk=2)
        self.assertEqual(resp.status_code, 404)