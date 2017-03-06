app.controller('homeController', function($scope, $http, page){

	$scope.logo = "pyngShop";

	page.setTitle("Home");

	

});

app.controller('pageController', function($scope, $route, $routeParams, $location, $http) {

	// if ($routeParams.page != NOTINDB) {
	// 	$location.path("/404");
	// }
	console.log($routeParams.page);
	$scope.test = $routeParams.page;


});

app.controller('categoryController', function($rootScope, $scope, $routeParams, $http, $log, $location, $sce, api, cart, page, newProd) {

	$rootScope.$broadcast("restorecart");
	$scope.user = USER;
	var categories = $routeParams.category.split("/");
	$scope.cat = categories[categories.length - 1]

	$scope.url = $location.absUrl();

	$scope.goback = function () {
		history.back()
		console.log("goind back")
	}

	var queryData = { category : $scope.cat, menu : $scope.categories };
	//var tmp = queryData.category.search(/\/./);

	//console.log(tmp);

	api.post("products", queryData).then(function(response) {
		$scope.products = response["products"];
		$scope.category = response["category"][0];
		page.setTitle($scope.category.name);
	});

	$scope.addItem = function() {
		newProd.storeProduct($scope.category);
		console.log(newProd.getProduct())
		$location.path("/p/addproduct");
	}

	$scope.addToCart = function (item) {
		var added = false;

		if (cart.model == undefined)
			$rootScope.$broadcast("savecart");

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

	$scope.renderHtml = function(html_code)
	{
	    return $sce.trustAsHtml(html_code);
	};

});

app.controller('mainController', function($rootScope, $scope, cart, page){
	$rootScope.$broadcast('initcart');
	$rootScope.$broadcast('restorecart');

	$scope.page = page;
})

app.controller('notFoundController', function($scope){
	
});