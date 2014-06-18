from datetime import datetime
import json
from time import time
import re
from django_cron2 import CronJobBase, Schedule
from lighting.models import ZWaveApi, Lighter
from lighting.pool import get_pool


class ChangeLightLevel:
    def __init__(self, light, value):
        super().__init__()
        self.__light = light
        if light.internal_dimmer():
            value = min(value, 99)
        self.__value = value


    def do(self):
        z_wave = ZWaveApi.objects.first()
        command_url = "{z_wave}/Run/{device}.{command}.Set({value})".format(
            z_wave = z_wave.url,
            device = self.__light.access_name,
            command = ("SwitchMultilevel" if self.__light.internal_dimmer() else "SwitchBinary"),
            value = self.__value
        )
        request = get_pool().request('GET', command_url)
        try:
            request.read()
        finally:
            request.close()


class UpdateZWaveStatus(CronJobBase):
    schedule = Schedule(run_every_secs = 20)
    code = "z-wave.update"

    def do(self):
            print("Updating ZWave status: ", datetime.now())
            z_wave = ZWaveApi.objects.first()
            lighters = Lighter.objects.all()
            request_time = int(time() * 10)
            data_url = "{z_wave}/Data/{time}".format(z_wave = z_wave.url, time = "{time}")

            request = get_pool().request('GET', data_url.format(time = request_time))
            try:
                request_time = json.loads(request.data.decode('utf-8'))["updateTime"]
            finally:
                request.close()

            for lighter in lighters:
                url = "{z_wave}/Run/{device}.{command}.Get()".format(z_wave = z_wave.url,
                                                                     device = lighter.access_name,
                                                                     command=("SwitchMultilevel" if lighter.internal_dimmer() else "SwitchBinary"))
                request = get_pool().request('GET', url)
                try:
                    request.read()
                finally:
                    request.close()
            request = get_pool().request('GET', data_url.format(time = request_time))
            try:
                state = json.loads(request.data.decode('utf-8'))
                for lighter in lighters:
                    device_name = re.sub(r'\[|\]\.?', r'.', lighter.access_name)
                    command_node = "{device}commandClasses.{command}.data.level".format(device = device_name,
                                                                                        command = 38 if lighter.internal_dimmer() else 37
                    )
                    if state[command_node]:
                        if lighter.is_dimmer():
                            lighter.value = int(state[command_node]["value"])
                        else:
                            lighter.value = 255 if state[command_node]["value"] else 0

                        lighter.save()
            finally:
                request.close()
