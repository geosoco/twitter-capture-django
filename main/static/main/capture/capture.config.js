'use string';
(function(){


function HomeConfig($stateProvider) {

	$stateProvider
		.state("main", {
			url: "/",
			templateUrl: "/static/main/capture/templates/capture.list.html",
			controller: "CaptureListCtrl as capture"
		})
		.state("capture", {
			url: "/capture",
			abstract: true,
			views: {
				"": {
					templateUrl: "/static/main/capture/templates/capture.root.html",
					controller: "CaptureRootCtrl as root"
				},
				"main@capture": {
					templateUrl: "/static/main/capture/templates/capture.edit.html",
					controller: "CaptureEditCtrl as capture"
				}
			}
		})
		.state("capture.create", {
			url: "/create",
			views: {
				"main@capture": {
					templateUrl: "/static/main/capture/templates/capture.create.html"
				},
			}
		})
		.state("capture.edit", {
			url: "/edit/:id",
			views: {
				"main@capture": {
					templateUrl: "/static/main/capture/templates/capture.edit.html",
					controller: "CaptureEditCtrl as capture"
				},
			}
		})		
		.state("capture.create.reddit", {
			url: "/reddit",
			views: {
				"main@capture": {
					templateUrl: "/static/main/capture/templates/capture.create.reddit.html"
				},
			}
		})
		.state("capture.create.reddit.randomsample", {
			url: "/randomsample",
			views: {
				"main@capture": {
					templateUrl: "/static/main/capture/templates/capture.create.reddit.randomsample.html",
					controller: "CaptureCreateRedditCtrl as ccrc"
				},
			}
		})
		.state("capture.create.reddit.streamfilters", {
			url: "/streamfilters",
			views: {
				"main@capture": {
					templateUrl: "/static/main/capture/templates/capture.create.reddit.streamfilters.html",
					controller: "CaptureCreateRedditCtrl as ccrc"
				},
			}
		})
		.state("capture.create.twitter", {
			url: "/twitter",
			views: {
				"main@capture": {
					templateUrl: "/static/main/capture/templates/capture.create.twitter.html"
				},
			}
		})
		.state("capture.create.twitter.randomsample", {
			url: "/randomsample",
			views: {
				"main@capture": {
					templateUrl: "/static/main/capture/templates/capture.create.twitter.randomsample.html",
					controller: "CaptureCreateTwitterCtrl as cctc"
				},
			}
		})
		.state("capture.create.twitter.streamfilters", {
			url: "streamfilters",
			views: {
				"main@capture": {
					templateUrl: "/static/main/capture/templates/capture.create.twitter.streamfilters.html",
					controller: "CaptureCreateTwitterCtrl as cctc"
				},
			}
		})
		.state("capture.details", {
			url: "",
			params: {
				details: { value: "details", squash: true }
			},
			views: {
				"details": {
					templateUrl: "/static/main/capture/templates/capture.details.html",
					controller: "CaptureDetailsViewCtrl as dv"
				}
			}
		})
		.state("capture.graphs", {
			url: "/graphs",
			params: {
				details: { value: "graphs", squash: true }
			},
			views: {
				"details": {
					templateUrl: "/static/main/capture/templates/capture.graphs.html",
					controller: "CaptureGraphsViewCtrl as gv"
				}
			}
		})
		.state("capture.tweets", {
			url: "/tweets",
			params: {
				details: { value: "tweets", squash: true }
			},
			views: {
				"details": {
					templateUrl: "/static/main/capture/templates/capture.tweets.html",
					controller: "CaptureTweetsViewCtrl as tv"
				}
			}
		})
		.state("capture.history", {
			url: "/history",
			params: {
				details: { value: "history", squash: true }
			},
			views: {
				"details": {
					templateUrl: "/static/main/capture/templates/capture.history.html",
					controller: "CaptureTermHistoryViewCtrl as thv"
				}
			}
		})
}

HomeConfig.$inject = ["$stateProvider"];

angular
	.module("main.home", ["main.services", "endpoint.factories"])
	.config(HomeConfig);

})();