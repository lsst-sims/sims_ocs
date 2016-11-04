from sqlalchemy import select

from lsst.sims.ocs.database.tables import view

__all__ = ["create_summary_all_props"]

def create_summary_all_props(metadata, oh, sh, sfs, p, ph, f):
    """Create the SummaryAllProps view (table).

    Parameters
    ----------
    metadata : sqlalchemy.MetaData
        The database object that collects the tables.
    oh : sqlalchemy.Table
        The instance of the ObsHistory table.
    sh : sqlalchemy.Table
        The instance of the SlewHistory table.
    sfs : sqlalchemy.Table
        The instance of the SlewFinalState table.
    p : sqlalchemy.Table
        The instance of the Proposal table.
    ph : sqlalchemy.Table
        The instance of the ProposalHistory table.
    f : sqlalchemy.Table
        The instance of the Field table.
    Returns
    -------
    :class:`.view`
        The instance of the SummaryAllProps view.
    """

    summary_view = view("SummaryAllProps", metadata,
                        select([oh.c.observationId.label('observationId'),
                                oh.c.night.label('night'),
                                oh.c.observationStartTime.label('observationStartTime'),
                                oh.c.observationStartMJD.label('observationStartMJD'),
                                oh.c.observationStartLST.label('observationStartLST'),
                                oh.c.numExposures.label('numExposures'),
                                oh.c.visitTime.label('visitTime'),
                                oh.c.visitExposureTime.label('visitExposureTime'),
                                ph.c.Proposal_propId.label('proposalId'),
                                oh.c.Field_fieldId.label('fieldId'),
                                oh.c.ra.label('fieldRA'),
                                oh.c.dec.label('fieldDec'),
                                oh.c.altitude.label('altitude'),
                                oh.c.azimuth.label('azimuth'),
                                oh.c.filter.label('filter'),
                                oh.c.airmass.label('airmass'),
                                oh.c.skyBrightness.label('skyBrightness'),
                                oh.c.cloud.label('cloud'),
                                oh.c.seeingFwhm500.label('seeingFwhm500'),
                                oh.c.seeingFwhmGeom.label('seeingFwhmGeom'),
                                oh.c.seeingFwhmEff.label('seeingFwhmEff'),
                                sh.c.slewTime.label('slewTime'),
                                sh.c.slewDistance.label('slewDistance'),
                                sfs.c.paraAngle.label('paraAngle'),
                                sfs.c.rotTelPos.label('rotTelPos'),
                                sfs.c.rotSkyPos.label('rotSkyPos'),
                                oh.c.moonRA.label('moonRA'),
                                oh.c.moonDec.label('moonDec'),
                                oh.c.moonAlt.label('moonAlt'),
                                oh.c.moonAz.label('moonAz'),
                                oh.c.moonDistance.label('moonDistance'),
                                oh.c.moonPhase.label('moonPhase'),
                                oh.c.sunAlt.label('sunAlt'),
                                oh.c.sunAz.label('sunAz'),
                                oh.c.solarElong.label('solarElong')
                                ]).
                        where(oh.c.observationId == sh.c.ObsHistory_observationId).
                        where(sh.c.slewCount == sfs.c.SlewHistory_slewCount).
                        where(ph.c.ObsHistory_observationId == oh.c.observationId))

    return summary_view
