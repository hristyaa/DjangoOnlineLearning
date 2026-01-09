from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(name="Test Course")
        self.lesson = Lesson.objects.create(
            name="Test lesson",
            description="Test lesson",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_get(self):
        """Тестирование детального просмотра урока"""
        url = reverse("materials:lesson_get", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        """Тестирование создания урока"""
        url = reverse("materials:lesson_create")
        data = {"name": "Test2 Lesson", "video_url": "https://youtube.com/video"}
        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_update_patch(self):
        """Тестирование редактирования урока"""
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {"name": "Test2 Lesson"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Test2 Lesson")
        self.assertEqual(Lesson.objects.count(), 1)

    def test_lesson_delete(self):
        """Тестирование удаления урока"""
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_list(self):
        """Тестирование просмотра списка уроков"""
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        data = response.json()
        print(data)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_url": None,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "image": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubmissionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(name="Test Course")
        self.client.force_authenticate(user=self.user)

    def test_subscriprion_add(self):
        """Тестирование добавления подписки на курс"""
        url = reverse("materials:subscription")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course))

    def test_subscriprion_delete(self):
        """Тестирование удаления подписки"""
        Subscription.objects.create(user=self.user, course=self.course)
        url = reverse("materials:subscription")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course)
        )
