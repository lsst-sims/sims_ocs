#import collections

import SALPY_scheduler

target = SALPY_scheduler.scheduler_targetTestC()
target.targetId = 10
target.fieldId = 300
target.filter = "r"
target.ra = 1.000
target.dec = -3.00
target.angle = 0.5
target.num_exposures = 2

field_topic = SALPY_scheduler.scheduler_fieldC()
field_topic.ID = 1
field_topic.fov = 0.5
field_topic.ra = 30.0
field_topic.dec = -30.0
field_topic.gl = -45.0
field_topic.gb = 45.0
field_topic.el = 60.0
field_topic.eb = -60.0
