from datetime import datetime
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main_app.settings")
django.setup()

import www.tasks as tasks

#f = open('/var/log/chalaoshi/tasks.log','a')
#try:    
print('%s: start chalaoshi tasks.' % datetime.now())

#tasks.cal_rate()
#print('%s: cal_rate finished.\n' % datetime.now())
tasks.cal_hot()
print('%s: cal_hot finished.' % datetime.now())
tasks.clear_rank_cache()
print('%s: cleared cache' % datetime.now())
#finally:
#    f.close()
