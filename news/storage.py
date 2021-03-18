def article_image_path(instance, filename):
    return 'articles/user_{0}/{1}'.format(instance.author.uuid, filename)
