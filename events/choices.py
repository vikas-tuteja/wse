CANDIDATE_TYPE = (
    ('promotor','Promotor'),
    ('hostess', 'Hostess'),
    ('emcee', 'Emcee'),
    ('anchor','Anchor'),
    ('model','Model'),
    ('actor', 'Actor'),
    ('mascot', 'Mascot'),
    ('biker', 'Biker'),
    ('lookwalkers', 'Lookwalkers'),
    ('other','Other'),
)


GENDER = (
    ('m', 'Male'),
    ('f', 'Female'),
    ('a', 'Any')
)


EVENT_STATUS = (
    ('pending', 'Pending'),
    ('in-progress', 'In-progress'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
)


CANDIDATE_CLASS = (
    ('A+', 'A+'),
    ('A', 'A'),
    ('B', 'B'),
)


CONFIRMATION_STATUS = (
    ('applied', 'Applid'),
    ('wl', 'WL')
)


ALLOCATION_STATUS = (
    ('applied', 'Applied'),
    ('shortlisted', 'Shortlisted'),
    ('rejected', 'Rejected'),
    ('selected', 'Selected'),
    ('backup', 'Backup'),
    ('working', 'Working',),
    ('backed-out', 'Backed out')
)
