from datetime import datetime
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main_app.settings")
django.setup()

import www.tasks as tasks

f = open('/var/log/chalaoshi/tasks.log','a')
try:
    tasks.cal_rate()
    f.write('%s: cal_rate finished.\n' % datetime.now())
    tasks.cal_hot()
    f.write('%s: cal_hot finished.\n' % datetime.now())
    tasks.clear_rank_cache()
    f.write('%s: cleared cache\n' % datetime.now())
finally:
    f.close()
