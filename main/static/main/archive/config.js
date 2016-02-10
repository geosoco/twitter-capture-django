'use strict';

(function(){
	
	function ArchiveConfig($stateProvider) {
		$stateProvider
			.state("archive", {
				url: "/archive",
				abstract: true,
				controller: "ArchiveCtrl as root",
				templateUrl: "/static/main/archive/templates/root.html",
			})
			.state("archive.list", {
				url: "",
				templateUrl: "/static/main/archive/templates/list.html",
				controller: "ArchiveListCtrl as listctrl"

			})

	}

	ArchiveConfig.$inject = ["$stateProvider"];


	angular
		.module('archive.home', ['endpoint.factories'])
		.config(ArchiveConfig);

})();