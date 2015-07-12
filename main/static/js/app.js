var captureApp = angular.module('capture.app', ['ngRoute', 'capture.services', 'capture.controllers']);

/*
 * set up app config (csrf )
 */
captureApp.config(['$resourceProvider', '$httpProvider', '$routeProvider', '$locationProvider', 
	function($resourceProvider, $httpProvider, $routeProvider, $locationProvider) {
		$resourceProvider.defaults.stripTrailingSlashes = false;

		$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
		$httpProvider.defaults.xsrfCookieName = 'csrftoken';

		$locationProvider.html5Mode(false).hashPrefix('!');

		$routeProvider
			.when('/', {controller: 'jobListControl'})
			.when('/job/create/', {controller: 'jobCreateController'})
			.when('/job/:id/', {controller: 'jobEditController'})
}]);



/*
 *
 *  set up toast
 *
 */
captureApp.run(['$rootScope', '$route', '$controller', function($rootScope, $route, $controller) {

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


	// set the $route on the rootScope
	$rootScope.$route = $route;

	// add a handler to set the controller name
	$rootScope.$on("$routeChangeSuccess", function(e, data, previous) {
    	$rootScope.controller = data.controller;

    	console.log("routeChangeSuccess")
    	console.dir(e);
    	console.dir(data);

    	if("activate" in data.controller && typeof data.controller.activate === "function") {
    		data.controller.activate(data);
    	}
	});
}]);

