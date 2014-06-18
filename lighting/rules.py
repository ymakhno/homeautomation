from datetime import datetime, timedelta
import json
import random
from threading import Thread
from time import sleep
from urllib.parse import urlencode
from django_cron2 import CronJobBase, Schedule
from lighting.models import Rule
from lighting.pool import get_pool
from lighting.zwave import ChangeLightLevel

class RunRule(Thread):
    def __init__(self, rule, run_end):
        super().__init__(daemon=True, name="RunRule %d" % rule.id)
        self._rule = rule
        self._run_end = run_end

    def run(self):
        delta = self._rule.end_delta if self._run_end else self._rule.start_delta
        sleep(random.randint(0, delta * 60))
        ChangeLightLevel(self._rule.lighter, 0 if self._run_end else 255).do()


class RulesChecker(CronJobBase):
    schedule = Schedule(run_every_secs = 30)
    code = "rules.checker"

    def do(self):
        now = datetime.now()
        print("Starting rules job: ", now)
        start = now.time().replace(second=0, microsecond=0)
        end = (now + timedelta(seconds = 60)).time().replace(second=0, microsecond=0)
        rules = Rule.objects.filter(start__gte = start, start__lt = end)
        for rule in rules:
            if rule.check_day(now, False):
                print("Light on: ", rule)
                RunRule(rule, False).start()

        rules = Rule.objects.filter(end__gte = start, end__lt = end)
        for rule in rules:
            if rule.check_day(now, True):
                print("Light off: ", rule)
                RunRule(rule, True).start()

class SendSMSWithIP(CronJobBase):
    schedule = Schedule(run_every_secs=432000)
    code = "send.ip"

    def do(self):
        print("Sending SMS with current ip")
        r = get_pool().request('GET', 'http://ip-api.com/json')
        try:
            ip = json.loads(r.data.decode('utf-8'))["query"]
            params = {'version' : 'http', 'login' : '380502921842', 'password' : '112111',
                      'command' : 'send', 'from' : 'raspberry', 'to' : '380502921842', 'message' : ip}
            url = "http://smsukraine.com.ua/api/http.php?%s" % urlencode(params)
            r.close()

            r = get_pool().request('GET', url)
            r.read()
        finally:
            r.close()
