#!/bin/python
from django.core.management.base import BaseCommand, CommandError
from main.models import Job, Update
from datetime import datetime, timedelta
import random
import pytz
import math


class Command(BaseCommand):
	help = 'Adds some fake updates to the specified job'

	def add_arguments(self, parser):
		parser.add_argument('job', help='name of job to add updates to')
		parser.add_argument('delta', type=int, help='number of seconds difference between updates' )
		parser.add_argument('num', type=int, help='number of entries to generate')
		parser.add_argument('--initial_rate', type=float, help='starting rate')
		parser.add_argument('--max', type=int, help='maximum number to generate', default=50)
		parser.add_argument('--truncate', action="store_true", help="truncate all previous updates first")

	def handle(self, *args, **options):
		try:
			job = Job.objects.filter(name=options['job']).get()
		except Job.DoesNotExist:
			raise CommandError('Job "%s" does not exist' % options['job'])


		if options['truncate']:
			Update.objects.filter(job=job).delete()

		now = datetime.now()
		total_delta = timedelta(seconds=(options['num'] * options['delta']))
		delta = timedelta(seconds=options['delta'])
		start = now - total_delta

		start = start.replace(microsecond=0, tzinfo=pytz.utc)

		curtime = start
		last = options['initial_rate'] if options['initial_rate'] is not None else 0
		limit = options['max']
		total_count = 0
		range_val = max(1,math.floor((limit * .05) + 1))
		self.stdout.write("...%f"%(range_val))
		while curtime < datetime.now().replace(tzinfo=pytz.utc):
			curtime = curtime + delta
			min_val = max(0, last-range_val)
			max_val = min(limit, last + range_val)
			val = random.uniform(min_val, max_val)
			count = val * delta.total_seconds()
			total_count += count
			self.stdout.write("Writing for '%s'... %f [%d,%d]" %(curtime, val, min_val, max_val))

			last = val

			update = Update.objects.create(job=job, total_count=total_count, count=count, rate=val)
			update.save()
			update.date = curtime
			update.save()
		