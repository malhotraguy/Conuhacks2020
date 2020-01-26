# Donate Time

We built a server in Flask that serves the user a webapp, including a login page and a form that helps us determine which volunteering opportunities are the best for each user. The information is passed to a NoSQL Firebase instance, and the user is prompted to log in and give our system access (via OAuth 2.0) to their Google Calendar. With that access, we can extract their daily schedule, and in comparison with a schedule of charity/volunteering opportunities, we identify potential (one hour) blocks of time in which the user might donate their time. It is at this point that the users are served a personally-tailored list of volunteering opportunities to choose from. When they choose a volunteering opportunity, we use the Zendesk API to connect them with charity representatives and other volunteers through their preferred form of messaging. We also update both employees' and coordinators' calendars to reflect the new commitments.
