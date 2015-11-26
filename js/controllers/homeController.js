app.controller('homeController', function($scope, $http, page){

	$scope.logo = "pyngShop";

	console.log("hello");

	page.setTitle("Home");

	

});

app.controller('pageController', function($scope, $route, $routeParams, $location, $http) {

	// if ($routeParams.page != NOTINDB) {
	// 	$location.path("/404");
	// }
	console.log($routeParams.page);
	$scope.test = $routeParams.page;


});

app.controller('categoryController', function($rootScope, $scope, $routeParams, $http, $log, api, cart, page) {

	$rootScope.$broadcast("restorecart");
	$scope.user = USER;
	$scope.cat = $routeParams.category;
	page.setTitle($routeParams.category);

	var queryData = { category : $routeParams.category };

	api.post("products", queryData).then(function(response) {
		
		angular.forEach(response, function(value, key) {
			value.quantity = 1;
		})

		$scope.products = response;
	});

	$scope.addItem = function() {
		console.log("Adding item")
	}

	$scope.addToCart = function (item) {
		var added = false;

		if (cart.model == undefined)
			$rootScope.$broadcast("savecart");

		angular.forEach(cart.model.items, function(value, key) {
			if (!added) {
				if (value.product_id == item.product_id) {
					value.quantity++;
					added = true;
					console.log("found")
				}

				console.log(item)
				console.log(value)
			}
		});
		if (!added) {
			console.log(cart.model);
			cart.model.items.push(item)
		}
		cart.model.count++;
		$rootScope.$broadcast("savecart"); 
	}

});

app.controller('mainController', function($rootScope, $scope, cart, page){
	$rootScope.$broadcast('initcart');
	$rootScope.$broadcast('restorecart');

	$scope.page = page;
})