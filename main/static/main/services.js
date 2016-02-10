'use string';

(function() {


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

	function UserService($resource) {
		return $resource( "/api/users/:id/", {id: "@id"}, basicService );
	}

	function GroupService($resource) {
		return $resource( "/api/groups/:id/", {id: "@id"}, basicService );
	}


	function JobService($resource) {
		return $resource( "/api/jobs/:id/", {id: "@id"}, basicService );
	}

	function ClientService($resource) {
		return $resource( "/api/clients/:id/", {id: "@id"}, basicService );
	}

	function UpdateService($resource) {
		return $resource( "/api/liveupdates/:id/", {id: "@job_id"}, basicService );
	}



	var services = angular.module('main.services', ['ngResource']);

	services.factory("User", UserService);
	services.factory("Group", GroupService);
	services.factory("Job", JobService );
	services.factory("Client", ClientService );
	services.factory("Update", UpdateService );


})();
