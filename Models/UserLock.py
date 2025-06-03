class UserLock:
    def __init__(self, enroll_id, week_zone, group, start_time, end_time):
        self.enroll_id = enroll_id
        self.week_zone = week_zone
        self.group = group
        self.start_time = start_time
        self.end_time = end_time

    @property
    def enroll_id(self):
        return self._enroll_id

    @enroll_id.setter
    def enroll_id(self, enroll_id):
        self._enroll_id = enroll_id

    @property
    def week_zone(self):
        return self._week_zone

    @week_zone.setter
    def week_zone(self, week_zone):
        self._week_zone = week_zone

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, group):
        self._group = group

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        self._end_time = end_time
