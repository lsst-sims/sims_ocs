.. _database-tables-field:

=====
Field
=====

This table contains all the coordinate information for the "visiting" fields. The field centers are determined from a tessellation (or tiling) of the celestial sphere which results in a closest-packed set of 5280 hexagons and 12 pentagons inscribed in circular fields having a 3.5-degree diameter (R. H. Hardin, N. J. A. Sloane and W. D. Smith, *Tables of spherical codes with icosahedral symmetry*, published electronically at http://NeilSloane.com/icosahedral.codes/).

.. list-table:: 
    :header-rows: 1

    * -  Column
      -  Description
    * -  fieldId
      -  Numeric identifier for the given field.
    * -  Session_sessionId
      -  The simulation run session Id.
    * -  fov
      -  The field of view of the field (units=degrees).
    * -  ra
      -  The Right Ascension of the field (units=degrees).
    * -  dec
      -  The Declination of the field (units=degrees).
    * -  gl
      -  The Galactic Longitude of the field (units=degrees).
    * -  gb
      -  The Galactic Latitude of the field (units=degrees).
    * -  el
      -  The Ecliptic Longitude of the field (units=degrees).
    * -  eb
      -  The Ecliptic Latitude of the field (units=degrees).
