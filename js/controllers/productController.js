app.controller('productController', function($rootScope, $scope, $route, $routeParams, $sce, $location, api, cart, auth) {
	
	auth.get()

	$scope.user = auth.user;
	$scope.role = $scope.user;

	//check.product($routeParams);
	api.post("product", $routeParams.product).then(function(response) {
		$scope.product = response[0];
		if (response[0] == undefined) {
			$location.path("/404");
		}

		var origname = $scope.product.name;

		api.post("reviews", $scope.product.product_id).then(function(r) {
			$scope.reviews = r;
			$scope.posted = true;

			if (auth.user.customer) {
				for(var i = 0; i < $scope.reviews.length; i++) {
					console.log($scope.reviews[i])
					if ($scope.reviews[i].customer_id == auth.user.cred.details.customer_id) {
						$scope.posted = false;
					}
				}
			}
		})
	});

	if ($scope.user.admin) {
		api.get("warehouse").then(function(r) {
			console.log(r["man"])
			$scope.supply = r["man"];
		});
	}

	$scope.renderHtml = function(html_code)
	{
	    return $sce.trustAsHtml(html_code);
	};

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

	$scope.deleteReview = function(cust, prod) {
		console.log(cust);
		console.log(prod)
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

	$scope.deleteProduct = function() {
		console.log("Deleting product with id: " + $scope.product.product_id)
		api.delete("product", $scope.product).then(function(r) {
			console.log(r)
			$location.path("/" + $routeParams.category)
		})
	}
	$scope.man = null;

	$scope.updateProduct = function() {
		console.log($scope.product)
		console.log($scope.man)

		var supplier = null;

		if($scope.man != undefined)
			supplier = $scope.man

		console.log($scope.man)

		data = {
			product : $scope.product,
			supplier : supplier
		}

		console.log(data)

		api.post("updateproduct", data).then(function(r) {
			console.log(r);
			if (r == "OK")
				$location.path("/" + $routeParams.category )
		})
	}

});

app.controller('newProductController', function($scope, $location, $sce, auth, fileUpload, api, newProd){
	auth.get()

	$scope.user = auth.user;
	$scope.fileUpload = false;
	$scope.man = null;

	if (!auth.user.admin) {
		$location.path("/404");
	}
	$scope.product = {
		name : "Product name",
		price : 999,
		description: "Lorem Ipsum dolor sit amet with <strong>html markup</strong>",
		image : "http://placehold.it/500x500",
		in_stock : 99
	}

	$scope.category = newProd.getProduct();

	console.log($scope.category)

	api.get("warehouse").then(function(r) {
		console.log(r["man"])
		$scope.supply = r["man"];
	});

	if ($scope.category.category == undefined) {
		api.get("categories").then(function(r) {
			$scope.categories = r;
		})
	}


	// $scope.uploadImage = function() {
	// 	$scope.fileUpload = !$scope.fileUpload;

	// 	var file;

	// 	if ((document.getElementById('file'))!= undefined) {
	// 		file = document.getElementById('file').files[0]
	// 		console.log(file);

	// 		api.post('newproduct', file).then(function(r) {
	// 			console.log(r)
	// 		})
	// 	}
	// }

	$scope.addProduct = function() {
		console.log($scope.product)
		console.log($scope.man)
		console.log($scope.category)
		var data = {
			product : $scope.product,
			category : newProd.getProduct(),
			supplier : $scope.man[0]
		}

		data.product["slug"] = data.product.name;

		api.post("addproduct", data).then(function(r) {
			console.log(r);
			if (r == "OK")
				$location.path("/" + $scope.category.slug )
		})
	}

	$scope.renderHtml = function(html_code)
	{
	    return $sce.trustAsHtml(html_code);
	};
	
});