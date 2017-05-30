import unittest

from sqlalchemy import MetaData

import lsst.sims.ocs.database.tables as tbls

import topic_helpers

class TablesTest(unittest.TestCase):

    def setUp(self):
        self.metadata = MetaData()

    def check_ordered_dict_to_table(self, ordered_dict, table):
        for column in table.c:
            self.assertTrue(column.name in ordered_dict, "{} not a key in ordered_dict".format(column.name))

    def test_create_session_table(self):
        session = tbls.create_session(self.metadata)
        self.assertEqual(len(session.c), 6)
        self.assertEqual(len(session.indexes), 1)
        self.assertTrue(session.c.sessionId.autoincrement)

    def test_create_session_table_without_autoincrement(self):
        session = tbls.create_session(self.metadata, False)
        self.assertEqual(len(session.c), 6)
        self.assertEqual(len(session.indexes), 1)
        self.assertFalse(session.c.sessionId.autoincrement)

    def test_create_target_history_table(self):
        targets = tbls.create_target_history(self.metadata)
        self.assertEqual(len(targets.c), 32)
        self.assertEqual(len(targets.indexes), 3)

    def test_write_target_history_table(self):
        target_topic = topic_helpers.target
        session_id = 1001

        result = tbls.write_target_history(target_topic, session_id)
        targets = tbls.create_target_history(self.metadata)
        self.check_ordered_dict_to_table(result, targets)
        self.assertEqual(result['Session_sessionId'], session_id)
        self.assertEqual(result['Field_fieldId'], target_topic.fieldId)
        self.assertEqual(result['groupId'], target_topic.groupId)
        self.assertEqual(result['filter'], target_topic.filter)
        self.assertEqual(result['dec'], target_topic.dec)
        self.assertEqual(result['requestedExpTime'], sum(target_topic.exposure_times))
        self.assertEqual(result['airmass'], target_topic.airmass)
        self.assertEqual(result['cloud'], target_topic.cloud)
        self.assertEqual(result['seeing'], target_topic.seeing)
        self.assertEqual(result['rank'], target_topic.rank)
        self.assertEqual(result['numRequestingProps'], target_topic.num_proposals)
        self.assertEqual(result['moonRA'], target_topic.moon_ra)
        self.assertEqual(result['moonAz'], target_topic.moon_az)
        self.assertEqual(result['cost'], target_topic.cost)

    def test_create_field_table(self):
        fields = tbls.create_field(self.metadata)
        self.assertEqual(len(fields.c), 9)
        self.assertEqual(len(fields.indexes), 4)

    def test_write_field_table(self):
        field_topic = topic_helpers.field_tuple

        result = tbls.write_field(field_topic, 1000)
        fields = tbls.create_field(self.metadata)
        self.check_ordered_dict_to_table(result, fields)
        self.assertEqual(result['fieldId'], field_topic[0])
        self.assertEqual(result['ra'], field_topic[2])
        self.assertEqual(result['gb'], field_topic[5])
        self.assertEqual(result['el'], field_topic[6])

    def test_create_observation_history_table(self):
        obs_hist = tbls.create_observation_history(self.metadata)
        self.assertEqual(len(obs_hist.c), 36)
        self.assertEqual(len(obs_hist.indexes), 4)

    def test_write_observation_history_table(self):
        obs_topic = topic_helpers.observation_topic
        session_id = 1001

        result = tbls.write_observation_history(obs_topic, session_id)
        obs_hist = tbls.create_observation_history(self.metadata)
        self.check_ordered_dict_to_table(result, obs_hist)
        self.assertEqual(result['Session_sessionId'], session_id)
        self.assertEqual(result['observationId'], obs_topic.observationId)
        self.assertEqual(result['observationStartTime'], obs_topic.observation_start_time)
        self.assertEqual(result['observationStartMJD'], obs_topic.observation_start_mjd)
        self.assertEqual(result['observationStartLST'], obs_topic.observation_start_lst)
        self.assertEqual(result['night'], obs_topic.night)
        self.assertEqual(result['TargetHistory_targetId'], obs_topic.targetId)
        self.assertEqual(result['Field_fieldId'], obs_topic.fieldId)
        self.assertEqual(result['groupId'], obs_topic.groupId)
        self.assertEqual(result['filter'], obs_topic.filter)
        self.assertEqual(result['dec'], obs_topic.dec)
        self.assertEqual(result['altitude'], obs_topic.altitude)
        self.assertEqual(result['visitTime'], obs_topic.visit_time)
        self.assertEqual(result['visitExposureTime'], sum(obs_topic.exposure_times))
        self.assertEqual(result['skyBrightness'], obs_topic.sky_brightness)
        self.assertEqual(result['cloud'], obs_topic.cloud)
        self.assertEqual(result['seeingFwhmGeom'], obs_topic.seeing_fwhm_geom)
        self.assertEqual(result['fiveSigmaDepth'], obs_topic.five_sigma_depth)
        self.assertEqual(result['moonRA'], obs_topic.moon_ra)
        self.assertEqual(result['moonAz'], obs_topic.moon_az)
        self.assertEqual(result['sunDec'], obs_topic.sun_dec)
        self.assertEqual(result['sunAlt'], obs_topic.sun_alt)
        self.assertEqual(result['solarElong'], obs_topic.solar_elong)

    def test_create_slew_history_table(self):
        slew_hist = tbls.create_slew_history(self.metadata)
        self.assertEqual(len(slew_hist.c), 7)
        self.assertEqual(len(slew_hist.indexes), 1)

    def test_write_slew_history_table(self):
        sh = topic_helpers.slew_history_coll
        result = tbls.write_slew_history(sh, 1000)
        slew_hist = tbls.create_slew_history(self.metadata)
        self.check_ordered_dict_to_table(result, slew_hist)
        self.assertEqual(result['slewCount'], sh.slewCount)
        self.assertEqual(result['startDate'], sh.startDate)
        self.assertEqual(result['endDate'], sh.endDate)
        self.assertEqual(result['slewTime'], sh.slewTime)
        self.assertEqual(result['slewDistance'], sh.slewDistance)
        self.assertEqual(result['ObsHistory_observationId'], sh.ObsHistory_observationId)
        self.assertEqual(result['Session_sessionId'], 1000)

    def test_create_slew_final_state_table(self):
        slew_state = tbls.create_slew_final_state(self.metadata)
        self.assertEqual(len(slew_state.c), 17)
        self.assertEqual(len(slew_state.indexes), 1)

    def test_write_slew_state_final_table(self):
        ss = topic_helpers.slew_state_coll
        result = tbls.write_slew_final_state(ss, 1000)
        self.assertEqual(result['slewStateId'], ss.slewStateId)
        self.assertEqual(result['slewStateDate'], ss.slewStateDate)
        self.assertEqual(result['SlewHistory_slewCount'], ss.SlewHistory_slewCount)

    def test_create_slew_initial_state_table(self):
        slew_state = tbls.create_slew_initial_state(self.metadata)
        self.assertEqual(len(slew_state.c), 17)
        self.assertEqual(len(slew_state.indexes), 1)

    def test_write_slew_state_initial_table(self):
        ss = topic_helpers.slew_state_coll
        result = tbls.write_slew_initial_state(ss, 1000)
        self.assertEqual(result['slewStateId'], ss.slewStateId)
        self.assertEqual(result['slewStateDate'], ss.slewStateDate)
        self.assertEqual(result['SlewHistory_slewCount'], ss.SlewHistory_slewCount)

    def test_create_target_exposures_table(self):
        exposure = tbls.create_target_exposures(self.metadata)
        self.assertEqual(len(exposure.c), 5)
        self.assertEqual(len(exposure.indexes), 2)

    def test_write_target_exposures_table(self):
        exposure = topic_helpers.exposure_coll1
        result = tbls.write_target_exposures(exposure, 1000)
        exposure_table = tbls.create_target_exposures(self.metadata)
        self.check_ordered_dict_to_table(result, exposure_table)
        self.assertEqual(result['exposureId'], exposure.exposureId)
        self.assertEqual(result['exposureNum'], exposure.exposureNum)
        self.assertEqual(result['exposureTime'], exposure.exposureTime)
        self.assertEqual(result['TargetHistory_targetId'], exposure.TargetHistory_targetId)

    def test_create_observation_exposures_table(self):
        exposure = tbls.create_observation_exposures(self.metadata)
        self.assertEqual(len(exposure.c), 6)
        self.assertEqual(len(exposure.indexes), 2)

    def test_write_observation_exposures_table(self):
        exposure = topic_helpers.exposure_coll3
        result = tbls.write_observation_exposures(exposure, 1000)
        exposure_table = tbls.create_observation_exposures(self.metadata)
        self.check_ordered_dict_to_table(result, exposure_table)
        self.assertEqual(result['exposureId'], exposure.exposureId)
        self.assertEqual(result['exposureNum'], exposure.exposureNum)
        self.assertEqual(result['exposureTime'], exposure.exposureTime)
        self.assertEqual(result['exposureStartTime'], exposure.exposureStartTime)
        self.assertEqual(result['ObsHistory_observationId'], exposure.ObsHistory_observationId)

    def test_create_slew_activities_table(self):
        slew_ac = tbls.create_slew_activities(self.metadata)
        self.assertEqual(len(slew_ac.c), 6)
        self.assertEqual(len(slew_ac.indexes), 1)

    def test_write_slew_activities_table(self):
        sa = topic_helpers.slew_activity_coll
        result = tbls.write_slew_activities(sa, 1000)
        slew_ac_table = tbls.create_slew_activities(self.metadata)
        self.check_ordered_dict_to_table(result, slew_ac_table)
        self.assertEqual(result['slewActivityId'], 1)
        self.assertEqual(result['Session_sessionId'], 1000)
        self.assertEqual(result['activityDelay'], sa.activityDelay)
        self.assertEqual(result['inCriticalPath'], sa.inCriticalPath)
        self.assertEqual(result['SlewHistory_slewCount'], sa.SlewHistory_slewCount)

    def test_create_slew_maxspeeds_table(self):
        slew_ms = tbls.create_slew_maxspeeds(self.metadata)
        self.assertEqual(len(slew_ms.c), 8)
        self.assertEqual(len(slew_ms.indexes), 1)

    def test_write_slew_maxspeeds_table(self):
        sm = topic_helpers.slew_maxspeed_coll
        result = tbls.write_slew_maxspeeds(sm, 1000)
        slew_ms_table = tbls.create_slew_maxspeeds(self.metadata)
        self.check_ordered_dict_to_table(result, slew_ms_table)
        self.assertEqual(result['slewMaxSpeedId'], 1)
        self.assertEqual(result['Session_sessionId'], 1000)
        self.assertEqual(result['domeAzSpeed'], sm.domeAzSpeed)
        self.assertEqual(result['telAltSpeed'], sm.telAltSpeed)
        self.assertEqual(result['SlewHistory_slewCount'], sm.SlewHistory_slewCount)

    def test_create_scheduled_downtime_table(self):
        sched_down = tbls.create_scheduled_downtime(self.metadata)
        self.assertEqual(len(sched_down.c), 4)
        self.assertEqual(len(sched_down.indexes), 1)

    def test_write_scheduled_downtime_table(self):
        sd = (45, 7, "general maintanence")
        result = tbls.write_scheduled_downtime(sd, 1000)
        sched_down = tbls.create_scheduled_downtime(self.metadata)
        self.check_ordered_dict_to_table(result, sched_down)
        self.assertEqual(result['night'], sd[0])
        self.assertEqual(result['Session_sessionId'], 1000)
        self.assertEqual(result['duration'], sd[1])
        self.assertEqual(result['activity'], sd[2])

    def test_create_unscheduled_downtime_table(self):
        unsched_down = tbls.create_unscheduled_downtime(self.metadata)
        self.assertEqual(len(unsched_down.c), 4)
        self.assertEqual(len(unsched_down.indexes), 1)

    def test_write_unscheduled_downtime_table(self):
        usd = (20, 3, "intermediate event")
        result = tbls.write_unscheduled_downtime(usd, 1000)
        unsched_down = tbls.create_unscheduled_downtime(self.metadata)
        self.check_ordered_dict_to_table(result, unsched_down)
        self.assertEqual(result['night'], usd[0])
        self.assertEqual(result['Session_sessionId'], 1000)
        self.assertEqual(result['duration'], usd[1])
        self.assertEqual(result['activity'], usd[2])

    def test_create_proposal_table(self):
        props = tbls.create_proposal(self.metadata)
        self.assertEqual(len(props.c), 4)
        self.assertEqual(len(props.indexes), 1)

    def test_write_proposal_table(self):
        pinfo = topic_helpers.prop_info
        result = tbls.write_proposal(pinfo, 1000)
        prop_info = tbls.create_proposal(self.metadata)
        self.check_ordered_dict_to_table(result, prop_info)
        self.assertEqual(result['propId'], pinfo[0])
        self.assertEqual(result['propName'], pinfo[1])
        self.assertEqual(result['propType'], pinfo[2])
        self.assertEqual(result['Session_sessionId'], 1000)

    def test_create_observation_proposal_history_table(self):
        prop_hist = tbls.create_observation_proposal_history(self.metadata)
        self.assertEqual(len(prop_hist.c), 8)
        self.assertEqual(len(prop_hist.indexes), 1)

    def test_write_observation_proposal_history_table(self):
        phist = topic_helpers.obs_prop_hist
        result = tbls.write_observation_proposal_history(phist, 1001)
        prop_hist = tbls.create_observation_proposal_history(self.metadata)
        self.check_ordered_dict_to_table(result, prop_hist)
        self.assertEqual(result['propHistId'], phist[0])
        self.assertEqual(result['Proposal_propId'], phist[1])
        self.assertEqual(result['proposalValue'], phist[2])
        self.assertEqual(result['proposalNeed'], phist[3])
        self.assertEqual(result['proposalBonus'], phist[4])
        self.assertEqual(result['proposalBoost'], phist[5])
        self.assertEqual(result['ObsHistory_observationId'], phist[6])
        self.assertEqual(result['Session_sessionId'], 1001)

    def test_create_target_proposal_history_table(self):
        prop_hist = tbls.create_target_proposal_history(self.metadata)
        self.assertEqual(len(prop_hist.c), 8)
        self.assertEqual(len(prop_hist.indexes), 1)

    def test_write_target_proposal_history_table(self):
        phist = topic_helpers.target_prop_hist
        result = tbls.write_target_proposal_history(phist, 1001)
        prop_hist = tbls.create_target_proposal_history(self.metadata)
        self.check_ordered_dict_to_table(result, prop_hist)
        self.assertEqual(result['propHistId'], phist[0])
        self.assertEqual(result['Proposal_propId'], phist[1])
        self.assertEqual(result['proposalValue'], phist[2])
        self.assertEqual(result['proposalNeed'], phist[3])
        self.assertEqual(result['proposalBonus'], phist[4])
        self.assertEqual(result['proposalBoost'], phist[5])
        self.assertEqual(result['TargetHistory_targetId'], phist[6])
        self.assertEqual(result['Session_sessionId'], 1001)

    def test_create_config_table(self):
        cnf = tbls.create_config(self.metadata)
        self.assertEqual(len(cnf.c), 4)
        self.assertEqual(len(cnf.indexes), 1)

    def test_write_config_table(self):
        cnt = topic_helpers.config_tuple
        result = tbls.write_config(cnt, 1002)
        cnf = tbls.create_config(self.metadata)
        self.check_ordered_dict_to_table(result, cnf)
        self.assertEqual(result['configId'], cnt[0])
        self.assertEqual(result['Session_sessionId'], 1002)
        self.assertEqual(result['paramName'], cnt[1])
        self.assertEqual(result['paramValue'], cnt[2])

    def test_summary_all_props_table(self):
        oh = tbls.create_observation_history(self.metadata)
        sh = tbls.create_slew_history(self.metadata)
        sfs = tbls.create_slew_final_state(self.metadata)
        ph = tbls.create_observation_proposal_history(self.metadata)
        p = tbls.create_proposal(self.metadata)
        f = tbls.create_field(self.metadata)
        summary = tbls.create_summary_all_props(self.metadata, oh, sh, sfs, p, ph, f)
        self.assertEqual(len(summary.c), 36)

    def test_create_proposal_field_table(self):
        fields = tbls.create_proposal_field(self.metadata)
        self.assertEqual(len(fields.c), 4)
        self.assertEqual(len(fields.indexes), 3)

    def test_write_proposal_field_table(self):
        field_topic = topic_helpers.field_tuple

        result = tbls.write_proposal_field(field_topic, 1000)
        fields = tbls.create_proposal_field(self.metadata)
        self.check_ordered_dict_to_table(result, fields)
        self.assertEqual(result['fieldId'], field_topic[0])
        self.assertEqual(result['ra'], field_topic[2])
        self.assertEqual(result['gb'], field_topic[5])
        self.assertEqual(result['el'], field_topic[6])
