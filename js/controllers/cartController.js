app.controller('cartController', function($scope, $route, $rootScope, cart, page) {
	console.log(cart.model);

	page.setTitle("Cart");

	$scope.cart = cart.model;

	$scope.removeItems = function () {
		$rootScope.$broadcast('cleancart');
		$rootScope.$broadcast('restorecart');
		$rootScope.$broadcast('applycart');
		$scope.cart = cart.model;
		$route.reload();
		
	}
});

var ordered = {}

app.controller('checkoutController', function($scope, $route, $rootScope, $location, cart, page, api, auth) {
	// console.log(cart.model);

	$scope.user = auth.get();
	if ($scope.user.customer == true)
		$scope.customer = $scope.user.cred.details

	console.log($scope.customer);

	page.setTitle("Cart");

	$scope.cart = cart.model;

	api.get("shipping").then(function(response) {
		$scope.shipping = response;
	});

	$scope.removeItems = function () {
		$rootScope.$broadcast('cleancart');
		$rootScope.$broadcast('restorecart');
		$rootScope.$broadcast('applycart');
		$scope.cart = cart.model;
		$route.reload();
	}

	$scope.order = function(customer, shipping, cart) {

		customer["telephone"] = customer["telephone"].replace(/[+]/g, '00');

		api.post("order", {customer : customer, shipping: shipping, cart: cart}).then(function(response) {
			if (response = "1") {
				ordered = {customer : customer, shipping: shipping, cart: cart};
				
			}
			console.log(response)
			console.log("redirecting")
			$location.path("checkout/success");
		});
		
	}
});

app.controller('successController', function($scope, $rootScope, page, cart) {
	page.setTitle("Successfull order")
	$rootScope.$broadcast('cleancart');
	cart.model.count = 0;
	$scope.cart = cart.model;
})

app.controller('invoiceController', function($scope, $rootScope, $routeParams, api) {
	console.log($routeParams.id);

	$scope.authorized = 0;

	$scope.check = function(user) {
		api.post('invoice', user).then(function(response) {
			console.log(response);
			if (response.valid == "true") {
				$scope.authorized = 1;
				$scope.invoice = response;
			}
		})
	}
	
})