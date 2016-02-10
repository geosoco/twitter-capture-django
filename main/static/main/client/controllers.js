'use string';

(function() {

	function createSubmitErrorHandler(scope) {
		var _scope = scope;

		return function(error) {
			console.log("error");
			if("data" in error) {
				if(typeof error.data === 'object') {
					scope.errors = error["data"];
					return;
				} else if(typeof error.data === 'string') {
					scope.formerrors = [error.statusText, error.data];
				}
				
			} else {
				scope.formerrors = [error.statusText];
			}
		}
	}

	/*
	 *
	 * capture controller
	 *
	 */
	function ClientCtrl($scope, ClientFactory) {
		console.log("Clientctrl");
	}

	ClientCtrl.$inject = ['$scope', 'ClientFactory'];


	/*
	 *
	 * capture controller
	 *
	 */
	function ClientListCtrl($scope, ClientFactory) {
		var self = this;


		self.clients = ClientFactory.getClients();


		self.delete = function(obj) {
			var id = obj.id,
				ret = confirm("Press OK to delete the client '" + obj.username + "'");
			if(ret === true) {
				var index = self.clients.indexOf(obj);
				if(index >= 0) {
					var req = ClientFactory.delete(id);
					req.$promise.then(function(){
						self.clients.splice(index,1);
					}).catch(function(e){
						console.error(e);
					})
				}

			}
		}
	}

	ClientListCtrl.$inject = ['$scope', 'ClientFactory'];


	/*
	 *
	 * ClientAddCtrl
	 *
	 */
	function ClientAddCtrl($scope, $state, ClientFactory) {
		var self = this;
		
		self.verb = "Add";

		self.submitForm = function(v) {
			var c = ClientFactory.create(self.model);
			
			c.catch(createSubmitErrorHandler(self));
			c.then(function(){
				$state.go('client.list');
			});

		}

	}

	ClientAddCtrl.$inject = ['$scope', '$state', 'ClientFactory'];



	/*
	 *
	 * ClientEditCtrl
	 *
	 */
	function ClientEditCtrl($stateParams, $scope, $state, ClientFactory) {
		var self = this;
		
		self.verb = "Edit";

		self.model = ClientFactory.get($stateParams.id);

		self.submitForm = function(v) {
			var c = ClientFactory.update(self.model);

			c.$promise
				.catch(createSubmitErrorHandler(self))
				.then(function(){
					$state.go('client.list');
				});
		}
	}

	ClientEditCtrl.$inject = ['$stateParams', '$scope', '$state', 'ClientFactory'];


	/*
	 *
	 * capture controller
	 *
	 */

	angular.module('client.home')
		.controller('ClientListCtrl', ClientListCtrl)
		.controller('ClientCtrl', ClientCtrl)
		.controller('ClientAddCtrl', ClientAddCtrl)
		.controller('ClientEditCtrl', ClientEditCtrl);


})();