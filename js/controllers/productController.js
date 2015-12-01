app.controller('productController', function($rootScope, $scope, $routeParams, api, cart, auth) {
	
	auth.get()
	//check.product($routeParams);
	api.post("product", $routeParams.product).then(function(response) {
		$scope.product = response[0];

		api.post("reviews", $scope.product.product_id).then(function(r) {
			$scope.reviews = r;
			$scope.posted = true;

			for(var i = 0; i < $scope.reviews.length; i++) {
				console.log($scope.reviews[i])
				if ($scope.reviews[i].customer_id == auth.user.cred.details.customer_id) {
					$scope.posted = false;
				}
			}
		})
	});

	
	$scope.role = auth.user

	
	{}
	console.log($scope.reviews)


	$scope.addReview = function(review) {
		if (review.customer_id == undefined) {
			review.customer_id = auth.user.cred.details.customer_id;
		}
		if (review.email == undefined)
			review.email = auth.user.cred.details.email
		if (review.content == undefined)
			review.content = null

		review.product_id = $scope.product.product_id

		console.log(review)

		api.post("newreview", review).then(function(res) {
			console.log(res)

			api.post("reviews", $scope.product.product_id).then(function(r) {
				$scope.reviews = r;
			})
		})
	} 

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

	console.log($scope.role)
});