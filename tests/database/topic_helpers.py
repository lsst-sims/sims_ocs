#import collections

import SALPY_scheduler
import lsst.sims.ocs.observatory

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

observation_topic = SALPY_scheduler.scheduler_observationTestC()
observation_topic.observationID = 5
observation_topic.targetID = 10
observation_topic.observationTime = 1640995200.0
observation_topic.fieldId = 300
observation_topic.filter = "r"
observation_topic.ra = 1.000
observation_topic.dec = -3.00
observation_topic.angle = 0.5
observation_topic.num_exposures = 2

slew_history_coll = lsst.sims.ocs.observatory.SlewHistory(slewCount=1, startDate=2922, endDate=2925,
                                                          slewTime=6.0, slewDistance=1.0,
                                                          ObsHistory_observationID=1)
