'use string';

(function() {

	function ArchiveCtrl($scope, CaptureFactory) {
		console.log("archivectrl-");
	}

	ArchiveCtrl.$inject = ['$scope', 'CaptureFactory'];



	function ArchiveListCtrl($scope, CaptureFactory) {
		var self = this;


		self.archives = CaptureFactory.getArchives();
	}

	ArchiveListCtrl.$inject = ['$scope', 'CaptureFactory'];

	function ArchiveDetailsViewCtrl($stateParams, $scope, CaptureFactory) {
		this.vm = this;

		this.model = CaptureFactory.get($stateParams.id);
		console.log("archive details");
		console.dir(this.model);
	}

	ArchiveDetailsViewCtrl.$inject = ['$stateParams', '$scope', 'CaptureFactory'];

	angular.module('archive.home')
		.controller('ArchiveListCtrl', ArchiveListCtrl)
		.controller('ArchiveCtrl', ArchiveCtrl)
		.controller('ArchiveDetailsViewCtrl', ArchiveDetailsViewCtrl);


})();