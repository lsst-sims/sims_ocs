.. _database-tables-targetproposalhistory:

=====================
TargetProposalHistory
=====================

This table records all of the proposals and proposal information for a given target.

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
      -  The value (need + bonus) of the target assigned by a particular proposal.
    * -  proposalNeed
      -  The need of the target assigned by a particular proposal.
    * -  proposalBonus
      -  The bonus of the target assigned by a particular proposal.
    * -  proposalBoost
      -  The time-balancing boost assigned by a particular proposal.
    * -  TargetHistory_targetId
      -  Numeric identifier that relates to an entry in the TargetHistory table.
