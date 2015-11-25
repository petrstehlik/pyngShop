app.controller('homeController', function($scope, $http){

	$scope.logo = "pyngShop";

	console.log("hello");

	

});

app.controller('pageController', function($scope, $route, $routeParams, $location, $http) {

	// if ($routeParams.page != NOTINDB) {
	// 	$location.path("/404");
	// }
	console.log($routeParams.page);
	$scope.test = $routeParams.page;


});

app.controller('categoryController', function($scope, $route, $routeParams, $location, $http) {

	// if ($routeParams.page != NOTINDB) {
	// 	$location.path("/404");
	// }
	$scope.test = $location.page;

	console.log($routeParams)

	$http({
		method : 'POST',
		//headers: { 'Content-Type': 'application/json' },
		headers: { 'Content-Type': 'application/json' },
		url : "//localhost:5000/v1/products",
		data : JSON.stringify({ category : $routeParams.category})
	}).then(function successCallback(response) {
		$scope.products = response["data"];
		console.log(response)
	}, function errorCallback(response) {
		// $scope.categories = response["data"];
		console.log(response)
	});
	//$http.get('http://localhost:5000/v1/products?category=' + $routeParams.category)

});