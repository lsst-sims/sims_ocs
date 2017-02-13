.. _database-tables-obsproposalhistory:

==================
ObsProposalHistory
==================

This table records all of the proposals and proposal information for a given observation.

.. list-table:: 
    :header-rows: 1

    * -  Column
      -  Description
    * -  propHistId
      -  The numeric identifier for the particular proposal history entry.
    * -  Session_sessionId
      -  The simulation run session Id.
    * -  Proposal_propId
      -  Numeric identifier that relates to an entry in the Proposal table.
    * -  proposalValue
      -  The value (need + bonus) of the observation assigned by a particular proposal.
    * -  proposalNeed
      -  The need of the observation assigned by a particular proposal.
    * -  proposalBonus
      -  The bonus of the observation assigned by a particular proposal.
    * -  proposalBoost
      -  The time-balancing boost assigned by a particular proposal.
    * -  ObsHistory_observationId
      -  Numeric identifier that relates to an entry in the ObsHistory table.
