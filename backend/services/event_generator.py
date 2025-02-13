from ics import Calendar, Event


def create_ics_file(event) -> Calendar.serialize:
    event_dates = event.generate_valid_dates()
    calendar = Calendar()
    for event_date in event_dates:
        events = Event()
        events.name = event.name
        events.begin = event_date.strftime("%Y-%m-%d")
        events.make_all_day()
        calendar.events.add(events)
    return calendar.serialize()
