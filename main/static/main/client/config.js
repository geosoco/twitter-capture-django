'use strict';

(function(){
	
	function ClientConfig($stateProvider) {
		$stateProvider
			.state("client", {
				url: "/client",
				abstract: true,
				controller: "ClientCtrl as root",
				templateUrl: "/static/main/client/templates/root.html",
			})
			.state("client.list", {
				url: "",
				templateUrl: "/static/main/client/templates/list.html",
				controller: "ClientListCtrl as lc"

			})
			.state("client.add", {
				url: "/add",
				templateUrl: "/static/main/client/templates/add.html",
				controller: "ClientAddCtrl as fc"
			})
			.state("client.edit", {
				url: "/{id:int}",
				templateUrl: "/static/main/client/templates/add.html",
				controller: "ClientEditCtrl as fc"
			});

	}

	ClientConfig.$inject = ["$stateProvider"];


	angular
		.module('client.home', ['ngMessages', 'endpoint.factories'])
		.config(ClientConfig);

})();