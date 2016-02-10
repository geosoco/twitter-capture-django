'use string';

(function() {

	function ArchiveCtrl($scope, CaptureFactory) {
		console.log("archivectrl");
	}

	ArchiveCtrl.$inject = ['$scope', 'CaptureFactory'];



	function ArchiveListCtrl($scope, CaptureFactory) {
		var self = this;


		self.archives = CaptureFactory.getArchives();
	}

	ArchiveListCtrl.$inject = ['$scope', 'CaptureFactory'];

	angular.module('archive.home')
		.controller('ArchiveListCtrl', ArchiveListCtrl)
		.controller('ArchiveCtrl', ArchiveCtrl);


})();