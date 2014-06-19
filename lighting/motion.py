from datetime import datetime
from io import BytesIO
import json
import os
from threading import Thread
from time import sleep
from PIL import Image, ImageMath, ImageOps
from PIL.ImageFilter import MedianFilter
from django_cron2 import CronJobBase, Schedule
from lighting.models import WebCamera
from lighting.pool import get_pool
from urllib.parse import urlencode

class MotionDetection(Thread):
    def __init__(self, camera):
        super().__init__(name = "Motion Detection %d" % camera.id, daemon=True)
        self._camera = camera
        self._previous = None

    def run(self):
        while True:
            try:
                camera = WebCamera.objects.get(pk = self._camera.id)
                if camera.motion_control:
                    now = datetime.now()
                    request = get_pool().request("GET", "%s?action=snapshot" % camera.url)
                    try:
                        source = Image.open(BytesIO(request.data))
                        img = ImageOps.equalize(ImageOps.grayscale(source))
                        if self._previous is not None:
                            out = ImageMath.eval("convert(a - b, 'L')", a = img, b = self._previous)
                            out = out.filter(MedianFilter())
                            total = 0
                            for idx, val in enumerate(out.histogram()):
                                total += val * idx
                            if total > 3000000:
                                camera.last_motion = now
                                camera.save()

                                filename = os.path.join(camera.motion_folder, "{:%Y%m%d-%H%M%S}.jpg".format(now))
                                source.save(filename)

                        self._previous = img
                    finally:
                        request.close()
                else:
                    self._previous = None
            except:
                print("Ignore Exception")
            sleep(1)

    @classmethod
    def start_motion_detection(cls):
        for camera in WebCamera.objects.all():
            MotionDetection(camera).start()

class SendSMSWithMotions(CronJobBase):
    schedule = Schedule(run_every_secs=21600)
    code = "send.motions"

    def do(self):
        print("Sending SMS with current ip")
        r = get_pool().request('GET', 'http://ip-api.com/json')
        try:
            ip = json.loads(r.data.decode('utf-8'))["query"]
            text = "ip: %s;" % ip
            for camera in WebCamera.objects.all():
                text += "{name}: {motion:%d-%H%M%S};".format(name = camera.name, motion = camera.last_motion)

            params = {'version' : 'http', 'login' : '380502921842', 'password' : '112111',
                      'command' : 'send', 'from' : 'raspberry', 'to' : '380502921842', 'message' : text}
            url = "http://smsukraine.com.ua/api/http.php?%s" % urlencode(params)
            r.close()

            r = get_pool().request('GET', url)
            r.read()
        finally:
            r.close()


#from lighting.motion import MotionDetection
#from lighting.models import WebCamera
#MotionDetection(WebCamera.objects.first()).run()