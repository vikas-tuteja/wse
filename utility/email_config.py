email_data = {
    'client': {
        'welcome': {
            'html': '<div style="font-family:Roboto;">\
                    Dear %(username)s,<br>\
                    <br>\
                    Thank You for registering with WorkSmart Events. We extend you a warm welcome from the WSE community.<br>\
                    <br>\
                    Your login credentials are as follows - <br>\
                    Username - %(username)s<br>\
                    Password - %(password)s<br>\
                    <br>\
                    WorkSmart Events is a platform that bridges the gap between event organizers and resources required for the events.<br>\
                    As an esteemed client you have an opportunity to post a requirement and we will provide you with the screened candidates to make the event a success (<a href="http://www.worksmartevents.com/termsandconditions">T&C Apply</a>)<br>\
                    Someone from our team would get back to you in the next 24 hours to understand your requirements better before posting them on the website.<br>\
                    You may start posting your requirements at - http://www.worksmartevents.com/post-events/<br>\
                    You may update your profile from - http://www.worksmartevents.com/my-profile/profile/<br><br>\
                    In case of any queries please get in touch with us at +91-702-111-5997 (8AM - 9PM) or email us at worksmartevent@gmail.com<br>\
                    <br>\
                    Regards, <br>\
                    WorkSmart Events Team<br>\
                    </div>',
            'subject': 'Welcome to Worksmart Events',
            'bcc_address': '',
            'plain_text': ''
        },
        'post_event': {
            'html': '<div style="font-family:Roboto;">\
                    Dear %(username)s,><br><br>\
                    Thank You for posting an event on WorkSmart Events, your event has been posted successfully.<br>\
                    You may view / promote the same using the following url - %(eventurl)s<br>\
                    However, it is still under verification. Our team would get back to you in the next 24 hours to understand your requirements better.<br>\
                    <br>\
                    Discalimer: We may disallow to publish an event on our website on the basis of any negative content.<br><br>\
                    Regards, <br>\
                    WorkSmart Events Team<br>\
                    </div>',
            'subject': 'Congratulations! Event Posted Successfully.',
            'bcc_address': '',
            'plain_text': ''
        }
    },

    'candidate': {
        'welcome': {
            'html': '<div style="font-family:Roboto;">\
                    Dear %(username)s,<br>\
                    <br>\
                    Thank You for registering with WorkSmart Events. We extend you a warm welcome from the WSE community <br>\
                    <br>\
                    Your login credentials are as follows - <br>\
                    Username - %(username)s<br>\
                    Password - %(password)s<br>\
                    <br>\
                    WorkSmart Events is a platform that bridges the gap between event organizers and resources required for the events.<br>\
                    As an esteemed candidate you have an opportunity to engage and work with big brands for short/long durations and get handsomely paid for your contribution. (<a href="http://www.worksmartevents.com/termsandconditions">T&C Apply</a>)<br>\
                    Someone from our team would get back to you in the next 24 hours to verify your details.<br>\
                    You may start applying for events by visiting - http://www.worksmartevents.com/events/<br>\
                    You may update your profile from - http://www.worksmartevents.com/my-profile/profile/<br><br>\
                    In case of any queries please get in touch with us +91-702-111-5997 (8AM - 9PM) or email us at worksmartevent@gmail.com<br>\
                    <br>\
                    Regards, <br>\
                    WorkSmart Events Team<br>\
                    </div>',
            'subject': 'Welcome to Worksmart Events',
            'bcc_address': '',
            'plain_text': ''
        },
        'apply_event': {
            'html': '<div style="font-family:Roboto"><br>\
                    Dear %(username)s,<br><br>\
                    Thank You for applying for an event on WorkSmart Events.<br>\
                    Link to the event detail - %(eventurl)s <br><br>\
                    We will get back in touch with you at your mobile number, if you are shortlisted.<br>\
                    We will keep you posted on any changes in the event schedule<br><br>\
                    Regards, <br>\
                    WorkSmart Events Team<br>\
                    </div>',
            'subject': 'Congratulations! Applied for event successfully',
            'bcc_address': '',
            'plain_text': ''
        }
    }
}
