app.controller('homeController', function($scope){

	$scope.logo = "pyngShop";

});

app.controller('pageController', function($scope, $route, $routeParams, $location) {

	//if ($routeParams.page != NOTINDB) {
		$location.path("/404");
	}
	//console.log($routeParams.page);
	//$scope.test = $routeParams.page;
});