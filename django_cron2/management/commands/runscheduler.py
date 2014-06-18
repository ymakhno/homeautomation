from time import sleep
from django_cron2.management.commands import runcrons
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        command = runcrons.Command()
        while True:
            command.handle(force = False, silent = False)
            sleep(10)




