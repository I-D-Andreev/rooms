# rooms


Admin Name: for_testing
Admin Pass: admin161720


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'OPTIONS': {
    #         'read_default_file': os.path.join(BASE_DIR, 'database.cnf')
    #     }
    # }
}

or use branch "use_sqlite3"