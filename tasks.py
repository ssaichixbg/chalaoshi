import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main_app.settings")
django.setup()

import www.tasks as tasks

tasks.cal_rate()
tasks.cal_hot()
tasks.clear_rank_cache()
