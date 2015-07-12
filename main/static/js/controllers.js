var captureListApp = angular.module('capture.controllers', ['ngCookies', 'angularMoment' ]);









/*
 *
 * toast controller
 *
 */
captureListApp.controller('toastController', 
	['$scope', '$rootScope', '$document', '$cookies', '$sce', '$http', '$location', '$q',
	function($scope, $rootScope, $document, $cookies, $sce, $http, $location,  $q) {
		$scope.next_id = 0;
		$scope.toasts = [];

		//$scope.on
		$rootScope.$on('toast:create', function(event, data) {
			console.log("alert");
			console.dir(event);
			console.dir(data);
			var id = ($scope.next_id++);
			$scope.toasts.push({id: id, level: data[0], text: data[1] });
		});

		$scope.dismiss = function(id) {
			var idx = $scope.toasts.map(function(d) { return d.id; }).indexOf(id);
			console.log('dismiss: ' + id + ' - ' + idx);

			if(idx >= 0) {
				$scope.toasts.splice(idx, 1);	
			} else {
				console.error('bad id : '+ id );
			}
			
		}
	}])

captureListApp.controller('jobListControl',
	['$scope', '$rootScope', '$document', '$cookies', '$sce', '$http', '$location', '$q', 'Job', 'Client', 
	function($scope, $rootScope, $document, $cookies, $sce, $http, $location,  $q, Job, Client) {
		var client_states = Object.freeze({
			STATUS_UNKNOWN: 0,
			STATUS_CREATED: 1,
			STATUS_STARTING: 2,
			STATUS_STARTED: 3,
			STATUS_STOPPING: 4,
			STATUS_STOPPED: 5
		});

		var client_state_names = Object.freeze({
			0: "Unknown",
			1: "Created",
			2: "Starting",
			3: "Started",
			4: "Stopping",
			5: "Stopped",
		})



		$scope.syncJobs = function() {
			$scope.jobs = Job.query({active: "True"});	
		}

		$scope.isRunningJob = function(job) {
			//console.log('isRunningJob');
			//console.dir(job);
			return (job.status == client_states.STATUS_STARTING || job.status == client_states.STATUS_STARTED);
		}

		$scope.isStoppedJob = function(job) {
			return !(job.status == client_states.STATUS_STARTING || job.status == client_states.STATUS_STARTED);
		}


		$scope.runningJobs = function(jobs) {
			//console.log('runningJobs');
			//console.dir(jobs);
			var result = jobs.filter($scope.isRunningJob);
			return result;
		}

		$scope.stoppedJobs = function(jobs) {
			//console.log('stoppedJobs');
			//console.dir(jobs);
			return jobs.filter($scope.isStoppedJob)
		}

		$scope.isWorking = function(job) {
			//console.log('isWorking')
			//console.dir(job)
			return (job.status == client_states.STATUS_STARTING || job.status == client_states.STATUS_STOPPING);
		}


		$scope.onActionClicked = function(job, newStatus) {
			var oldStatus = job.status;
			console.log('action clicked (job:' + job.id + ' , status:' + job.status + " -> " + newStatus + ')');

			// find index of job
			//var idx = $scope.jobs.map(function(d) { return d.id; }).indexOf(id);

			// sync job
			job.$get({}, 
				function(data) {
					// verify we're in sync
					if(job.status === oldStatus) {
						job.status = newStatus;
						job.$update(function(obj) {
							// success
						}, function(error) {
							// revert status visually and report error
							$rootScope.toast.error("Couldn't set job");
							job.status = oldStatus;
						});
					} else {
						$rootScope.toast.warn("Job was out of sync with the server. (old status: " + oldStatus + ", new status: " + newStatus + ")")
					}
				},
				function(data) {
					console.log("scope.jobs got error: " + data);
				});

		}

		$scope.create = function() {
			$location.path('/job/create/');
			console.log('creating')
		}


		/*
		 *
		 * initialization
		 *
		 */


		$scope.jobs = null;
		$scope.syncJobs();

		$q.all([$scope.jobs.$promise])
			.then(function(data){
				console.dir(data[0]);

				if(data[0].data != null && data[0].data.results) {
					$scope.jobs = data[0].data.results;
				}

				//$scope.apply();
				//$scope.$broadcast("data:loaded");
			});


}]);


captureListApp.controller('JobController', ['$scope', '$rootScope',
	function($scope, $rootScope) {


}]);


captureListApp.controller('jobFormController', ['$scope', '$rootScope', 
	function($scope, $rootScope){


}]);

captureListApp.controller('jobCreateController', ['$scope', '$rootScope', 
	function($scope, $rootScope){

	$scope.mode = 'create';
	$scope.title = 'Create a new Job';
	$scope.job = {};

	$scope.activate = function(data) {
		console.log("jobCreateController - Active");
	}

}]);

captureListApp.controller('jobEditController', ['$scope', '$rootScope',
	function($scope, $rootScope){

	$scope.mode = 'edit';
	$scope.title = 'Edit a job';
	$scope.job = {name: "test"}


	$scope.activate = function(data) {
		console.log("jobEditController - Active");
	}
}]);


captureListApp.controller('clientListController', ['$scope', '$rootScope', 'Client',
	function($scope, $rootScope, Client) {

		$scope.unassignedClients = function(clients) {
		}


		$scope.syncClients = function() {
			$scope.clients = Client.query();
		}

		/*
		 *
		 * initialization
		 *
		 */

		 $scope.clients = null;
		 $scope.syncClients();


}]);


