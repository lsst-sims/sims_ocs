import math

__all__ = ["Field"]

class Field(object):
    """Class for handling field information.

    This is the class for handling the field information on the sky. The values contained
    within the class are all kept in degrees. Properties are exposed that present those
    values in radians.

    Attributes
    ----------
    fid : int
        The field's ID.
    fov : float
        The field's field-of-view.
    ra : float
        The field's right ascension.
    dec : float
        The field's declination.
    gl : float
        The field's galactic latitude.
    gb : float
        The field's galactic longitude.
    el : float
        The field's ecliptic latitude.
    eb : float
        The field's ecliptic longitude.
    """

    def __init__(self, fid, fov, ra, dec, gl, gb, el, eb):
        """Initialize the class.

        Note
        ----
            All angular values are expected to be in degrees!

        Parameters
        ----------
        fid : int
            The field's ID.
        fov : float
            The field's field-of-view.
        ra : float
            The field's right ascension.
        dec : float
            The field's declination.
        gl : float
            The field's galactic latitude.
        gb : float
            The field's galactic longitude.
        el : float
            The field's ecliptic latitude.
        eb : float
            The field's ecliptic longitude.
        """
        self.fid = fid
        self.fov = fov
        self.ra = ra
        self.dec = dec
        self.gl = gl
        self.gb = gb
        self.el = el
        self.eb = eb

    def __str__(self):
        """str
        """
        return "Field ID: {0}, FOV: {1:.3f} deg, RA: {2:.3f} deg, DEC: {3:.3f} deg, GalL: {4:.3f} deg, "\
               "GalB: {5:.3f} deg, EclL: {6:.3f} deg, EclB: {7:.3f} deg".format(self.fid, self.fov, self.ra,
                                                                                self.dec, self.gl, self.gb,
                                                                                self.el, self.eb)

    def __repr__(self):
        """str
        """
        return "Field({!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r})".format(self.fid, self.fov, self.ra,
                                                                              self.dec, self.gl, self.gb,
                                                                              self.el, self.eb)

    @classmethod
    def from_topic(cls, topic):
        """Alternate initializer.

        Parameters
        ----------
        topic : SALPY_scheduler.fieldC
            The field topic instance.

        Returns
        -------
        field.Field
        """
        return cls(topic.ID, topic.fov, topic.ra, topic.dec, topic.gl, topic.gb, topic.el, topic.eb)

    @property
    def fov_rad(self):
        """float: Field-of-view in radians.
        """
        return math.radians(self.fov)

    @property
    def ra_rad(self):
        """float: Right ascension in radians.
        """
        return math.radians(self.ra)

    @property
    def dec_rad(self):
        """float: Declination in radians.
        """
        return math.radians(self.dec)

    @property
    def gl_rad(self):
        """float: Galactic latitude in radians.
        """
        return math.radians(self.gl)

    @property
    def gb_rad(self):
        """float: Galactic longitude in radians.
        """
        return math.radians(self.gb)

    @property
    def el_rad(self):
        """float: Ecliptic latitude in radians.
        """
        return math.radians(self.el)

    @property
    def eb_rad(self):
        """float: Ecliptic longitude in radians.
        """
        return math.radians(self.eb)
