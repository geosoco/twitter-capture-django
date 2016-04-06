'use string';

(function(){



	/*
	 * CaptureListCtrl
	 *
	 *
	 */

	function CaptureListCtrl($scope, CaptureFactory) {
		this.test = "SOCO!";

		this.active_jobs = CaptureFactory.getActiveJobs();

		this.archive = function(job) {
			console.log("archiving2 " + job.id);
		}		
	}
	CaptureListCtrl.$inject = ['$scope', 'CaptureFactory'];


	/*
	 * CaptureListItemCtrl
	 *
	 *
	 */

	function CaptureListItemCtrl($scope, CaptureFactory) {
		var self = this;

		console.log("capturelistitemctrl");
		console.dir(this);
		console.dir($scope);

		self.archive = function(job) {
			console.log("archiving " + job.id);

			CaptureFactory.archive(job);
		}


		self.onActionClicked = function(job, action) {
			console.log("action clicked: " + job.id );
		}
	}

	CaptureListItemCtrl.$inject = ['$scope', 'CaptureFactory'];



	/*
	 * CaptureRootCtrl
	 *
	 *
	 */

	function CaptureRootCtrl($stateParams, $scope, CaptureFactory) {
		$scope.test = "LKJ";
		$scope.model = CaptureFactory.get($stateParams.id);
	}

	CaptureRootCtrl.$inject = ['$stateParams', '$scope', 'CaptureFactory'];


	/*
	 * CaptureCreateTwitterCtrl
	 *
	 *
	 */

	function CaptureCreateTwitterCtrl($stateParams, $scope, CaptureFactory) {
		var vm = this;
		vm.test = "LKJ";
		vm.model = {"name": "test"};
		vm.submit = function(){
			console.log("cookies")
		}
	}

	CaptureCreateTwitterCtrl.$inject = ['$stateParams', '$scope', 'CaptureFactory'];


	/*
	 * CaptureEditCtrl
	 *
	 *
	 */

	function CaptureEditCtrl($stateParams, $scope, CaptureFactory) {
		var vm = this;

		vm.step = $stateParams.step;
		console.log(vm.step);
	}

	CaptureEditCtrl.$inject = ['$stateParams', '$scope', 'CaptureFactory'];


	/*
	 * CaptureDetailsViewCtrl
	 *
	 *
	 */

	function CaptureDetailsViewCtrl($stateParams, $scope, CaptureFactory) {
		this.vm = this;

		this.model = CaptureFactory.get($stateParams.id);
	}

	CaptureDetailsViewCtrl.$inject = ['$stateParams', '$scope', 'CaptureFactory'];


	/*
	 * CaptureGraphsViewCtrl
	 *
	 *
	 */

	function CaptureGraphsViewCtrl($stateParams, $scope, CaptureFactory) {
		this.vm = this;

		this.model = CaptureFactory.get($stateParams.id);

	}

	CaptureGraphsViewCtrl.$inject = ['$stateParams', '$scope', 'CaptureFactory'];


	/*
	 * CaptureTweetsViewCtrl
	 *
	 *
	 */

	function CaptureTweetsViewCtrl($stateParams, $scope, CaptureFactory) {
		this.vm = this;

		this.model = CaptureFactory.get($stateParams.id);
	}

	CaptureTweetsViewCtrl.$inject = ['$stateParams', '$scope', 'CaptureFactory'];


	/*
	 * CaptureTermHistoryViewCtrl
	 *
	 *
	 */

	function CaptureTermHistoryViewCtrl($stateParams, $scope, CaptureFactory) {
		this.vm = this;

		this.model = CaptureFactory.get($stateParams.id);
	}

	CaptureTermHistoryViewCtrl.$inject = ['$stateParams', '$scope', 'CaptureFactory'];	

	//
	//
	//
	//
	//
	

	angular.module('main.home')
		.controller('CaptureListCtrl', CaptureListCtrl)
		.controller('CaptureListItemCtrl', CaptureListItemCtrl)
		.controller('CaptureEditCtrl', CaptureEditCtrl)
		.controller('CaptureDetailsViewCtrl', CaptureDetailsViewCtrl)
		.controller('CaptureGraphsViewCtrl', CaptureGraphsViewCtrl)
		.controller('CaptureTweetsViewCtrl', CaptureTweetsViewCtrl)
		.controller('CaptureRootCtrl', CaptureRootCtrl)
		.controller('CaptureTermHistoryViewCtrl', CaptureTermHistoryViewCtrl)
		.controller('CaptureCreateTwitterCtrl', CaptureCreateTwitterCtrl)

})();