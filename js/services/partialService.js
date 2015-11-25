app.directive("mainMenu", function() {
	return {
		scope: {
			section: '=',
		},
		templateUrl: SETTINGS.partials() + 'mainmenu.html'
	};
});

app.directive("userMenu", function() {
	return {
		scope: {
			section: '=',
		},
		templateUrl: SETTINGS.partials() + 'usermenu.html'
	};
});


app.controller('mainMenuController', function($scope, $http){
	$http({
		method : 'GET',
		url : "http://localhost:5000/v1/categories"
	}).then(function successCallback(response) {
		$scope.categories = response["data"];
		console.log(response["data"])
	});
})