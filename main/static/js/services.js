var captureServices = angular.module('capture.services', ['ngResource']);


/*
 * Job
 */
captureServices.factory("Job", function($resource){
	return $resource( "/api/jobs/:id/\/.json", {id: "@id"}, 
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

/*
 * Client
 */

 captureServices.factory("Client",function($resource){
 	return $resource( "/api/clients/:id/\/.json", {id: "@id"},
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