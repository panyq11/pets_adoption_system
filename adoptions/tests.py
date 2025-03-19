# adoptions/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from posts.models import Pet, PetImage, PostPetInfo
from adoptions.models import AdoptPetInfo, AdoptionReview

User = get_user_model()


class AdoptionViewsTest(TestCase):
    def setUp(self):
        # Create a normal user and an admin user
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        self.operator = User.objects.create_user(username='operator', password='operatorpass',
                                                 email='operator@example.com', user_type='Admin')

        # Create a test pet record
        self.pet = Pet.objects.create(
            name='Buddy',
            sex='Male',
            age='Young',  # 年龄为 'Young' 或 'Adult'
            weight=15.0,
            breed='Golden Retriever',
            size='Large',
            status='Available',
            posted_by=self.operator,

            type='Dog'
        )

        # Create a test PostPetInfo record for the pet_detail view to display pet posting information
        self.post_pet_info = PostPetInfo.objects.create(
            pet=self.pet,
            user=self.user,
            email=self.user.email,
            home_type='Apartment',
            home_ownership='Own',
            has_other_pets='None',
            has_children='0',
            experience_with_pets='I have raised pets before.',
            reason_for_fostering='I love animals.',
            pet_passport='Available',
            vaccinated='Yes',
            status='Pending'
        )

        # Create an AdoptPetInfo record as a submitted adoption application
        self.adopt_pet_info = AdoptPetInfo.objects.create(
            pet=self.pet,
            user=self.user,
            operator=self.operator,
            home_type='Apartment',
            home_ownership='Own',
            has_landlord_permission=True,
            has_other_pets='None',
            has_children='0',
            experience_with_pets='I have experience with pets.',
            reason_for_adoption='I want to adopt this pet.',
            pet_passport='Available'
        )

        # Creates an AdoptionReview record with a default status of Pending
        self.adoption_review = AdoptionReview.objects.create(
            pet=self.pet,
            adopter_username=self.user,
            operator_username=self.operator,
            status='Pending'
        )

        self.client = Client()
        self.client.login(username='testuser', password='testpass')

    def test_available_pets_view(self):
        """
        Test that the available_pets view returns status code 200 and the correct list of pets
        """
        url = reverse('adoptions:available_pets')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.pet, response.context['pets'])

    def test_pet_detail_view(self):
        """Testing that the pet_detail view returns the correct pet and release information"""
        url = reverse('adoptions:pet_detail', kwargs={'pet_id': self.pet.pet_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['pet'], self.pet)
        self.assertEqual(response.context['pet_info'], self.post_pet_info)
        self.assertIn('images', response.context)

    def test_apply_for_adoption_get(self):
        """测试 apply_for_adoption 视图 GET 请求返回表单"""
        url = reverse('adoptions:apply_for_adoption', kwargs={'pet_id': self.pet.pet_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIn('pet', response.context)

    def test_apply_for_adoption_post_no_existing_application(self):
        """测试当没有未处理申请时，POST 提交成功创建新的申请记录"""
        # 首先删除所有当前用户的 Pending AdoptionReview 记录
        AdoptionReview.objects.filter(adopter_username__username=self.user.username, status='Pending').delete()
        url = reverse('adoptions:apply_for_adoption', kwargs={'pet_id': self.pet.pet_id})
        data = {
            'home_type': 'Apartment',
            'home_ownership': 'Own',
            'has_landlord_permission': True,
            'has_other_pets': 'None',
            'has_children': '0',
            'experience_with_pets': 'I have experience with pets.',
            'reason_for_adoption': 'I want to adopt this pet.',
            'pet_passport': 'Available',
        }
        response = self.client.post(url, data)
        # 检查是否重定向到 my_application
        self.assertEqual(response.status_code, 302)
        # 检查是否创建了新的 AdoptPetInfo 记录
        self.assertTrue(AdoptPetInfo.objects.filter(pet=self.pet, user=self.user).exists())
        # 检查是否创建了新的 AdoptionReview 记录
        self.assertTrue(AdoptionReview.objects.filter(pet=self.pet, adopter_username=self.user).exists())

    def test_apply_for_adoption_post_existing_application(self):
        """测试当已有未处理申请时，POST 不允许提交新申请"""
        # 确保已有 Pending 状态的 AdoptionReview 记录
        AdoptionReview.objects.create(
            pet=self.pet,
            adopter_username=self.user,
            operator_username=self.operator,
            status='Pending'
        )
        url = reverse('adoptions:apply_for_adoption', kwargs={'pet_id': self.pet.pet_id})
        data = {
            'home_type': 'Apartment',
            'home_ownership': 'Own',
            'has_landlord_permission': True,
            'has_other_pets': 'None',
            'has_children': '0',
            'experience_with_pets': 'I have experience with pets.',
            'reason_for_adoption': 'I want to adopt this pet.',
            'pet_passport': 'Available',
        }
        response = self.client.post(url, data)
        # 预期重定向到 my_application
        self.assertEqual(response.status_code, 302)
        # 检查是否未创建新的 AdoptPetInfo（假设只允许一个 Pending 记录）
        count = AdoptPetInfo.objects.filter(pet=self.pet, user=self.user).count()
        self.assertEqual(count, 1)

    def test_my_application_view(self):
        """测试 my_application 视图返回正确上下文数据"""
        url = reverse('adoptions:my_application')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # 假设视图中返回的 context 包含 'review' 和 'application'
        self.assertIn('review', response.context)
        self.assertIn('application', response.context)

    def test_adoption_history_view(self):
        """测试 adoption_history 视图返回当前用户的所有审核记录"""
        url = reverse('adoptions:adoption_history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        history_list = response.context['history_list']
        self.assertIn(self.adoption_review, history_list)

    def test_history_details_view(self):
        """测试 history_details 视图返回正确的申请和审核详情"""
        url = reverse('adoptions:history_details', kwargs={'pet_id': self.pet.pet_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # 验证 context 中的 application 和 review 对象与数据库中对应记录一致
        expected_application = AdoptPetInfo.objects.get(pet__pet_id=self.pet.pet_id)
        expected_review = AdoptionReview.objects.get(pet__pet_id=self.pet.pet_id)
        self.assertEqual(response.context['application'], expected_application)
        self.assertEqual(response.context['review'], expected_review)
