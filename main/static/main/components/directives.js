'use string';

(function(){
	
	function LineGraphDirective($document, $q) {
		return {
			restrict: 'E',
			scope: {
				names: '='
			},
			link: function(scope, element, attrs) {
				
			}
		}
	}


	angular
		.module('main.directives', [])
		.directive('linegraph', ['$document', '$q', LineGraphDirective])


})();