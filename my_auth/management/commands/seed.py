import random

from django.core.files import File
from django.core.management.base import BaseCommand

from my_auth.models import MyUser
from news.models import Article, Category, Comment


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('clearing database...')
        clear_data()
        self.stdout.write('seeding users...')
        seed_users()
        self.stdout.write('seeding categories...')
        seed_categories()
        self.stdout.write('seeding articles...')
        seed_articles()
        self.stdout.write('done!')


def clear_data():
    MyUser.objects.exclude(is_staff=True).delete()
    Article.objects.all().delete()
    Category.objects.all().delete()


def seed_users():
    with open('../first_names.txt', 'r') as first_names,\
            open('../last_names.txt', 'r') as last_names:
        for i in range(1, 11):  # 2001
            email = 'user{:04d}@m.ru'.format(i)
            first_name = first_names.readline()
            last_name = last_names.readline()
            user = MyUser.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.set_unusable_password()
            user.save()


def seed_categories():
    names = [
        'politics',
        'sport',
        'nature',
        'art',
        'culture',
        'information technologies',
        'animals',
        'gender studies',
        'science',
        'space'
    ]
    for n in names:
        category = Category.objects.create(name=n)
        category.save()


lorem_ipsum = [
    'lorem',
    'ipsum',
    'dolor',
    'sit',
    'amet',
    'consectetur',
    'adipiscing',
    'elit',
    'aliquam',
    'sagittis'
]


def seed_articles():
    authors = MyUser.objects.all()
    categories = Category.objects.all()
    with open('../russian.txt', 'r', encoding='cp1251') as file:
        for i in range(21):  # 300000
            title = ''
            text = ''
            for title_lines in range(5):
                title += file.readline()[:-1] + ' '
            for text_lines in range(20):
                text += file.readline()[:-1] + ' '
            if i % 19 == 0:
                title += random.choice(lorem_ipsum)
                text += random.choice(lorem_ipsum)

            article_categories_amount = random.randint(0, 3)
            article_categories = random.sample(list(categories), article_categories_amount)

            article = Article.objects.create(
                title=title,
                text=text,
                likes=random.randint(0, 5000),
                author=random.choice(authors)
            )
            article.categories.set(article_categories)

            if article_categories_amount % 2 == 0:
                article.image.save('3.jpeg', File(open('../3.jpeg', 'rb')))

            article_comments_amount = random.randint(0, 10)  # 100
            seed_article_comments(article, article_comments_amount, file, authors)


def seed_article_comments(article, comments_amount, file, authors):
    if comments_amount == 0:
        return
    else:
        for comment in range(comments_amount):
            text = ''
            for text_lines in range(10):
                text += file.readline()[:-1] + ' '
            comment = Comment.objects.create(
                author=random.choice(authors),
                article=article,
                text=text,
                likes=random.randint(0, 100)
            )
