(function() {
	var captureListApp = angular.module('capture.controllers', ['ngCookies', 'angularMoment' ]);


	var client_states = Object.freeze({
		STATUS_UNKNOWN: {id: 0, text: "Unknown"},
		STATUS_CREATED: {id: 1, text: "Created"},
		STATUS_STARTING: {id: 2, text: "Starting"},
		STATUS_STARTED: {id: 3, text: "Started"},
		STATUS_STOPPING: {id: 4, text: "Stopping"},
		STATUS_STOPPED: {id: 5, text: "Stopped"}

	});



	/*
	 *
	 * capture controller
	 *
	 */
	captureListApp.controller('CaptureCtrl', 
		['$scope', '$rootScope', '$document', '$location', '$q',
		function($scope, $rootScope, $document, $location, $q) {


			//$scope.


	}]);



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
		}]);





	captureListApp.controller('jobListControl',
		['$scope', '$rootScope', '$document', '$cookies', '$sce', '$http', '$location', '$q', 'Job', 'Client', 
		function($scope, $rootScope, $document, $cookies, $sce, $http, $location,  $q, Job, Client) {

			$scope.syncJobs = function() {
				$scope.jobs = Job.query({active: "True"});	
			}

			$scope.isRunningJob = function(job) {
				//console.log('isRunningJob');
				//console.dir(job);
				return (job.status == client_states.STATUS_STARTING.id || job.status == client_states.STATUS_STARTED.id);
			}

			$scope.isStoppedJob = function(job) {
				return !(job.status == client_states.STATUS_STARTING.id || job.status == client_states.STATUS_STARTED.id);
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
				return (job.status == client_states.STATUS_STARTING.id || job.status == client_states.STATUS_STOPPING.id);
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
				//$location.path('/job/create/');
				console.log('creating');

				$rootScope.$broadcast('job:showCreateUI', 
					{ 
						title: 'Create Job',
						submitText: 'Create',
					});
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


	captureListApp.controller('JobCtrl', ['$scope', '$rootScope',
		function($scope, $rootScope) {

		$scope.archive = function(job) {
			console.log('archive!')
		}

		$scope.edit = function(job) {
			console.log('edit');

			$rootScope.$broadcast('job:showEditUI', 
				{ 
					title: 'Edit Job',
					submitText: 'Save',
					job: job
				});
		}

	}]);


	captureListApp.controller('jobFormController', ['$scope', '$rootScope', 'Job', 'Client',
		function($scope, $rootScope, Job, Client){

			$scope.init = function(e, data) {
				// grab a list of clients
				$scope.getClients();

				// update dialog fields
				$scope.updateDialogFields(data);

				$scope.$hidden_fields = [];

				if('job' in data) {
					$scope.job = data.job;
					$scope.$hidden_fields.push('status', 'assigned_worker');
					$scope.edit = true;
				} else {
					$scope.job = new Job({status: 2});
				}

			}

			$scope.updateDialogFields = function(data) {
				$scope.dlgParams = angular.extend({
						title: "",
						submitText: "Submit"
					}, data);

				$('#job-form-dlg .modal-title').text($scope.dlgParams.title);
				$('#job-form-dlg .job-create-dlg-submit').text($scope.dlgParams.submitText);
			}

			$scope.getClients = function() {
				$scope.clients = Client.query({}, $scope.showCreateDlg, $scope.onGetClientsFailed);
			}

			$scope.getClientsFailed = function(error) {
				$rootScope.toast.error("Couldn't get client list from server");
			}

			$scope.showCreateDlg = function(e, data) {
				var unassigned_clients = $scope.unassigned_clients();

				if(unassigned_clients.length > 0) {
					$scope.job.assigned_worker = unassigned_clients[0].id;
				} else {
					$scope.job.assigned_worker = null;
				}

				$('#job-form-dlg').modal('show');
			}

			$scope.isUnassigned = function(client) {
				return (client.active_jobs.length == 0);
			}

			$scope.unassigned_clients = function() {
				return $scope.clients.filter($scope.isUnassigned);
			}

			$scope.onSaveSuccessful = function() {
				$('#job-form-dlg').modal('hide');
			}

			$scope.onSaveFailed = function(error) {
				$rootScope.toast.error("Save failed: " + error)

				// step through all the errors and apply them to the properties
				angular.forEach(error.data, function(value,key) {

					// create errors dict
					$scope.job.$errors = error.data;

					/*
					if(!(key in $scope.job.$errors)) {
						$scope.job.$errors[key] = [];
					}*/

					// append error to the array
					//$scope.job.$errors[key] = value;


				});
			}

			$scope.submit = function() {
				if($scope.edit === true) {
					$scope.job.$update($scope.onSaveSuccessful, $scope.onSaveFailed);
				} else {
					$scope.job.$save($scope.onSaveSuccessful, $scope.onSaveFailed);
				}
				
			}


			$scope.client_states = client_states;

			$rootScope.$on('job:showCreateUI', $scope.init );
			$rootScope.$on('job:showEditUI', $scope.init );

	}]);


	captureListApp.controller('jobCreateController', ['$scope', '$rootScope', 
		function($scope, $rootScope){

		$scope.mode = 'create';
		$scope.title = 'Create a new Job';
		$scope.job = {};

	}]);



	captureListApp.controller('jobEditController', ['$scope', '$rootScope',
		function($scope, $rootScope){

		$scope.mode = 'edit';
		$scope.title = 'Edit a job';
		$scope.job = {name: "test"}

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

})();
