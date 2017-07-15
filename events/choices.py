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
    ('any', 'Any'),
)


APPLICATION_STATUS = (
    ('applied', 'Applied'),
    ('wl', 'WL')
)


ALLOCATION_STATUS = (
    #('applied', 'Applied'),
    #('selected', 'Selected'),
    ('shortlisted', 'Shortlisted'),
    ('rejected', 'Rejected'),
    ('positions-full', 'Position Full'),
    ('backup', 'Backup'),
    ('working', 'Working',),
    ('backed-out', 'Backed out'),
    ('completed', 'Completed'),
)
