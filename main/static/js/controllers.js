var captureListApp = angular.module('captureListApp', ['ngCookies', 'angularMoment', 'ngResource']);

/*
// for a fixed header at the tope
captureListApp.run(['$anchorScroll', function($anchorScroll) {
	$anchorScroll.yOffset = 60;	// always scroll by an extra 60 pixels
}]);
*/

captureListApp.run(['$http', '$cookies', '$rootScope', function($http, $cookies, $rootScope) {
	//$http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
	//$http.defaults.headers.put['X-CSRFToken'] = $cookies['csrftoken'];

	var toast = function(level, msg ) {
		$rootScope.$emit('toast:create', [level, msg] )
	}

	$rootScope.toast = {
		toast: toast,
		error: function(msg) { console.error(msg); toast('danger', msg); },
		warn: function(msg) { console.warn(msg); toast('warning', msg); },
		info: function(msg) { console.info(msg); toast('info', msg); },
		success: function(msg) { console.info("success: " + msg); toast('success', msg); }
	} 
}]);


captureListApp.config(['$resourceProvider', '$httpProvider', function($resourceProvider, $httpProvider) {
	$resourceProvider.defaults.stripTrailingSlashes = false;

	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
}]);

//
//
//
//
//

captureListApp.factory("Job", function($resource){
	return $resource(
		"/api/jobs/:id/\/.json", 
		{id: "@id"}, 
		{
			query: { 
				method: 'GET',
				transformResponse: function(data) { 
					var results = angular.fromJson(data);
					return results.results;  
				},
				isArray: true
			},
			update: { method: 'PUT'}
		});
});



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
	['$scope', '$rootScope', '$document', '$cookies', '$sce', '$http', '$location', '$q', 'Job',
	function($scope, $rootScope, $document, $cookies, $sce, $http, $location,  $q, Job) {
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

			/*
			var newJobObj = Job.get({id: oldJob.id}, 
				function(data) {
					console.log("Got job " + newJobObj.id + " successfully");
					console.dir(newJobObj);
					if(newJobObj.status === oldJob.status) {
						newJobObj.status = newStatus;
						newJobObj.$update(function(obj) {
							$scope.syncJobs();
						}, function(error) {
							$rootScope.toast.error("failed to save job (" + oldJob.name + ") : " + error.status + " " + error.statusText )
							//$scope.$emit('alert:create', ['error', 'failed to save job #' + oldJob.id ]);
							//$rootScope.$emit('alert:create', ['danger', "failed to get job #" + oldJob.id ] );
						});
					} else {
						// error
						console.error("OUT OF SYNC")
					}
				},
				function(data) {
					var msg = "failed to get job #" + oldJob.id ;
					console.error(msg);
					$rootScope.emit('alert:create', ['error', "failed to get job #" + oldJob.id ] )
				});
			*/
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


captureListApp.controller('editJobController', ['$scope', '$rootScope', function($scope, $rootScope){

}]);