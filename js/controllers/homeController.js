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

app.controller('categoryController', function($scope, $routeParams, $http, $log, api) {

	// if ($routeParams.page != NOTINDB) {
	// 	$location.path("/404");
	// }
	$scope.user = USER;
	$scope.cat = $routeParams.category;

	var queryData = { category : $routeParams.category };

	api.post("products", queryData).then(function(response) {
		$scope.products = response;
	});

});