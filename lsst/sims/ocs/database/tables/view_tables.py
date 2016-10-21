from sqlalchemy import select

from lsst.sims.ocs.database.tables import view

__all__ = ["create_summary"]

def create_summary(metadata, oh, sh, sfs, p, ph):

    # pid_select = select([ph.c.Proposal_propId]).where(oh.c.observationId == ph.c.ObsHistory_observationId)

    summary_view = view("Summary", metadata,
                        select([oh.c.observationId.label('observationId'),
                                oh.c.night.label('night'),
                                ph.c.Proposal_propId.label('proposalId'),
                                oh.c.observationStartMJD.label('observationStartMJD'),
                                sh.c.slewTime.label('slewTime'),
                                sh.c.slewDistance.label('slewDistance'),
                                sfs.c.paraAngle.label('paraAngle'),
                                sfs.c.rotTelPos.label('rotTelPos'),
                                sfs.c.rotSkyPos.label('rotSkyPos')]).
                        where(oh.c.observationId == sh.c.ObsHistory_observationId).
                        where(sh.c.slewCount == sfs.c.SlewHistory_slewCount).
                        where(ph.c.ObsHistory_observationId == oh.c.observationId))
                        # where(ph.c.Proposal_propId == pid_select))

    return summary_view
