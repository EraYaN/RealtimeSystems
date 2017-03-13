import re
import collections

class TraceFile(object):
    """description of class"""
    def __init__(self, filename, **kwargs):
        self.trace = {}
        self.has_data = False
        self.data_re = re.compile('([0-9]+)\s?:\s?([0-9]+)')
        self.metadata_re = re.compile('([A-Za-z]+)\s?:\s?([^\s]+)')
        with open(filename,'r',encoding='utf-8',newline=None) as file:
            self.parse(file)
        return super().__init__(**kwargs)


    def parse(self, file):
        is_header = False
        is_data = False
        is_metadata = False
        current_trace = ''
        for line in file:
            if line == '':
                continue

            if line[0] == '#':
                current_trace = ''
                current_trace_count = ''
                continue

            match_md = self.metadata_re.search(line)
            if match_md:
                if match_md.group(1) == 'id':
                    current_trace = match_md.group(2)
                continue

            if current_trace != '':
                match_d = self.data_re.search(line)
                if match_d:
                    if current_trace not in self.trace:
                        self.trace[current_trace] = collections.OrderedDict()

                    timestamp = int(match_d.group(1))
                    value = int(match_d.group(2))

                    self.trace[current_trace][timestamp] = value

        if len(self.trace) > 0:
            self.has_data = True


    def get_high_period(self, signal, threshold=0):
        period = 0
        number_of_periods = 0
        last_was_high = False
        last_timestamp = 0
        last_value = 0
        if signal not in self.trace:
            raise ValueError('Signal is not in trace.')
        for timestamp, value in self.trace[signal].items():
            if value <= threshold and last_was_high:
                period += (timestamp - last_timestamp)
                number_of_periods+=1
            last_was_high = (value > threshold)
            last_value = value
            last_timestamp = timestamp


        return {'t':period,'n':number_of_periods}

    def find_risingedge_before(self, signal, original_timestamp, threshold=0):
        if signal not in self.trace:
            raise ValueError('Signal is not in trace.')

        first = -1
        first_value = False

        for timestamp, value in reversed(self.trace[signal].items()):
            if timestamp >= original_timestamp:
                continue

            if first == -1:
                first = timestamp
                first_value = (value > threshold)
            else:
                if first_value:
                    if not (value > threshold):
                        return first
                else:
                    if (value > threshold):
                        first = timestamp
                        first_value = (value > threshold)

        return first

    def find_risingedge_after(self, signal, original_timestamp, threshold=0):
        if signal not in self.trace:
            raise ValueError('Signal is not in trace.')

        first = -1
        first_value = False

        for timestamp, value in self.trace[signal].items():
            if timestamp <= original_timestamp:
                continue

            if first == -1:
                first = timestamp
                first_value = (value > threshold)
            else:
                if not first_value:
                    if (value > threshold):
                        return first
                else:
                    if not (value > threshold):
                        first = timestamp
                        first_value = (value > threshold)

        return first

    def get_event_latency(self, signal_event, signal_intr, signal_threshold=0, intr_threshold=0):

        if signal_event not in self.trace:
            raise ValueError('Event Signal is not in trace.')
        if signal_intr not in self.trace:
            raise ValueError('Interrupt Signal is not in trace.')

        delay = 0
        events_found = 0
        current_time = 0
        exit = False
        while True:
            timestamp = self.find_risingedge_after(signal_event,current_time)
            if timestamp > current_time:
                intr_timestamp = self.find_risingedge_before(signal_intr,timestamp,3)
                current_time = timestamp
            else:
                break
            delay += timestamp - intr_timestamp
            events_found += 1
            print("Found delay: {} ns".format(delay))


        return {'t':delay,'n':events_found}

