import random

from django.core.files import File
from django.core.management.base import BaseCommand

from my_auth.models import MyUser
from news.models import Article, Category, Comment


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('seeding users...')
        seed_users()
        self.stdout.write('seeding categories...')
        seed_categories()
        self.stdout.write('seeding articles...')
        seed_articles()
        self.stdout.write('done!')


def seed_users():
    with open('../first_names.txt', 'r') as first_names, \
            open('../last_names.txt', 'r') as last_names:
        for i in range(2000):
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


authors = MyUser.objects.exclude(is_staff=True)


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
        Category.objects.create(name=n)


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
    with open('../russian.txt', 'r', encoding='cp1251') as file:
        bulk_articles = []
        for i in range(3000):
            title = ''
            text = ''
            for title_lines in range(5):
                title += file.readline()[:-1] + ' '
            for text_lines in range(20):
                text += file.readline()[:-1] + ' '
            if i % 19 == 0:
                title += random.choice(lorem_ipsum)
                text += random.choice(lorem_ipsum)
            article = Article(
                title=title,
                text=text,
                likes=random.randint(0, 5000),
                views=random.randint(0, 2000),
                author=random.choice(authors)
            )
            bulk_articles.append(article)
        Article.objects.bulk_create(bulk_articles)
        seed_categories_images_comments(file)
        finish_comments_seeding()


def seed_categories_images_comments(file):
    articles = list(Article.objects.all())
    categories = list(Category.objects.all())
    bulk_comments = []
    for article in articles:
        article_categories_amount = random.randint(0, 3)
        article_categories = random.sample(categories, article_categories_amount)
        article.categories.set(article_categories)

        if article_categories_amount % 2 == 0:
            article.image.save('3.jpeg', File(open('../3.jpeg', 'rb')))

        for comment in range(random.randint(0, 100)):
            text = ''
            for text_lines in range(10):
                text += file.readline()[:-1] + ' '
            comment = Comment(
                author=random.choice(authors),
                article=article,
                text=text,
                likes=random.randint(0, 100)
            )
            bulk_comments.append(comment)
    Comment.objects.bulk_create(bulk_comments)


def finish_comments_seeding():
    spaces = '          '
    empty_comments = list(Comment.objects.filter(
        text=spaces
    ))  # 10 spaces means that comment's text is empty. The reason is the way of constructing comment texts.
    while empty_comments:
        with open('../russian.txt', 'r', encoding='cp1251') as file:
            for comment in empty_comments:
                text = ''
                for text_lines in range(10):
                    text += file.readline()[:-1] + ' '
                comment.text = text
        Comment.objects.bulk_update(empty_comments, ['text'])
        empty_comments = list(Comment.objects.filter(text=spaces))
