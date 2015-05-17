from config.settings import common

from django.db import models
from app_main import models

class Topic(models.Model):
	subtopic = models.ForeignKey(Topic)


class Project(models.Model):
	thread = models.ForeignKey(Thread)
	topics = models.ManyToManyField(Topic, verbose_name="list of topics", through='TopicWeight', through_fields=('project', 'topic'))
	voters = ManyToManyField(common.AUTH_USER_MODEL, through='ProjectVote', through_fields=('user', 'project'))

	def pollResults():
		return

class TopicWeight(models.Model):
	project = models.ForeignKey(Project)
	topic = models.ForeignKey(Topic)
	weight = models.PositiveIntegerField()

	def save(self, *args, **kwargs):
		self.validateWeith()
		return super(TopicWeight, self).save(*args, **kwargs)

	def validateWeith():
		# validate the weight according the topics in the project
		# save many

class Vote(models.Model)
	user = models.ForeignKey(common.AUTH_USER_MODEL)
	weight = models.PositiveIntegerField()
	agree = models.BooleanField()

	class Meta:
        abstract = True

class ProjectVote(Vote):
	project = models.ForeignKey(Project)

	def save(self, *args, **kwargs):
		self.weight = self.calculateWeith();
		self.updateFollowing()
		return super(Vote, self).save(*args, **kwargs)


	def updateFollowing():
		# Call user to get following and update Projects with 
		# saveAll

	def calculateWeith():
		# Call users to get followers and calculate price
		# based on topic of the Project
		# Take into account the votes 


class CommentVote(Vote):
	comment = models.ForeignKey(Project)




