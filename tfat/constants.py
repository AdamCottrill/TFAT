'''=============================================================
c:/1work/Python/djcode/tfat/tfat/constants.py
Created: 27 May 2015 09:03:24


DESCRIPTION:

this file contain the look-ups used by various models in tfat
application.  Most of these were derived directly form fishnet data
dictionary.

A. Cottrill
=============================================================

'''


REPORTING_CHOICES = {
    ('verbal', 'verbal'),
    ('e-mail', 'e-mail'),
    ('letter', 'letter'),
    ('other', 'other'),
}


SEX_CHOICES = {
    ('1', 'Male'),
    ('2', 'Female'),
    ('3', 'Hermaphrodite'),
    ('9', 'Unknown')
}


TAG_TYPE_CHOICES = {
    ('0', 'No tag'),
    ('1', 'Streamer'),
    ('2', 'Tubular Vinyl'),
    ('3', 'Circular Strap Jaw '),
    ('4', 'Butt End Jaw '),
    ('5', 'Anchor'),
    ('6', 'Coded Wire'),
    ('7', 'Strip Vinyl  '),
    ('8', 'Secure Tie'),
    ('9', 'Type Unknown or not applicable'),
    ('A', 'Internal (Radio)'),
    ('X', 'Tag Scar/obvious loss'),
}

TAG_POSITION_CHOICES = {
    ('1', 'Anterior Dorsal'),
    ('2', 'Between Dorsal'),
    ('3', 'Posterior Dorsal'),
    ('4', 'Abdominal Insertion'),
    ('5', 'Flesh of Back'),
    ('6', 'Jaw'),
    ('7', 'Snout'),
    ('8', 'Anal'),
    ('9', 'Unknown')
}


TAG_ORIGIN_CHOICES = {
    ('01', 'Ontario Ministry of Natural Resources'),
    ('02', 'New York State'),
    ('03', 'State of Michigan'),
    ('04', 'University of Guelph'),
    ('05', 'University of Toronto'),
    ('06', 'State of Ohio'),
    ('07', 'State of Pennsylvania'),
    ('08', 'Royal Ontario Museum'),
    ('09', 'State of Minnesota'),
    ('10', 'Lakehead University'),
    ('11', 'Sir Sandford Fleming College'),
    ('12', 'Private Club'),
    ('13', 'Ontario Hydro'),
    ('19', 'Other'),
    ('99', 'Unknown')
}

TAG_COLOUR_CHOICES = {
    ('1', 'Colourless'),
    ('2', 'Yellow'),
    ('3', 'Red'),
    ('4', 'Green'),
    ('5', 'Orange'),
    ('6', 'Other'),
    ('9', 'Unknown')
}

TAGSTAT_CHOICES = {
    ('C', 'Existed on Capture'),
    ('A', 'Applied'),
}


FATE_CHOICES = {
    ('R', 'Released'),
    ('K', 'Killed'),
}

DATE_FLAG_CHOICES = {
    (0, 'Unknown'),
    (1, 'Reported'),
    (2, 'Derived'),
}

LATLON_FLAG_CHOICES = {
    (0, 'Unknown'),
    (1, 'Reported'),
    (2, 'Derived'), #from grid
}

PROVINCES_STATE_CHOICES = [
    ('ON', 'Ontario'),
    ('AB', 'Alberta'),
    ('BC', 'British Columbia'),
    ('MB', 'Manitoba'),
    ('NB', 'New Brunswick'),
    ('NL', 'Newfoundland and Labrador'),
    ('NS', 'Nova Scotia'),
    ('NT', 'Northwest Territories'),
    ('NU', 'Nunavut'),
    ('PE', 'Prince Edward Island'),
    ('QC', 'Quebec'),
    ('SK', 'Saskatchewan'),
    ('YT', 'Yukon'),
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
]
