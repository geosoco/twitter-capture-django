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
		if($stateParams.id !== undefined) {
			$scope.model = CaptureFactory.get($stateParams.id);	
		} else {
			$scope.model = {};
		}
		
	}

	CaptureRootCtrl.$inject = ['$stateParams', '$scope', 'CaptureFactory'];


	/*
	 * CaptureCreateTwitterCtrl
	 *
	 *
	 */

	function CaptureCreateTwitterCtrl($stateParams, $scope, uiGmapIsReady, CaptureFactory) {
		var vm = this;
		vm.test = "LKJ";
		vm.model = {"name": "", "terms": [], "georects": [], "selectedRectangle": null};
		vm.rects = [];
		vm.selectedRectangle = null;
		vm.submitted = false;


		vm.drawingManagerControl = {};
		vm.drawingOptions = {
			drawingMode: google.maps.drawing.OverlayType.RECTANGLE,
			rectangleOptions: { editable: true, draggable: true}
		}


		$scope.map = { center: { latitude: 45, longitude: -73 }, zoom: 8 };
		$scope.drawingControlOptions = {
			position: google.maps.ControlPosition.TOP_CENTER,
			drawingModes: [
				google.maps.drawing.OverlayType.RECTANGLE
			],

		}


		vm.onCreationSuccess = function(obj) {
			console.log("successfully created");
		}

		vm.onCreationError = function(response) {
			console.log("failed to create object");

			console.dir(response);
		}


		vm.submit = function(){
			vm.submitted = true;
			console.log("cookies");
			angular.forEach($scope.form.$error.required, function(field) {
				field.$setTouched();
			});

			if($scope.form.$valid) {
				// set the description to the name initially
				vm.model.description = vm.model.name;


				var promise = CaptureFactory.create(vm.model);

				promise.$promise.then(vm.onCreationSuccess, vm.OnCreationError);
			}
		}


		vm.selectRectangle = function(rect) {
			if (vm.selectedRectangle !== null){
				vm.selectedRectangle.setOptions({fillColor:'black'});
			}

			vm.selectedRectangle = rect;
			vm.selectedRectangle.setOptions({fillColor:'blue'});
		}

		vm.rectangleClicked = function(rect, eventName, arguments, model){
			vm.selectRectangle(this);
		}
		

		vm.deleteSelected = function(){
			if(vm.selectedRectangle !== null){
				vm.selectedRectangle.setMap(null);
				var idx = vm.rects.findIndex(function(el){return el == vm.selectedRectangle});
				if (idx !== undefined){
					vm.rects.splice(idx, 1)
				}
			}
		}


		//
		// init code
		//

		uiGmapIsReady.promise(1).then(function(instances){
			google.maps.event.addListener($scope.drawingControlOptions.getDrawingManager(), 'rectanglecomplete', function (e) {
				vm.rects.push(e);
				e.addListener('click', vm.rectangleClicked);
				vm.selectRectangle(e);
			});
		})

		$scope.$watch('$scope.drawingControlOptions.getDrawingManager', function(val) {
			if (!$scope.drawingControlOptions.getDrawingManager) {
				return;
			}


		});
	}

	CaptureCreateTwitterCtrl.$inject = ['$stateParams', '$scope', 'uiGmapIsReady', 'CaptureFactory'];


	/*
	 * CaptureCreateRedditCtrl
	 *
	 *
	 */

	function CaptureCreateRedditCtrl($stateParams, $scope, CaptureFactory) {
		var vm = this;
		vm.test = "LKJ";
		vm.model = {"name": "", "terms": [], "subreddits": [], "threads": [], "chainrxn": false};
		vm.submit = function(){
			console.log("cookies")
		}
	}

	CaptureCreateRedditCtrl.$inject = ['$stateParams', '$scope', 'CaptureFactory'];


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
		.controller('CaptureCreateRedditCtrl', CaptureCreateRedditCtrl)

})();