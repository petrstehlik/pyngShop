app.controller('cartController', function($scope, $rootScope, cart, page) {
	console.log(cart.model);

	$scope.cart = cart.model;

	page.setTitle("Cart");

	$scope.removeItems = function () {
		$rootScope.$broadcast('cleancart');
		$rootScope.$broadcast('restorecart');
		
		$rootScope.$broadcast('apply');
	}
})