app.controller('productController', function($scope, $routeParams, api) {
	console.log($routeParams)

	var queryData = { category : $routeParams.category };

	api.post("products", queryData).then(function(response) {
		
		angular.forEach(response, function(value, key) {
			value.quantity = 1;
		})

		$scope.products = response;
	});
});