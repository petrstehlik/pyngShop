app.controller('productController', function($rootScope, $scope, $routeParams, api, cart) {
	//check.product($routeParams);
	api.post("product", $routeParams.product).then(function(response) {
		$scope.product = response[0];

		api.post("reviews", $scope.product.product_id).then(function(r) {
			$scope.reviews = r;
		})
	});

	$scope.addToCart = function (item) {
		var added = false;

		if (cart.model == undefined)
			$rootScope.$broadcast("savecart");

		console.log(item)

		angular.forEach(cart.model.items, function(value, key) {
			if (!added) {
				if (value.product_id == item.product_id) {
					value.quantity += 1;
					added = true;
					console.log("found")
				}

				console.log(item)
				console.log(value)
			}
		});
		if (!added) {
			console.log(cart.model);
			item.quantity = 1;
			cart.model.items.push(item)
		}
		cart.model.count++;
		$rootScope.$broadcast("savecart"); 
	}
});