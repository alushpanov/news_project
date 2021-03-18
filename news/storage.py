def path_file_name(instance, filename):
    return 'articles/user_{0}/{1}'.format(instance.author.uuid, filename)
