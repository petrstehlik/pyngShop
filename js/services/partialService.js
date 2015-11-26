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


app.controller('mainMenuController', function($scope, $http, api){
	api.get("categories").then(function(r) {
		$scope.categories = r;
	})
});

app.service('api', function($http, $log) {
	var url = "//" + API.host + ":" + API.port + "/" + API.version + "/";
	this.post = function(query, data) {
		var promise = $http({
			method : 'POST',
			headers: { 'Content-Type': 'application/json' },
			url : url + query,
			data : JSON.stringify(data)
		}).then(function successCallback(response) {
			return response["data"];
		}, function errorCallback(response) {
			$log.error(response);
			return response;
		});
		return promise;
	}

	this.get = function(query) {
		var promise = $http({
			method : 'GET',
			url : url + query,
		}).then(function successCallback(response) {
			return response["data"];
		}, function errorCallback(response) {
			$log.error(response);
			return response;
		});
		return promise;
	}
});