(function() {

	var services = angular.module('capture.services', ['ngResource']);

	/*
	 * basic service
	 */
	var basicService = {
				query: { 
					method: 'GET',
					transformResponse: transformGetResponse,
					isArray: true
				},
				update: { method: 'PATCH'},
				delete: { method: 'DELETE'},
				save: { method: 'POST'},
				get: { method: 'GET'}
			};


	/*
	 *
	 * common function for transforming results
	 * 
	 */
	function transformGetResponse(data) {
		var results = angular.fromJson(data);
		return results.results;
	}


	/*
	 *
	 * service methods
	 *
	 */

	function JobService($resource) {
		return $resource( "/api/jobs/:id/\/.json", {id: "@id"}, basicService );
	}

	function ClientService($resource) {
		return $resource( "/api/clients/:id/\/.json", {id: "@id"}, basicService );
	}

	function UpdateService($resource) {
		return $resource( "/api/liveupdates/:id/\/.json", {id: "@job_id"}, basicService );
	}




	services.factory("Job", JobService );
	services.factory("Client", ClientService );
	services.factory("Update", UpdateService );


})();
