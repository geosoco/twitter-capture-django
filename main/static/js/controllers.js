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


			$scope.$on("job:archived", function(e,data){
				if('id' in data) {
					var idx = $scope.jobs.map(function(d) { return d.id; }).indexOf(data.id);
					if(idx >= 0) {
						$scope.jobs.splice(idx,1);
					} else {
						$rootScope.toast.error("Couldn't find archived job with id: " + data.id);
					}
				} else {
					$rootScope.toast.error("Couldn't remove archived job - no id");
					console.dir(data);
				}
				
			});

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

		$scope.onSaveFailed = function(data) {
			console.dir(data);
			$rootScope.toast.error("Failed to archive job: " + data.status + " " + data.statusText );
		}

		$scope.onSaveSucceeded = function(data) {
			console.log("job archived");
			$rootScope.$broadcast("job:archived",{id: data.id});
		}

		$scope.archive = function(job) {
			job.archived_date = new Date();
			job.$update($scope.onSaveSucceeded, $scope.onSaveFailed);
		}

		$scope.edit = function(job) {
			

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

				// reset data
				$scope.$hidden_fields = [];
				$scope.$errors = [];
				$scope.job.$errors = {};
				$scope.initial = null;
				$scope.edit = false;
				$scope.job = null;


				// if the message contained a job, we're editing
				if('job' in data) {
					$scope.job = data.job;
					// make a backup
					$scope.initial = angular.copy($scope.job);
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
				//return (client.active_jobs.length == 0 || client.active_jobs.);
				var assigned_count = 0;
				if('id' in $scope.job) {
					for(var i = 0; i < client.active_jobs.length; i++) {
						if(client.active_jobs[i].id !== $scope.job.id) {
							assigned_count += 1;
						}
					}
				} 

				return (assigned_count === 0);
			}

			$scope.unassigned_clients = function() {
				return $scope.clients.filter($scope.isUnassigned);
			}

			$scope.onSaveSuccessful = function() {
				$('#job-form-dlg').modal('hide');
			}

			$scope.onSaveFailed = function(error) {

				$scope.job.$errors = {};
				$scope.$errors = [];

				// toast an error if there's no reasonable feedback
				if(!('data' in error)) {
					var saveFailedMsg = "Failed to save job: " + + error.status + " " + error.statusText;
					$rootScope.toast.error(saveFailedMsg);
					$scope.job.$errors["request"] = saveFailedMsg;
					$scope.$errors = saveFailedMsg;
				} else {
					$scope.job.$errors = error.data;

					// step through all the errors and apply them to the properties
					angular.forEach(error.data, function(value,key) {

						// create errors dict
						

						/*
						if(!(key in $scope.job.$errors)) {
							$scope.job.$errors[key] = [];
						}*/

						// append error to the array
						//$scope.job.$errors[key] = value;

						angular.forEach(value, function(errText, idx){
							var msg = "";

							if(key == "non_field_errors") {
								msg = errText;
							} else {
								msg = key + ": " + errText;
							}

							$scope.$errors.push(msg);

						});

					});
				}
			}

			$scope.submit = function() {
				if($scope.edit === true) {
					$scope.job.$update($scope.onSaveSuccessful, $scope.onSaveFailed);
				} else {
					$scope.job.$save($scope.onSaveSuccessful, $scope.onSaveFailed);
				}
				
			}

			$scope.onClose = function() {

			}

			$scope.onCancel = function(e) {
				if('initial' in $scope) {
					angular.copy($scope.initial, $scope.job);	
				}
				$('#job-form-dlg').modal('hide');
			}


			$scope.client_states = client_states;

			$rootScope.$on('job:showCreateUI', $scope.init );
			$rootScope.$on('job:showEditUI', $scope.init );
			$rootScope.$on('job:cancelUI', $scope.onCancel );

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


		$scope.onCancel = function(e) {
			$rootScope.$broadcast("job:cancelUI", {})
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

})();
