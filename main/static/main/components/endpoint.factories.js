(function() {

	/*
	 * CaptureFactory
	 *
	 *
	 */

	function CaptureFactory(Job, Update) {
		var self = {};


		function getJobById(id) {
			for(var i = 0; i < self.jobs.length; i++) {
				if(self.jobs[i].id == id) {
					return i;
				}
			}
			return -1;
		}

		self.getJobs = function() {
			return Job.query();
		}

		self.getActiveJobs = function() {
			return Job.query({active: true});
		}

		self.getArchives = function() {
			return Job.query({active: false});
		}


		self.get = function(id) {
			var obj = Job.get({id:id}, null, null, function(error){
				console.error("Couldn't get Job: " + error);
				console.dir(error);
			});

			return obj;
		}


		self.archive = function(job) {

			job.archived_date = new Date();
			job.$update(function(){
				var id = getJobById(job.id);

				if(id >= 0) {
					self.jobs = self.jobs.splice(id,1);
				}
			}, function(error) {
				console.error("error archiving: " + error);
				console.dir(error);
			});
		}

		return self;
	}

	CaptureFactory.$inject = ['Job', 'Update'];


	/*
	 * ClientFactory
	 *
	 *
	 */

	function ClientFactory(Client) {
		var self = this, 
			f = {};

		f.getClients = function() {
			return Client.query();
		}

		f.get = function(id) {
			return Client.get({id:id});
		}

		f.create = function(params) {
			var c = new Client(params);
			return c.$save();
		}

		f.delete = function(id) {
			return Client.delete({id:id});
		}

		f.update = function(params) {
			return Client.update(params);
		}


		return f;
	}
	ClientFactory.$inject = ['Client'];


	/*
	 *
	 * JobModificationFactory
	 *
	 */

	 function JobModificationFactory(JobModification) {
	 	var self = this,
	 		f = {};


	 	f.getJobModifications = function(jobId) {
	 		return JobModification.query({job: jobId});
	 	}

	 	f.get = function(id) {
	 		return JobModification.get({id:id});
	 	}
	 }




	angular.module('endpoint.factories', ['main.services'])
		.factory('CaptureFactory', CaptureFactory)
		.factory('ClientFactory', ClientFactory)
		.factory('JobModificationFactory', JobModificationFactory);





})();