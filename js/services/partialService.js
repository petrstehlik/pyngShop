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
		controller : "userMenu",
		templateUrl: SETTINGS.partials() + 'usermenu.html'
	};
});


app.controller('mainMenuController', function($scope, $http, api){
	api.get("categories").then(function(r) {
		$scope.categories = r;
	})
});

app.controller('userMenu', function($rootScope, $scope, cart) {
	
	//$rootScope.$broadcast('restorecart');

	$scope.cart = cart.model;

	$scope.$on('addToCart', function(event, args) {
		//if($scope.cart.items.indexOf(args) == -1) {
			($scope.cart.items).push(args);
			$scope.cart.count++;
			console.log($scope.cart)
		//}

	})

	$rootScope.$on('applycart', function(event, args) {
		$scope.cart = cart.model;
	});
});

app.service('api', function($http, $log) {
	var url = "//" + API.host + ":" + API.port + "/" + API.version + "/";
	this.post = function(query, data) {
		console.log(JSON.stringify(data));
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

app.factory('cart', function ($rootScope, $localStorage) {
	var service = {
	    model : {
			count : 0,
			items : []
		},

        SaveState: function () {
           $localStorage.cart = angular.toJson(service.model);
           console.log(service)
           //console.log($localStorage.list)
        },

        RestoreState: function () {
            service.model = angular.fromJson($localStorage.cart);
        },

        InitCart: function() {
        	if (angular.fromJson($localStorage.cart) == undefined) {
        		// var tmp = {model : }
	        	$localStorage.cart = angular.toJson({count : 0, items : []});
        	}
        },
        CleanCart: function() {
	        	$localStorage.cart = angular.toJson({count : 0, items : []});
        }
    }

    $rootScope.$on("initcart", service.InitCart);
    $rootScope.$on("cleancart", service.CleanCart);
    $rootScope.$on("savecart", service.SaveState);
    $rootScope.$on("restorecart", service.RestoreState);

    return service;
});

app.factory('page', function(){
  var title = "Default";
  return {
    title: function() { return title; },
    setTitle: function(newTitle) { title = newTitle; }
  };
});


app.filter("total", function() {
	return function(items) {
	  	var total = 0, i = 0;
	  	for (i = 0; i < items.length; i++) {
	  		total += items[i]['price'] * items[i]['quantity'];
	  		console.log(total);
	  	}

	  	return total;
	}
});