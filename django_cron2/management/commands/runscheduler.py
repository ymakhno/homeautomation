from time import sleep
from django_cron2.management.commands import runcrons
from django.core.management.base import BaseCommand
from lighting.motion import MotionDetection


class Command(BaseCommand):
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        MotionDetection.start_motion_detection()
        command = runcrons.Command()
        while True:
            command.handle(force = False, silent = False)
            sleep(10)




