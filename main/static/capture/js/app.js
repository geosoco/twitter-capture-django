(function() {
	var captureApp = angular.module('capture.app', 
		['ui.router', 'capture.services', 'toastr', 'angularSpinner',
		'angularMoment', 'capture.controllers']);

	/*
	 * set up app config (csrf )
	 */
	captureApp.config(
		['$resourceProvider', '$httpProvider', '$locationProvider', 
		'$stateProvider', '$urlRouterProvider', 'toastrConfig', 
		'usSpinnerConfigProvider',
			function(
					$resourceProvider, 
					$httpProvider, 
					$locationProvider,
					$stateProvider,
					$urlRouterProvider,
					toastrConfig, 
					usSpinnerConfigProvider) {

				$resourceProvider.defaults.stripTrailingSlashes = false;

				$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
				$httpProvider.defaults.xsrfCookieName = 'csrftoken';

				$locationProvider.html5Mode(false).hashPrefix('!');

	}]);



	/*
	 *
	 *  set up toast
	 *
	 */
	captureApp.run(['$rootScope', '$controller', function($rootScope, $controller) {

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

})();